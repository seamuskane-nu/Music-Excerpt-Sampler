"""log spectrum flux FFT onset detection module"""

from typing import Tuple
import numpy as np
from scipy.signal import get_window
import librosa

def audio_loader(file_path:str) -> Tuple[np.array, float]:
    """ Uses log spectral flux style onset detection with ffts
        to output the list of all onsets in an audio file as well
        as duration of track for ease of use

        Arg: file_path 
        Returns: Tuple of duration and list of onsets
    """
    # load the audio into samplerate, and list of audio samples
    try:
        # function changed to use librosa
        # scipy only uses wav while librosa can use all formats
        # otherwise I can't accomodate entire music library of various formats
        # scipy = just wav, librosa = all
        y, sr = librosa.load(file_path, sr=None, mono=True)
        max_amplitude = np.max(np.abs(y))
        if max_amplitude > 0:
            normalized_data = y / max_amplitude
        else:
            normalized_data = y
        return normalized_data, sr

    except FileNotFoundError:
        print(f"Error: file {file_path} was not found")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

    """
    # Uncomment to use with scipy
    # find max amplitude

    # normalize values to be between -1 and 1
    if max_amplitude > 0:
        normalized_data = data / max_amplitude
    else:
        normalized_data = data

    # make it mono
    mono_normalized_data = np.mean(normalized_data, axis=1)

    return mono_normalized_data, samplerate
    """

def window_fft(signal: np.array, frame_size: int = 2048, hop_size:int = 512) -> None:
    """
    Windowing and FFT phase
    takes in normalized and average signal for processing
    """
    window = get_window('hann', frame_size)
    num_frames = (len(signal) - frame_size) // hop_size + 1
    spectra = []

    for i in range(num_frames):
        start = i * hop_size
        # get frames
        frame = signal[start : start + frame_size]
        # apply window to frames
        windowed_frame = frame * window
        # apply fft to frames
        fft_result = np.fft.rfft(windowed_frame)
        # use abs to get the largest magnitude of each frame
        magnitude = np.abs(fft_result)
        # do log operations (human hearing is logarithmic)
        log_magnitude = np.log1p(magnitude * 1000)
        spectra.append(log_magnitude)

    return np.array(spectra)

def calculate_flux(spectra: np.array) -> None:
    """
    takes in spectra and calculates flux (finds onsets)
    """
    #takes the difference between frames, showing where new freq start appearing
    diff = np.diff(spectra, axis=0)

    # half wave rectification - we only care about increase in enrgy not decreases
    rect = np.maximum(0, diff)

    # gives sum across all freq bins for each frame
    flux = np.sum(rect, axis=1)

    return flux

def find_peaks(flux: np.array, threshold_factor: float = 1.0) -> np.array:
    thresh = np.mean(flux) + threshold_factor * np.std(flux)

    local_max = (flux[1:-1] > flux[:-2]) & (flux[1:-1] > flux[2:])

    above_thresh = flux[1:-1] > thresh
    peaks = local_max & above_thresh
    frame_peaks = np.where(peaks)[0]

    frame_peaks = frame_peaks + 1

    return frame_peaks

def frames_to_sec(frame_peaks: np.array, samplerate: int, hop_size: int) -> np.array:
    """
    converts the frame peaks to their actual time in the audio
    uses frame_peak data, samplerate, and hop size to achieve
    returns np.array
    """
    frame_sec = (frame_peaks * hop_size) / samplerate
    return frame_sec

def detect_onsets_inhouse(
        file_path:str,
        frame_size: int = 2048, 
        hop_size:int = 512, 
        threshold_factor: float = 1.25) -> Tuple[float, list[float]]:
    """
    Detects onsets in audio file using spectral flux
    takes in: 
    file_path
    frame_size
    hop_size
    threshold_factor
    """
    signal, samplerate = audio_loader(file_path)

    if signal is None:
        return 0.0, []
    duration = len(signal) / samplerate
    spectra = window_fft(signal, frame_size, hop_size)
    flux = calculate_flux(spectra)
    frame_peaks = find_peaks(flux, threshold_factor)
    onsets = frames_to_sec(frame_peaks, samplerate, hop_size)
    return duration, list(onsets)

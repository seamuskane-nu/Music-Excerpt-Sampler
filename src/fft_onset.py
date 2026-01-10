"""log spectrum flux FFT onset detection module"""

from typing import Tuple
import numpy as np
import scipy.io.wavfile as wavfile
from scipy.signal import get_window

def audio_loader(file_path:str) -> Tuple[np.array, float] :
    """ Uses log spectral flux style onset detection with ffts
        to output the list of all onsets in an audio file as well
        as duration of track for ease of use

        Arg: file_path 
        Returns: Tuple of duration and list of onsets
    """
    # load the audio into samplerate, and list of audio samples
    try:
        samplerate, data = wavfile.read(file_path)
    except FileNotFoundError:
        print(f"Error: file {file_path} was not found")
    except Exception as e:
        print(f"An error occurred: {e}")

    # convert audio samples to float format if not already there
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.uint8:
        data = (data.astype(np.float32) - 128.0) / 128.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0

    # find max amplitude
    max_amplitude = np.max(np.abs(data))

    # normalize values to be between -1 and 1
    if max_amplitude > 0:
        normalized_data = data / max_amplitude
    else:
        normalized_data = data

    # make it mono
    mono_normalized_data = np.mean(normalized_data, axis=1)

    return mono_normalized_data, samplerate

def window_fft(signal: np.array, frame_size: int = 2048, hop_size:int = 512) -> None:
    """
    Windowing and FFT phase
    takes in normalized and average signal for processing
    """
    
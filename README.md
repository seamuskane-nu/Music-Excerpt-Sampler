# Music Excerpt Sampler

An intelligent audio sampling tool that selects contextually meaningful excerpts from your 
music library using beat-detection, BPM analysis, and custom onset detection algorithms.

## Features

- **Three Selection Modes:**
  - **Beat Mode:** Beat mode will start on a random beat in the song, and play n number of bars from it (default = 4)
  - **Bar Mode:** Bar mode will choose a random onset/transient, and play n number of bars from it (for context in music, length matters)
  - **Manual Mode:** Manual onset mode will choose a random onset/transient, and play a set excerpt length from it (default = 8seconds)

- **Dual Onset Detection Algorithms:**
  - **Librosa:** Librosa is an industry standard for python implementation of DSP with algorithms yielding reliable results

  - **Custom FFT-Based:**  My custom FFT-based algorithm uses a log magnitude spectral flux approach,
                           with easily tunable parameters to allow the user to tailor their results.

- **Smart Caching System:**  Whenever an excerpt is selected, the file_path, duration of audio, beats (exact time of each beat),
                             and the onsets from the respective onset algorithm are saved. When the same file is loaded again,
                             the computation to calculate onsets and beats is referenced, improving speeds for users. The cache
                             will only store information being used, so if the user opts to never change the algorithm, the
                             computation will never be calculated nor stored.

- **Audio Playback & Export:**  With excerpts, you can use basic playback options to listen to it within the program, and volume controls
                                to tailor to your liking. An export option is also available, that will by default export the excerpt in .wav
                                format. This can be changed by altering the file extension in exporter.py

- **Multi-Format Support:**  By default, wav, flac, ogg, and aiff are supported. With FFmpeg installed, mp3, mp4, wma, and aac become available

## Installation

### Prerequisites
- Python 3.9+
- **FFmpeg** (required for MP3/M4A support)
  - **macOS:** `brew install ffmpeg`
  - **Linux:** `sudo apt install ffmpeg`
  - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org) and add to PATH

### Setup

1. Clone the repository:
```bash
   git clone [your-repo-url]
   cd Music-Excerpt-Sampler
```

2. Create virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt
```

4. Configure music folder:
   - Open `src/config.py`
   - Set `MUSIC_FOLDER = "/path/to/your/music"`
   - Optionally adjust `EXCERPT_LENGTH` and `EXPORTS_FOLDER`

## Usage

Run the application:
```bash
python src/main.py
```

### Controls

- **`R`** - Randomize new excerpt from your library
- **`P`** - Play/Pause current excerpt
- **`B`** - Toggle selection mode (beat/bar/manual)
- **`A`** - Switch onset detection algorithm (librosa/custom)
- **`+`** - Increase volume
- **`-`** - Decrease volume
- **`E`** - Export current excerpt to file
- **`Q`** - Quit and save cache

### Example Workflow

1. Start the app
2. Press R to select a random excerpt
3. Press P to play it
4. Press B to try different modes
5. Press E to export your favorite

## Technical Implementation

### Custom Onset Detection Algorithm

The custom onset detector implements **spectral flux analysis** from scratch using NumPy and SciPy:

#### Signal Processing Pipeline

1. **Audio Loading & Normalization**
   -  Audio is loaded using librosa (for its audio extension support) in mono, and normalized between -1 and 1 float values

2. **Windowing & FFT**
   -  From the mono normalized audio, the frames are acquired and a hann window is applied to the frames for spectral accuracy. 
      Each frame then undergoes a fast fourier transform to give the spectral domain info, and from each frame the maximum amplitudes
      are gathered. Log operations are then used to accommodate human hearing which is logarithmic.

3. **Spectral Flux Calculation**
   -  Frames differences are calculated to find new frequency increases, and half wave rectification occurs to eliminate decreases in spectral
      energy from the data. The flux is returned by getting the sum of all frequency bins for each frame.

4. **Peak Detection**
   -  Peak detection occurs with adaptive thresholding, with the frequency amplitude averages and standard deviation being used to pick amplitudes
      that are significant, and compares them against local maxima to select specific onsets.

5. **Time Conversion**
   -  Time conversion then occurs to turn the frame peak data into the time in audio when the event occurs.

#### Performance

- Achieves **98% accuracy** compared to librosa (industry standard)
- Example: 242 onsets detected vs 246 from librosa on test file

#### Performance Comparison

| Metric | Custom Algorithm | Librosa|
|--------|-----------------|---------|
| Onsets(test)| 242        | 246     |
| Accuracy    | 98.4%      | 100%(ref)|
| Processing speed | ~2-3s | ~1-2s   |
| Tunable parameters | Yes | Limited |

### Architecture
```
src/
├── main.py           -  Handles CLI and coordinates modules to run
├── selector.py       -  Selects the random excerpt timing from onset and BPM timing
├── fft_onset.py      -  Custom algorithm for onset detection
├── player.py         -  Handles audio playback and volume
├── cache.py          -  Creates cache structure for storing audio info
├── scanner.py        -  Scans file system for audio files
├── exporter.py       -  Exports current excerpt into folder
└── config.py         -  Holds reference information for excerpt preferences
```

### Selection Modes Explained

**Beat Mode:**
-  Beat mode will detect every single timestamp of a beat in the audio, and select one randomly. This ensures you are always
   starting on a beat and have musical context in excerpts. It plays x number of bars from the sample, so if bars = 2, it will be play 8
   full beats of audio.
-  This is the most user friendly mode for coherent sampling, because it sounds most normal to use audio in context!

**Bar Mode:**
-  Bar mode selects a random onset timestamp from the audio, and plays x number of bars from that timestamp. This means you will
   never start in the middle of a sound (like a cymbal) but at the beginning of a transient for context.
-  This mode was added as a distinction from Manual Mode, because having a contextual length for the sample can be important.

**Manual Mode:**
-  Manual mode, like bar mode, starts on a random onset timestamp, and plays a x number of seconds from the timestamp.
-  This is good for quick sampling or scenarios where you don't care about the end of the clip as it usually ends abruptly.

## Configuration

Edit `src/config.py` to customize:
```python
MUSIC_FOLDER = "/path/to/music"     # Your music library location
EXCERPT_LENGTH = 8.0                # Default excerpt duration (seconds)
EXPORTS_FOLDER = "./exports"        # Where to save exported excerpts
CACHE_FILE = "onset_cache.json"     # Cache storage location
```

## Dependencies

### Core Libraries
- **librosa** - Audio analysis, beat detection, BPM estimation
- **numpy** - Numerical computing and array operations
- **scipy** - Signal processing (FFT, windowing)
- **pygame** - Audio playback engine
- **pydub** - Audio manipulation and export

See `requirements.txt` for complete dependency list with versions.

## How It Works

### Caching System

The application caches analysis results to dramatically improve performance:

- Stores: file path, duration, beat positions, BPM, and onset times
- Separate storage for each algorithm (librosa vs custom)
- Only computes what's needed - switching algorithms triggers new analysis
- Automatically invalidates cache if source file is modified
- Typical speedup: 10-20x faster on subsequent loads

### Beat vs Onset Detection

Beat detection is the most "normal" sounding kind of excerpt because it sounds most like music to our ears. This is what you have
listened to your whole life, because the rhythm starts on the first beat and ends on the last.

Onset detection starts at the beginning of a random sound, and can feel more jarring compared to Beat detection, but is integral to 
the image intended for this program. This is a random sampler, used for producers and musicians to find inspiration and samples in their own
music. If every clip is "perfectly" synced, the program loses some of the purpose it was intended for when considering true randomness.
Onset detection is a compromise between being truly random and still being usable.

## Limitations

- Beat mode currently only supports 4/4 time signature
- Can not choose to start on first beat, it could be any beat in 4/4

## Future Enhancements

- [ ] GUI interface using tkinter or PyQt
- [ ] Support for additional time signatures (3/4, 6/8, etc.)
- [ ] Real-time visualization of waveforms and onset detection
- [ ] Simple effects such as speeding up, slowing down, and pitch shifting
- [ ] Cache mode that allows full library to be cached overnight (all computation at once) to avoid having slowdowns when in use

## Troubleshooting

### Common Issues

**"No audio files found"**
- Check that the path to music is changed in config.py

**"Cache file corrupted"**
- Delete the cache file and re-run the program to create new one

**"FFmpeg not found"**
- Download ffmpeg using brew (macos), or download from website and make sure it is added to system path

## License
MIT License - See LICENSE file for details

## Author
Seamus Kane

## Contact
email: seamuskane46@gmail.com
github: seamuskane-nu
---

**Built with Python, NumPy, and a passion for music and signal processing**
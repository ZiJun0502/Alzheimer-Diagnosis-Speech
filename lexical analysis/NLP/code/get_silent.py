from pydub import AudioSegment
from pydub.silence import split_on_silence
"""
Usage:
a = AudioSilentAnalyzer('./Audio_Reduced/Baycrest2103.wav')
num_silent, silent_proportion = a.get_silent()
"""
class AudioSilentAnalyzer:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        format = audio_path.split('.')[-1]
        self.audio_seg = AudioSegment.from_file(audio_path, format=format)

    def get_silent(self) -> tuple[int, float]:  # (total # of silent chunks, silent proportion)
        chunks = split_on_silence(self.audio_seg,
                                  min_silence_len=300,
                                  silence_thresh=self.audio_seg.dBFS - 16,
                                  keep_silence=250
                                  )
        total_silent_chunks = len(chunks)
        total_silent_duration = sum(len(x) for x in chunks)
        audio_duration = len(self.audio_seg)
        silent_proportion = total_silent_duration / audio_duration if audio_duration > 0 else 0.0

        return total_silent_chunks, silent_proportion
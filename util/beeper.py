import pyaudio
import numpy as np


class Beeper(object):
    """
    The beeper object.
    """

    def __init__(self, volume=0.1, duration=0.5):
        self.p = pyaudio.PyAudio()
        self.fs = 44100
        self.volume = volume
        self.duration = duration

    def _locking_tone(self, frequency):
        samples = (np.sin(2 * np.pi * np.arange(self.fs*self.duration)*frequency / self.fs)).astype(np.float32)
        stream = self.p.open(format=pyaudio.paFloat32,
                             channels=1,
                             rate=self.fs,
                             output=True)
        stream.write(self.volume * samples)
        stream.stop_stream()
        stream.close()

    def play_locking_start_tone(self):
        self._locking_tone(500)

    def play_locking_end_tone(self):
        self._locking_tone(300)

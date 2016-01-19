from ctypes import *
import math
import time
from scipy.signal import resample
try:
    from sdl2 import *
    from sdl2.ext import Resources
    from sdl2.ext.compat import byteify
except ImportError:
    import traceback
    traceback.print_exc()
    sys.exit(1)


class RawAudio(object):
  def __init__(self, freq):
    self._bufpos = 0
    self.done = False
    self.infreq = freq
    self.spec = SDL_AudioSpec(freq, AUDIO_S16, 1, 1024,
                              SDL_AudioCallback(self._play_next))
    obtained = SDL_AudioSpec(0,0,0,0)
    self._buffer = []
    
    self.devid = devid = SDL_OpenAudioDevice(None, 0, self.spec, obtained, 0)
    print obtained.freq
    self.outputspec = obtained
    if devid == 0:
        raise RuntimeError("Unable to open audio device: {}".format(SDL_GetError()))
    SDL_PauseAudioDevice(devid, 0)
    
  def _play_next(self, notused, stream, length):
    if len(self._buffer) < length:
      print 'input stalled', len(self._buffer)
      #return
    numbytes = min(length, len(self._buffer))
    for i in range(0, numbytes):
      stream[i] = self._buffer[i]
    
    self._buffer = self._buffer[numbytes:]
    self._bufpos += numbytes
    
    for i in range(numbytes, length):
      stream[i] = 0
  
  # 16bit PCM signed
  def putData(self, data):
    if self.infreq != self.outputspec.freq:
      ratio = 1.0*self.outputspec.freq/self.infreq
      data = resample(list(data), int(len(data)*ratio)).astype(int)
    
    samples = len(data)
    ar = cast((c_short*samples)(*data), POINTER(c_byte * (samples * 2)))
    #print len(list(ar[0])), slen
    self._buffer.extend(list(ar[0]))
  
  
def main():
    if SDL_Init(SDL_INIT_AUDIO) != 0:
        raise RuntimeError("Cannot initialize audio system: {}".format(SDL_GetError()))

    sound = RawAudio(48000)

    while not sound.done:
        SDL_Delay(100)
    SDL_CloseAudioDevice(sound.devid)

    SDL_Quit(SDL_INIT_AUDIO)


if __name__ == '__main__':
    main() 

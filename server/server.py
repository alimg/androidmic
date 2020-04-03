#!/usr/bin/env python
import socketserver
import struct

from audio import RawAudio

try:
    from sdl2 import *
    from sdl2.ext import Resources
    from sdl2.ext.compat import byteify
except ImportError:
    import traceback
    import sys

    traceback.print_exc()
    sys.exit(1)

sound = None


class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        global sound
        data = self.request[0]
        socket = self.request[1]
        # print data
        freq, ind = struct.unpack("!ii", data[0:8])
        data = data[8:]
        buff = struct.unpack(str(len(data) // 2).encode() + b"h", data)

        if not sound:
            sound = RawAudio(freq)
            print(f"input from {self.client_address[0]} @{freq} {len(data)} bytes")

        sound.putData(buff)

        socket.sendto(f"ACK {ind}".encode(), self.client_address)


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9900

    if SDL_Init(SDL_INIT_AUDIO) != 0:
        raise RuntimeError("Cannot initialize audio system: {}".format(SDL_GetError()))

    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
    server.serve_forever()

    SDL_CloseAudioDevice(sound.devid)
    SDL_Quit(SDL_INIT_AUDIO)

# androidmic
Use your android phone as pulseaudio microphone. Redirects raw audio into a UDP socket on your pc.

## Instructions
* Start `server.py` on your pc
* Start streaming using app to your ip address
* Create a virtual pulseaudio sink and loopback device:

        pactl load-module module-null-sink sink_name=nsink
        pactl load-module module-loopback source=nsink.monitor

* Use pavucontrol to connect server process to the virtual sink


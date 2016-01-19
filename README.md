# androidmic
Use your android phone as pulseaudio microphone. Redirects raw audio into a UDP socket on your pc.

## Instructions
* Start server on your pc
* Run `pactl load-module module-null-sink sink_name=nsink` to create a sink or use pavucontrol
* Start app to stream to your ip

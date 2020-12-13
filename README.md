# HCI_MIDI-keyboard-layouts

Here is our demo video: [![Watch the video](https://i.imgur.com/USGuE1h.png)](https://youtu.be/dWTX7w6zmd4)
 
Get all the supporting libraries. Run the following command:
> pip3 install -r requirements.txt

Run the python communicator 
> python pythonLib/communicate_max.py

How to:
- Even though the python library is meant to serve any application, our current prototype is based on MAX/MSP
- Download Max from here: [https://cycling74.com/downloads](https://cycling74.com/downloads)
- Run the following file in Max/MSP -> MIDI Controller v0.10
- Run the following file in Max/MSP (for two handed keyboard kayout) -> 2 MIDI Controllers v0.11

# Interacting with application
- Have the python communicator running in parallel when interacting with file
> python pythonLib/communicate_max.py
- Click 'Set Key Mapping' to map the green colored keys to the piano
- These green keys are editable
- Transpose and Octave can be changed up by pressing the key, and pressing Shift+key should get them down
- Pitch Bend and Modulation can be changed by pressing the key and moving the mouse/touchpad
- 'Generate MIDI' played a pregenerated midi file, which is generated from a recurrent neural network
- 'Sustain' will hold the pressed keys for longer and is a toggle on the assigned key
- Instrumentation can be change by clicking on them
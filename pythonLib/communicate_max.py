from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import OSCUDPServer

import time
import random
import mido
from midikeyboard import midiKeyboard

def default_handler(address, *args):
    print(f"Unknown Input - {address}: {args}")

def set_keyMappings(address, *args):
    if address.split('/')[-1] == 'keyboard':
        out = keyboard1.setNotesKeys(args[0])
        client_out.send_message("/outputs/key_mappings_spaced", out)
    elif address.split('/')[-1] == 'octave':
        out = keyboard1.setOctaveKey(args[0])
        client_out.send_message("/outputs/transpose", out)
    elif address.split('/')[-1] == 'transpose':
        out = keyboard1.setTransposeKey(args[0])
        client_out.send_message("/outputs/octave", out)
    elif address.split('/')[-1] == 'pitch_bend':
        keyboard1.setPitchKey(args[0])
    elif address.split('/')[-1] == 'modulation':
        keyboard1.setModulationKey(args[0])

def keyOn(address, *args):
    # make the MIDI output to be sent
    out = keyboard1.checkKeyAndCallFunction(args[0], second_key=args[1], key_status='on')
    # send the MIDI output
    if out:
        if len(out)>1:
            client_out.send_message("/outputs/" + out[0], out[1])
        else:
            client_out.send_message("/outputs/key", out[0])


def keyOff(address, *args): 
    # make the MIDI output to be sent
    out = keyboard1.checkKeyAndCallFunction(args[0], second_key=args[1], key_status='off')
    # send the MIDI output
    if out:
        if len(out)>1:
            client_out.send_message("/outputs/" + out[0], out[1])
        else:
            client_out.send_message("/outputs/key", out[0])

def set_genMIDI(address, *args):
    if args[0]==1:
        keyboard1.send_genMIDI(ip, port_out)
    else:
        keyboard1.stop_genMIDI()

# setup the needed keyboards
keyboard1 = midiKeyboard()

# setting the IP to localhost
ip = "127.0.0.1"

# setting the in and out port
port_in = 6450
port_out = 6451

# setting the object which sents messages out
client_out = SimpleUDPClient(ip, port_out)

# setting the object which receives the messages and decides where to send them
dispatcher = Dispatcher()
dispatcher.map("/inputs/key_mapping/*", set_keyMappings)
dispatcher.map("/inputs/key_on/gen_MIDI", set_genMIDI)
dispatcher.map("/inputs/key_on", keyOn)
dispatcher.map("/inputs/key_off", keyOff)
dispatcher.set_default_handler(default_handler)

# starting the server to keep listening for messages
client_in = OSCUDPServer((ip, port_in), dispatcher)
client_in.serve_forever()  # Blocks forever
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import OSCUDPServer

import time
import random
import mido

def default_handler(address, *args):
    print(f"Unknown Input - {address}: {args}")

def set_keyMappings(address, *args):
    # the needed function to set the keys
    return 0

def midi_keyOn(address, *args):
    # make the MIDI output to be sent
    out = [args[0],127]
    # send the MIDI output
    client_out.send_message("/outputs/key", out)


def midi_keyOff(address, *args):
    # make the MIDI output to be sent
    out = [args[0],0]
    # send the MIDI output
    client_out.send_message("/outputs/key", out)

# setting the IP to localhost
ip = "127.0.0.1"

# setting the in and out port
port_in = 6450
port_out = 6451

# setting the object which sents messages out
client_out = SimpleUDPClient(ip, port_out)

# setting the object which receives the messages and decides where to send them
dispatcher = Dispatcher()
dispatcher.map("/inputs/key_mapping", midi_keyOn)
dispatcher.map("/inputs/key_on", midi_keyOn)
dispatcher.map("/inputs/key_off", midi_keyOff)
dispatcher.set_default_handler(default_handler)

# starting the server to keep listening for messages
client_in = OSCUDPServer((ip, port_in), dispatcher)
client_in.serve_forever()  # Blocks forever
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import OSCUDPServer, AsyncIOOSCUDPServer
import asyncio

import time
import random
import mido
from midikeyboard import midiKeyboard

class communicateOSC():

    controller = None
    ip = "127.0.0.1"
    port_in = 6450
    port_out = 6451

    client_in = None
    client_out = None
    transport = None

    @classmethod
    async def create(cls,ip, port_in, port_out):
        self = communicateOSC()
        # setup the needed keyboards
        self.controller = midiKeyboard()

        # setting the IP to localhost
        self.ip = ip

        # setting the in and out port
        self.port_in = port_in
        self.port_out = port_out

        # setting the object which sents messages out
        self.client_out = SimpleUDPClient(self.ip, self.port_out)
        
        # starting the server to keep listening for messages
        # self.client_in = OSCUDPServer((self.ip, self.port_in), self.configureDispatcher())
        # self.client_in.serve_forever()  # Blocks forever

        # trying an async server
        self.client_in = AsyncIOOSCUDPServer((self.ip, self.port_in), self.configureDispatcher(), asyncio.get_event_loop())
        self.transport, protocol = await self.client_in.create_serve_endpoint()  # Create datagram endpoint and start serving

        return self

    def closeNetwork(self):
        self.transport.close()

    def configureDispatcher(self):
        # setting the object which receives the messages and decides where to send them
        dispatcher = Dispatcher()
        dispatcher.map("/inputs/key_mapping/*", self.set_keyMappings)
        dispatcher.map("/inputs/key_on/gen_MIDI", self.set_genMIDI)
        dispatcher.map("/inputs/key_on", self.keyOn)
        dispatcher.map("/inputs/key_off", self.keyOff)
        dispatcher.set_default_handler(self.default_handler)

        return dispatcher

    def default_handler(self,address, *args):
        print(f"Unknown Input - {address}: {args}")

    def set_keyMappings(self,address, *args):
        if address.split('/')[-1] == 'keyboard':
            out = self.controller.setNotesKeys(args[0])
            self.client_out.send_message("/outputs/key_mappings_spaced", out)
        elif address.split('/')[-1] == 'octave':
            out = self.controller.setOctaveKey(args[0])
            self.client_out.send_message("/outputs/octave", out)
        elif address.split('/')[-1] == 'transpose':
            out = self.controller.setTransposeKey(args[0])
            self.client_out.send_message("/outputs/transpose", out)
        elif address.split('/')[-1] == 'pitch_bend':
            self.controller.setPitchKey(args[0])
        elif address.split('/')[-1] == 'modulation':
            self.controller.setModulationKey(args[0])

    def keyOn(self,address, *args):
        # make the MIDI output to be sent
        out = self.controller.checkKeyAndCallFunction(args[0], second_key=args[1], key_status='on')
        # send the MIDI output
        if out:
            if len(out)>1:
                self.client_out.send_message("/outputs/" + out[0], out[1])
            else:
                self.client_out.send_message("/outputs/key", out[0])


    def keyOff(self,address, *args): 
        # make the MIDI output to be sent
        out = self.controller.checkKeyAndCallFunction(args[0], second_key=args[1], key_status='off')
        # send the MIDI output
        if out:
            if len(out)>1:
                self.client_out.send_message("/outputs/" + out[0], out[1])
            else:
                self.client_out.send_message("/outputs/key", out[0])

    def set_genMIDI(self,address, *args):
        if args[0]==1:
            self.controller.send_genMIDI(self.ip, self.port_out)
        else:
            self.controller.stop_genMIDI()

async def init_main():
    
    keyboard1 = await communicateOSC.create('127.0.0.1', 6450, 6451)
    keyboard2 = await communicateOSC.create('127.0.0.1', 6460, 6461)

    while True:
        await asyncio.sleep(1)

    keyboard1.closeNetwork()  # Clean up serve endpoint
    keyboard1.closeNetwork()  # Clean up serve endpoint

asyncio.run(init_main())
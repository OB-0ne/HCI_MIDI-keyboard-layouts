from pythonosc.udp_client import SimpleUDPClient
import pyautogui as py
import time
import random
import mido

from pynput.keyboard import Key, Listener, KeyCode



class midiKeyboard:

    def __init__(self):
        self.octave = {}
        self.dic_ascii = {}
        self.trans = {}
        self.pitch = {}
        self.modulation = {}
        self.oct = 48
        self.transpose = 0
        self.pit = 64
        self.old = 0
        self.modu = 0
        self.gen_MIDI_flag = False
        self.releaseFlagPitch = True
        self.releaseFlagModu = True

    def setIpPort(self,ip, port):
        self.client_ip = ip
        self.client_port = port

    def setTransposeKey(self,   key: str) -> None:
        self.trans = {}
        self.trans[ord(str(key))] = 'trans_inc'

        return self.transpose

    def setOctaveKey(self,  key: str) -> None:
        self.octave = {}
        self.octave[ord(str(key))] = 'oct_inc'

        return "C"+str(int(self.oct/12)-1)

    #Take sequence of characters and update the notes mapping (from 0 to 11)  
    def setNotesKeys(self,  string: str) -> None:
        ascii_list = [ord(s) for s in string]
        self.dic_ascii = {}
        for i,n in enumerate(ascii_list):
            self.dic_ascii[n] = i  

        return [str(x) for x in string]

    def setPitchKey(self, key: str) -> None:
        self.pitch = {}
        self.pitch[ord(str(key))] = 'pitch_inc'  

    def setModulationKey(self, key: str) -> None:
        self.modulation = {}
        self.modulation[ord(str(key))] = 'modu_inc'
       
    #Take the  ASCII value for the keys:('+','-') and update the octet by +12 or -12, respectively
    #And, rotate the value once it crosses the limit: [0,127]
    def updateOctave(self, second_key: int) -> None:
        if second_key == 0:
            self.oct += 12
        elif second_key == 512:
            self.oct -= 12
        self.oct = self.oct % 128 

        return ['octave','C'+str(int(self.oct/12)-1)]

    ##***Put condition for overall self.dic_ascii[n] + self.oct + self.transpose value exceeding 127 or become negative.***
    def updateTranspose(self, second_key: int) -> None:
        if second_key == 0:
            self.transpose += 1
        elif second_key == 512:
            self.transpose -= 1 

        return ['transpose',self.transpose]

    def updatePitch(self, key_status: str) -> int:
        change = 0.4
        if key_status == 'on':
            if self.pit>0 and self.pit<127:
                new = py.position().y
                diff = self.old - new
                self.pit += change*diff
                self.old = new
        elif key_status == 'off':
            self.pit = 64

        return ['pitch_bend',self.pit]

    def updateModulation(self,key_status: str) -> int:
        change = 1
        if key_status == 'on':
            new = py.position().y
            diff = self.old - new
            self.modu += change*diff
            self.old = new

        self.modu = max(self.modu,0)
        self.modu = min(self.modu,127)
        
        return ['modulation',self.modu]

    #Take an Ascii key as an input and returns the Midi input value.
    def keyToMidi(self, key: int, noteStatus: str) -> list:        
        midi_key = (self.dic_ascii[key] + self.oct + self.transpose) % 128        
        if noteStatus == "on":
            vol = 127
        if noteStatus == "off":
            vol = 0   
        return [[midi_key, vol]]

    def send_genMIDI(self, ip, port):

        self.gen_MIDI_flag = True
        client = SimpleUDPClient(ip, port)

        sample_no = random.randint(21,30)
        mid = mido.MidiFile('gen_midi_samples/sample_' + str(sample_no) + '.mid')
        for msg in mid.play():
            if self.gen_MIDI_flag:
                if msg.type == 'note_on':
                    client.send_message("/outputs/gen_MIDI",[msg.note, msg.velocity])
                elif msg.type == 'note_off':
                    client.send_message("/outputs/gen_MIDI",[msg.note, 0])
        for i in range(128):
            client.send_message("/outputs/gen_MIDI",[i, 0])
        return None

    def stop_genMIDI(self):
        self.gen_MIDI_flag = False
        return None

    def on_press(self,key):
        client = SimpleUDPClient(self.client_ip, self.client_port)
        if key == (KeyCode.from_char(chr(list(self.pitch.keys())[0]))):
            out = self.updatePitch(key_status='on')
            client.send_message("/outputs/" + out[0], out[1])  
        elif key == (KeyCode.from_char(chr(list(self.modulation.keys())[0]))):
            out = self.updateModulation(key_status='on')
            client.send_message("/outputs/" + out[0], out[1])  
            
    def on_release(self,key):
        if key == (KeyCode.from_char(chr(list(self.pitch.keys())[0]))):
            self.releaseFlagPitch = True
            return False
        elif key == (KeyCode.from_char(chr(list(self.modulation.keys())[0]))):
            self.releaseFlagModu = True
            return False

    def listenerKB(self):  
        with Listener(on_press=self.on_press, on_release=self.on_release):
            while not self.releaseFlagPitch:
                self.releaseFlagPitch = True
                time.sleep(5)
                pass
            while not self.releaseFlagModu:
                self.releaseFlagModu = True
                time.sleep(5)
                pass
 
  
    def checkKeyAndCallFunction(self, key, second_key='0', key_status='off'):
        if (key in self.octave and key_status=='on'):
            return self.updateOctave(second_key)
        elif (key in self.trans and key_status=='on'):
            return self.updateTranspose(second_key)
        elif (key in self.pitch):
            if key_status == "on":
                self.releaseFlagPitch = False
                self.listenerKB()
            else:
                return self.updatePitch(key_status)
        elif (key in self.modulation):
            if key_status == "on":
                self.releaseFlagModu = False
                self.listenerKB()
            else:
                return self.updateModulation(key_status)
        elif key in self.dic_ascii:
            return self.keyToMidi(key, key_status)
        else:
            return None

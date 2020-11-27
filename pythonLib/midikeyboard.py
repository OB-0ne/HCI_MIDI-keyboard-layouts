import pyautogui as py

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

    def setTransposeKey(self,   key: str) -> None:
        self.trans = {}
        self.trans[ord(key)] = 'trans_inc'

    def setOctaveKey(self,  key: str) -> None:
        self.octave = {}
        self.octave[ord(key)] = 'oct_inc'

    #Take sequence of characters and update the notes mapping (from 0 to 11)  
    def setNotesKeys(self,  string: str) -> None:
        ascii_list = [ord(s) for s in string]
        self.dic_ascii = {}
        for i,n in enumerate(ascii_list):
            self.dic_ascii[n] = i  

    def setPitchKey(self, key: str) -> None:
        self.pitch = {}
        self.pitch[ord(key)] = 'pitch_inc'  

    def setModulationKey(self, key: str) -> None:
        self.modulation = {}
        self.modulation[ord(key)] = 'modu_inc'
       
    #Take the  ASCII value for the keys:('+','-') and update the octet by +12 or -12, respectively
    #And, rotate the value once it crosses the limit: [0,127]
    def updateOctave(self, second_key: int) -> None:
        if second_key == 0:
            self.oct += 12
        elif second_key == 512:
            self.oct -= 12
        self.oct = self.oct % 128 

    ##***Put condition for overall self.dic_ascii[n] + self.oct + self.transpose value exceeding 127 or become negative.***
    def updateTranspose(self, second_key: int) -> None:
        if second_key == 0:
            self.transpose += 1
        elif second_key == 512:
            self.transpose -= 1 

    def updatePitch(self, key_status: str) -> int:
        if key_status == 'on':
            if self.pit>0 and self.pit<127:
                new = py.position().y
                diff = self.old- new
                if diff >0:
                    self.pit +=1
                elif diff <0:
                    self.pit -=1
                self.old = new
        elif key_status == 'off':
            if self.pit>64:
                self.pit -=1
            elif self.pit<64:
                self.pit +=1
        return self.pit   

    def updateModulation(self,key_status: str) -> int:
        if key_status == 'on':
            new = py.position().y
            diff = self.old- new
            if diff >0:
                self.modu +=1
            elif diff <0:
                self.modu -=1
            self.old = new
        if self.modu<0:
            self.modu = 0
        elif self.modu>127:
            self.modu = 127
        return self.modu 

    #Take an Ascii key as an input and returns the Midi input value.
    def keyToMidi(self, key: int, noteStatus: str) -> list:        
        midi_key = (self.dic_ascii[key] + self.oct + self.transpose) % 128        
        if noteStatus == "on":
            vol = 127
        if noteStatus == "off":
            vol = 0   
        return [midi_key, vol]
  
    def checkKeyAndCallFunction(self, key, second_key='0', key_status='off'):
        if (key in self.octave and key_status=='on'):
            self.updateOctave(second_key)
        elif (key in self.trans and key_status=='on'):
            self.updateTranspose(second_key)
        elif (key in self.pitch):
            return self.updatePitch(key_status)
        elif (key in self.modulation):
            return self.updateModulation(key_status)
        elif key in self.dic_ascii:
            return self.keyToMidi(key, key_status)
        else:
            return None

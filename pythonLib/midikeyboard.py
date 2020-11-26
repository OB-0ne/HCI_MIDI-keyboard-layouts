class midiKeyboard:

    def __init__(self):
        self.octave = {}
        self.dic_ascii = {}
        self.trans = {}
        self.oct = 48
        self.transpose = 0
        self.onOrOff = 127

    def setTransposeKey(self,   string: str) -> None:
        self.trans = {}
        self.trans[ord(string[0])] = 'trans_inc'
        self.trans[ord(string[1])] = 'trans_dec'

    def setOctaveKey(self,  string: str) -> None:
        self.octave = {}
        self.octave[ord(string[0])] = 'oct_inc'
        self.octave[ord(string[1])] = 'oct_dec'

    #Take sequence of characters and update the notes mapping (from 0 to 11)  
    def setNotesKeys(self,  string: str) -> None:
        ascii_list = [ord(s) for s in string]
        self.dic_ascii = {}
        for i,n in enumerate(ascii_list):
            self.dic_ascii[n] = i    
       
    #Take the  ASCII value for the keys:('+','-') and update the octet by +12 or -12, respectively
    #And, rotate the value once it crosses the limit: [0,127]
    def updateOctave(self,  string: str) -> None:        
        if string == "oct_inc":
            self.oct = self.oct + 12 if self.oct<116 else 0
        else:
            self.oct = self.oct - 12 if self.oct>11 else 116  

    ##***Put condition for overall self.dic_ascii[n] + self.oct + self.transpose value exceeding 127 or become negative.***
    def updateTranspose(self,   string: str) -> None:
        if string == "trans_inc":
            self.transpose += 1
        else:
            self.transpose -= 1     

    #Take an Ascii key as an input and returns the Midi input value.
    def keyToMidi(self, key: int, noteStatus: str) -> list:
        
        midi_key = (self.dic_ascii[key] + self.oct + self.transpose) % 128
        
        if noteStatus == "on":
            vol = 127
        if noteStatus == "off":
            vol = 0   

        return [midi_key, vol]
  
    def checkKeyAndCallFunction(self, key, key_status='off'):
        if key in self.octave:
            self.updateOctave(self.octave[key])
        elif key in self.trans:
            self.updateTranspose(self.trans[key])
        elif key in self.dic_ascii:
            return self.keyToMidi(key, key_status)
        else:
            return None
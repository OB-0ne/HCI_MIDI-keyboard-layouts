class Midikeyboard:

    def __init__(self):
        self.octave = 48
        self.dic_ascii = {}
    
    #Take the  ASCII value for the keys:('+','-') and update the octet by +12 or -12, respectively
    #And, rotate the value once it crosses the limit: [0,127]
    def SetOctave(self,key:int) -> None:
        if key == 43:
            self.octave = self.octave + 12 if self.octave<116 else 0
        elif  key == 45:
            self.octave = self.octave - 12 if self.octave>11 else 116     

    #Take sequence of characters and update the notes mapping (from 0 to 11)  
    def MapAsciiToNotes(self,string: str) -> None:
        ascii_list = [ord(s) for s in string]
        self.dic_ascii = {}
        for i,n in enumerate(ascii_list):
            self.dic_ascii[n] = i        

    #Take an Ascii key as an input and returns the Midi input value.
    def KeyToMidi(self,key: int) -> list:
        if key in self.dic_ascii:
            return [self.dic_ascii[key] + self.octave,127]
        else:
            return None

obj = Midikeyboard()
obj.MapAsciiToNotes(",;.lkmjnhbg")
obj.SetOctave(ord('+'))
obj.SetOctave(ord('-'))

print(obj.KeyToMidi(ord(",")))

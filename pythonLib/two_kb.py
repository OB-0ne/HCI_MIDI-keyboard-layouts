from midikeyboard import midiKeyboard

obj1 = midiKeyboard()
obj2 = midiKeyboard()
objects = [obj1,obj2]

#Set the keys by passing the strings
obj1.setTransposeKey("")
obj1.setOctaveKey("")
obj1.setNotesKeys("")


def checkKeyAndReturnMIDI(obj,key):
    if key in obj.octave:
        obj.updateOctave(obj.octave[key])
    elif key in obj.trans:
        obj.updateTranspose(obj.trans[key])
    elif key in obj.dic_ascii:
        return [obj.keyToMidi(key),obj.setOnOrOff(key_status)]

def chooseKeyboard(key,key_status: str):
    for obj in objects:
        checkKeyAndReturnMIDI(obj,key,key_status)

        





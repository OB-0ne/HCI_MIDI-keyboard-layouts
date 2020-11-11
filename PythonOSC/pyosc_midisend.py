from pythonosc.udp_client import SimpleUDPClient
# from pythonosc import osc_message_builder
import time
import random
import mido

ip = "127.0.0.1"
port = 6420

client = SimpleUDPClient(ip, port)

mid = mido.MidiFile('sample_02.mid')
for msg in mid.play():
    if msg.type == 'note_on':
        client.send_message("/python_test/",[msg.note, msg.velocity])
    elif msg.type == 'note_off':
        client.send_message("/python_test/",[msg.note, 0])
    
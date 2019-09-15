import rtmidi

midiin=rtmidi.MidiIn()

ports = range(midiin.get_port_count())
if ports:
    for i in ports:
        print(midiin.get_port_name(i))
    midiin.open_port(1)
    while True:
        mess = midiin.get_message() # some timeout in ms
        if mess != None:
            print(mess[0][1])

else:
    print('NO MIDI INPUT PORTS!')
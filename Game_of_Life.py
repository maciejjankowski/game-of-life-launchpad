import rtmidi
import time

def reduce_to_1(num):
    if num >= 1:
        return 1
    else:
        return 0

def light_up(port, position, color):
    port.send_message([
        240, 0, 32, 41, 2, 16, 10,
        position,
        color,
        247]
    )

def print_array(tab, midi_port):
    for i in range(1, len(tab)-1):
        for j in range(1, len(tab[0])-1):
            light_up(midi_port, i*10+j, 0)
    for i in range(1, len(tab)-1):
        print(tab[i])
    print("\n")
    for i in range(1, len(tab)-1):
        for j in range(1, len(tab[0])-1):
            if tab[i][j] >= 1:
                light_up(midi_port, i*10+j, tab[i][j]%127+1)

def count_neighbors(tab, i, j):
    counter=-reduce_to_1(tab[i][j])
    for k in range(i-1, i+2):
        for l in range(j-1, j+2):
            counter+=reduce_to_1(tab[k][l])
    return counter

def new_state(tab, i, j):
    if tab[i][j] >= 1:
        if count_neighbors(tab, i, j) < 2 or count_neighbors(tab, i, j) > 3:
            return 0
        else:
            return tab[i][j]+1
    else:
        if count_neighbors(tab, i, j) == 3:
            return 1
        else:
            return 0
        
def set_array_to_zero(array, n, m):
    for i in range(1, n-1):
        for j in range(1, m-1):
            array[i][j] = 0
    return array

def cycle(board, new_board, n, m):
    for i in range(1, n-1):
        board[0][i]=board[n-2][i]
        board[n-1][i]=board[1][i]
        board[i][0]=board[i][n-2]
        board[i][n-1]=board[i][1]
    board[0][0]=board[n-2][n-2]
    board[n-1][n-1]=board[1][1]
    board[0][n-1]=board[n-2][1]
    board[n-1][0]=board[1][n-2]
    for i in range(1, n-1):
        for j in range(1, m-1):
            new_board[i][j] = new_state(board, i, j)
    return new_board

def swap_arrays(board, new_board):
    for i in range(1, len(board)-1):
            for j in range(1, len(board[0])-1):
                board[i][j] = new_board[i][j]

def tick(board, new_board, midi_port):
    while True:
        new_board = cycle(board, new_board, len(board), len(board[0]))
        swap_arrays(board,new_board)
        new_board = set_array_to_zero(new_board, len(new_board), len(new_board[0]))
        print_array(board, midi_port)
        time.sleep(0.5)
            
def prepare_midi(board, midi_port):
    set_array_to_zero(board, len(board), len(board[0]))
    midiin=rtmidi.MidiIn()
    ports = range(midiin.get_port_count())
    if ports:
        midiin.open_port(1)
        while True:
            mess = midiin.get_message() # some timeout in ms
            if mess != None and mess[0][2]>5:
                print(mess)
                if mess[0][1] == 10 and mess[0][2]>5:
                    midiin.close_port()
                    return board
                else:
                    j=int(mess[0][1]%10)
                    i=int((mess[0][1]-j)/10)
                    if board[i][j]==0:
                        board[i][j]=1
                        light_up(midi_port, i*10+j, 1)
                    else:
                        board[i][j]=0
                        light_up(midi_port, i*10+j, 0)
                    print_array(board, midi_port)

def body():
    mo = rtmidi.MidiOut()
    for port_no in range(mo.get_port_count()):
        port_name = mo.get_port_name(port_no)
        print("MIDI out:", port_name)
        if port_name.find("MIDIOUT2") > -1:
            # or 'Launchpad Pro Standalone Port'
            midi_port = mo.open_port(port_no)

    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    new_board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    board = prepare_midi(board, midi_port)

    tick(board, new_board, midi_port)

def main():
    body()

main()
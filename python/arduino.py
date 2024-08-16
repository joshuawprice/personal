import pyfirmata
import time


board = pyfirmata.Arduino('/dev/ttyACM0')

morse_code = {
    'a': '12',
    'b': '2111',
    'c': '2121',
    'd': '211',
    'e': '1',
    'f': '1121',
    'g': '221',
    'h': '1111',
    'i': '11',
    'j': '1222',
    'k': '212',
    'l': '1211',
    'm': '22',
    'n': '21',
    'o': '222',
    'p': '1221',
    'q': '2212',
    'r': '121',
    's': '111',
    't': '2',
    'u': '112',
    'v': '1112',
    'w': '122',
    'x': '2112',
    'y': '2122',
    'z': '2211',
    '1': '12222',
    '2': '11222',
    '3': '11122',
    '4': '11112',
    '5': '11111',
    '6': '21111',
    '7': '22111',
    '8': '22211',
    '9': '22221',
    '0': '22222',
}

words_per_minute = 20
time_unit = 1200 / words_per_minute / 1000


while True:
    with open('data.txt') as f:
        text = f.read()

    for char in text:
        if char == " ":
            # Assume a previous word has just finished.
            time.sleep(time_unit * 4)
            continue

        if char not in morse_code.keys:
            continue

        print(char, end='')

        for digit in morse_code[char.lower()]:
            board.digital[13].write(1)
            time.sleep(time_unit if digit == 1 else time_unit * 3)
            board.digital[13].write(0)
            time.sleep(time_unit)

        time.sleep(time_unit * 2)

    # Newline before next run through file.
    print()
    time.sleep(5)

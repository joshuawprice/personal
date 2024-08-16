#!/usr/bin/env python3

import string

def main():
    alphabet = string.ascii_lowercase

    shift = int(input("Please enter an amount to shift by: ")) % len(string.ascii_lowercase)
    message = input("Please enter a message: ")

    shifted_alphabet = alphabet[shift:] + alphabet[:shift]

    table = str.maketrans(alphabet, shifted_alphabet)
    table_uppercase = str.maketrans(alphabet.upper(), shifted_alphabet.upper())

    print(message.translate(table).translate(table_uppercase))


if __name__ == "__main__":
    main()

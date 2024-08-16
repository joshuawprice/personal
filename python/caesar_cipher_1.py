#!/usr/bin/env python3


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def new_letter(letter: str, shift_amount: int):
    """Performs a caesar cipher shift on one letter"""
    index = ALPHABET.index(letter)
    return str(ALPHABET[(index + shift_amount) % len(ALPHABET)])


def main():
    shift = int(input("Please enter an amount to shift by: "))
    message = list(input("Please enter a message to shift: "))

    for i, letter in enumerate(message):
        if letter in ALPHABET:
            message.pop(i)
            message.insert(i, new_letter(letter, shift))
        elif letter in ALPHABET.upper():
            message.pop(i)
            message.insert(i, new_letter(letter.lower(), shift).upper())

    print("Output: " + "".join(message))


if __name__ == "__main__":
    main()

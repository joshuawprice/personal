#!/usr/bin/env python3

import string

def main():
    alphabets = string.ascii_lowercase, string.ascii_uppercase

    shift = int(input("Please enter an amount to shift by: ")) % len(string.ascii_lowercase)
    user_message = input("Please enter a message: ")

    shifted_alphabets = map(lambda x: x[shift:] + x[:shift], alphabets)
    table = str.maketrans("".join(alphabets), "".join(shifted_alphabets))

    print(user_message.translate(table))


if __name__ == "__main__":
    main()

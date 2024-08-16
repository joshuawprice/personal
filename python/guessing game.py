#!/usr/bin/env python3

from random import randint

number = randint(1, 100)

while (user_input := int(input("Enter a number between 1 and 100: "))) != number:
    print("Try lower!" if number < user_input else "Try higher!")
print("You got it, well done!")

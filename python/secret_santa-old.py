from random import shuffle


# Names to be paired, these can be changed by hand.
names = [
    "Trudi",
    "Charlotte",
    "Debbie",
    "Val",
    "Fiona B",
    "Trudy (Cook)",
    "Richard",
    "Sarah",
    "Gemma",
    "Fiona W",
]


# Pair names up randomly, ensuring no mutually exclusive name pairs.
# Performed by shuffling the list of names until a derangement is found.
paired_names = names.copy()
is_derangement = False
while not is_derangement:
    shuffle(paired_names)
    # Assume paired_names is a derangement until proven otherwise.
    is_derangement = True
    for name, paired_name in zip(names, paired_names):
        if name == paired_name:
            is_derangement = False
            break

# Save the length of the longest name for formatting later.
longest_name_length = 0
for name in names:
    if len(name) > longest_name_length:
        longest_name_length = len(name)

# Finally, print the paired names.
for name, paired_name in zip(names, paired_names):
    print(name.ljust(longest_name_length), "=", paired_name.rjust(longest_name_length), sep="  ")

# Keep the terminal window open.
while True: input()

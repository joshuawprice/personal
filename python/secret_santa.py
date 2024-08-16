from random import shuffle

# Husthwaite Birthday List

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


# Pair names up randomly, ensuring no matching names.
# Performed by shuffling the list of names until a derangement is found.
paired_names = names.copy()
while any(a == b for a, b in zip(names, paired_names)):
    shuffle(paired_names)

# Print the paired names.
for name, paired_name in zip(names, paired_names):
    print(name.ljust(len(max(names, key=len))), " = ",
          paired_name.rjust(len(max(names, key=len))))

# Keep the terminal window open.
while True:
    input()

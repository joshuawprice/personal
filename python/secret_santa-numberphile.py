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


# Pair names up randomly, ensuring no mutually exclusive name pairs.
# Performed by matching names against a shuffled list with an offset of one.
shuffle(paired_names := names.copy())
paired_names = [paired_names[(paired_names.index(name) + 1) % len(names)]
                for name in names]

# Print the paired names.
for name, paired_name in zip(names, paired_names):
    print(name.ljust(len(max(names, key=len))), " = ",
          paired_name.rjust(len(max(names, key=len))))

# Keep the terminal window open.
while True:
    input()

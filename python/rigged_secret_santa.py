from random import shuffle


# Names to be paired, these can be changed by hand.
names = [
    "Joseph",
    "Jack",
    "Niall",
    "Jamie",
    "Brass",
    "Mills",
    "Nathan",
    "Ken",
    "Jake",
    "Sam",
    "Beak",
    "Will V",
]

mutual_exclusives = [["Beak", "Jake", "Mills", "Ken"],
                     ["Nathan", "Sam"]]

# Pair names up randomly, ensuring no matching names.
# Performed by shuffling the list of names until a derangement is found.
paired_names = names.copy()
while (any(a == b for a, b in zip(names, paired_names))
       or any((a in mutual_exclusives[c % 2])
              and (b in mutual_exclusives[(c + 1) % 2])
              for a, b in zip(names, paired_names)
              for c in range(2))):
    shuffle(paired_names)

# Print the paired names.
for name, paired_name in zip(names, paired_names):
    print(name.ljust(len(max(names, key=len))), " = ",
          paired_name.rjust(len(max(names, key=len))))

# Keep the terminal window open.
while True:
    input()

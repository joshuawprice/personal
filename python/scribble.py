# Word cheat for scribble.io

word_count = input("Enter word count: ")
word_count = word_count.split(" ")

# with open("message.txt") as f:
#     phrases = f.read()

phrases = "Aeon Suit, Antimatter, Armour, Auto Field-Maintenance Unit, Beam Laser, Beluga Liner, Bi-Weave Shield Generator, Black Box, Body Scanner, Bulkheads, Cargo Hatch, Cargo Scanner, Chaff Launcher, Collector Limpet Controller, Collector Limpets, Collision Warning System, Conda, Conductive Limpet Controller, Console, Crop Harvester, Data Link Scanner, Datamined Wake Echoes, Detailed Surface Scanner, Discovery Scanner, Docking Computer, Dolphin, Dolphin Scout, D scanner, Dynamic Resonant Thrusters, Engineered Module, Frame Shift Drive, Frame Shift Drive Interdictor, Fuel Tank, Fuel Transfer Limpet Controller, Fuel Transfer Limpets, Guardian Module, Guardian Shard, Guardian Technology Broker, Heat Sink Launcher, Hull Reinforcement Package, Imperial Cutter, Imperial Eagle, Imperial Hammer, Imperial Navy Rank, Imperial Slave, Imperial Slave Cargo, Interdiction Limpet Controller, Interdiction Limpets, Kill Warrant Scanner, Krait Phantom, Krait Mk II, Laser, Life Support, Light Weight Alloys, Limpet Controller, Limpets, LYR, Main Fuel Tank, Medium Hardpoint, Medium Laser, Medium Shield Booster, Mining Laser, Mining Laser Controller, Mining Limpet Controller, Mining Limpets, Module Storage, Multi-Cannon, Multi-Cruiser Missile Rack, Multi-Purpose Hardpoint, Multi-Warhead Missile Rack, Night Vision, No Fire Zone, Passenger Cabin, Passenger Lounge, Planetary Approach Suite, Planetary Landing Suite, Plasma Accelerator, Power Distributor, Power Plant, Pulse Laser, Rail Gun, Repair Limpet Controller, Repair Limpets, Research limpet controller, Research limpets, Resource Extraction Site, Sidewinder, Sidewinder Scout, Ship Launched Fighter, Ship Scanner, Ship Transfer, Sidewinder, Small Hardpoint, Small Laser, Small Shield Booster, Sol, Solid Fuel Engine, Sothis, Specialised Bulkheads, Surface Scanner, Supercruise Assist, Target Lock, Thargoid Sensors, Thargoid Technology Broker, Thermal Resistant Alloys, Trade Data, Trade Routes, Type-10 Defender, Type-9 Heavy, Type-9 Miner, Type-7 Transporter, Type-6 Transporter, Vulture, Wake Scanner, Weapon Mount, Wireframe Scanner"

for phrase in phrases.split(", "):
    for i, word in enumerate(phrase.split(" ")):
        if (len(phrase.split(" ")) != len(word_count)
                or len(phrase.split(" ")) < len(word_count) < i
                or len(word) != int(word_count[i])):
            break
    else:
        print(phrase)

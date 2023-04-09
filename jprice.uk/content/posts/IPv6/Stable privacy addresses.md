---
title: "Stable Privacy Addresses"
#date: 2023-04-09T00:00:0+00:00
draft: false
aliases: stable privacy address
---

To address privacy issues of [modified EUI-64](../modified-eui-64) addresses, stable privacy addresses were created. These addresses are consistent within a network but change when moving to another network, enhancing privacy. They are chosen randomly yet deterministically from the network's address space.

Stable privacy addresses are generated using a hash function that considers various stable parameters. Although implementations vary, it's advised to use the network prefix, network interface name, a duplicate address counter, and a secret key. The hash value forms the final address, typically combining the least significant 64 bits with the 64-bit network prefix for a 128-bit address. If there's no conflict with existing or reserved addresses, the address is assigned to the interface.

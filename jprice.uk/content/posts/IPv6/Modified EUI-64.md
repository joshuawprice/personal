---
title: "Modified EUI 64"
#date: 2023-04-09T00:00:0+00:00
draft: false
aliases: eui-64
---

Traditionally MAC addresses were used to generate the interface identifier. A 48-bit MAC address is turned into a 64-bit EUI[^1]-64 address by inserting FF-FE in the middle, then the 7th most significant bit is inverted. The bit is inverted to specify that the address is now "universally unique". As compared to normal EUI-64 generation, when this EUI-64 is used to form an [IPv6](../) address, it is modified: the meaning of the Universal/Local bit (the 7th most significant bit of the EUI-64, starting from 1) is inverted, so that a 1 now means Universal.

[^1]: Extended Unique Identifier

## Example

Using the MAC address _00-0C-29-0C-47-D5_, with the network prefix _2001:db8:1:2::/64_:
1. Insert _FF-FE_ into the middle to create the EUI-64 (_00-0C-29-FF-FE-0C-47-D5_)
2. Flip the 7th most significant bit to create the modified EUI-64 (_0**2**-0C-29-FF-FE-0C-47-D5_ the hex character containing the flipped bit has been bolded)
3. Finally prefix it with the network prefix (_2001:db8:1:2:020c:29ff:fe0c:47d5_)

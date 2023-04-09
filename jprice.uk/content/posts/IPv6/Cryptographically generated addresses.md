---
title: "Cryptographically Generated Addresses"
#date: 2023-04-09T00:00:0+00:00
draft: false
aliases: cryptographically generated address
---

A CGA (cryptographically generated address) is created using two hash functions with multiple inputs. The first function uses a public key and a changing random value to obtain a certain number of zero bits in the hash. The second function combines the network prefix and the first hash. The final 128-bit address combines the network prefix with the last 64 bits of the second hash.

These hash functions help confirm if an [IPv6](../) address is a valid CGA, ensuring secure communication between trusted addresses.

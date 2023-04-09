---
title: "Unique Local Addresses"
#date: 2023-04-09T00:00:0+00:00
draft: false
aliases: ula, unique local address
---

Unique local addresses (ULAs) in [IPv6](../) are for local communication, similar to IPv4 private addresses (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16). They can only be routed within cooperating sites. The address block is divided into two parts: the lower half (fc00::/8) is meant for global allocation, but no method has been defined yet; the upper half (fd00::/8) is for "probabilistically unique" addresses. A /48 private prefix is created by combining the /8 prefix with a 40-bit random number, reducing the chance of conflicts when sites merge or communicate. The lower 64 bits are configured using [stateless autoconfiguration](../../ipv6#stateless-autoconfiguration).

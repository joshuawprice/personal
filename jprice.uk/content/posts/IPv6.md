---
title: "IPv6"
#date: 2023-04-09T00:00:0+00:00
draft: false
alias: internet protocol version 6
math: true
---

# IPv6 Addresses

IPv6 addresses are 128 bits long, meaning it can address $2^{128}$ addresses (340,282,366,920,938,463,463,374,607,431,768,211,456).

The first 64 bits of an address are the network prefix, with the remaining 64 bits being the interface identifier.

Written as eight groups of four hexadecimal digits, with colons between them. E.g. _2001:0db8:85a3:0000:0000:8a2e:0370:7334_. The hexadecimal is case insensitive but the IETF recommends using only lowercase letters.

The full representation of an address can be shortened using 2 techniques:
1. Leading zeros are suppressed, with each group containing at least one digit. (E.g. _2001:db8:85a3:0:0:8a2e:370:7334_)
2. The largest run of all zero groups be be compressed to two colons (_::_). If there is a choice, compress the leftmost one. (E.g. _2001:db8:85a3::8a2e:370:7334_)


## Address scopes

There are 2 address scopes:

1. Link-local
2. Global

_Link-local_ scope means they can only be used on a single directly attached network, and _global_ scope means they can be used to connect to addresses with _global_ scope anywhere, or to addresses with _link-local_ scope on the directly attached network. [Link-local addresses](../ipv6/link-local-addresses) and the loopback address have _link-local_ scope. All other addresses have global scope, including perhaps counter-intuitively [unique local addresses](../ipv6/unique-local-addresses).


## Special Addresses

There are a number of addresses with special meaning in IPv6. They represent less than 2% of the entire address space. The full list can be found on [Wikipedia](https://en.wikipedia.org/wiki/IPv6_address#Special_addresses).

| Address block (CIDR)     | First address | Last address                            | Number of addresses | Usage             | Purpose                                                                      |
| ------------------------ | ------------- | --------------------------------------- | ------------------- | ----------------- | ---------------------------------------------------------------------------- |
| ::/0                     | ::            | ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff | $2^{128}$           | Routing           | [Default route](https://en.wikipedia.org/wiki/Default_route "Default route") |
| ::/128                   | ::            | ::                                      | $1$                 | Software          | [Unspecified address](../ipv6/unspecified-address)                                                      |
| ::1/128                  | ::1           | ::1                                     | $1$                 | Host              | [Loopback address](https://en.wikipedia.org/wiki/Loopback_address)           |
| 100::/64                 | 100::         | 100::ffff:ffff:ffff:ffff                | $2^{64}$            | Routing           | Discard prefix                                                               |
| 2001:db8::/32            | 2001:db8::    | 2001:db8:ffff:ffff:ffff:ffff:ffff:ffff  | $2^{96}$            | Documentation     | Addresses used in documentation and example source code                      |
| fc00::/7                 | fc00::        | fdff:ffff:ffff:ffff:ffff:ffff:ffff:ffff | $2^{121}$           | Private internets | [Unique local addresses](../ipv6/unique-local-addresses)                                                     |
| fe80::/64 from fe80::/10 | fe80::        | fe80::ffff:ffff:ffff:ffff               | $2^{64}$            | Link              | [Link-local addresses](../ipv6/link-local-addresses)                                                       |


## Stateless autoconfiguration

Each IPv6 interface is given a [link local address](../ipv6/link-local-addresses). This address is selected with the prefix _fe80::/64_. Then when connecting to a router the router will also provide a network prefix for a globally routable address. The lower 64 bits of these addresses are populated with a 64-bit interface identifier. This should be a pseudo-random number for privacy reasons. The old [modified EUI-64](../ipv6/modified-eui-64) format is now deprecated. Also for privacy reasons, the interface identifier is different for each automatically configured address of that interface.

There are 3 methods for generating pseudo-random numbers for interface identifiers:
1. [Temporary addresses](../ipv6/temporary-addresses)
2. [Cryptographically generated addresses](../ipv6/cryptographically-generated-addresses)
3. [Stable privacy addresses](../ipv6/stable-privacy-addresses)

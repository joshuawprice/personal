---
title: "Link Local Addresses"
#date: 2023-04-09T00:00:0+00:00
draft: false
aliases: link-local address, link local address, link local addresses
---

The link-local prefix (fe80::/10) is valid and unique only on a single link, comparable to IPv4's auto-configuration addresses (169.254.0.0/16). Within this prefix, there's a single subnet (fe80::/64). The last 64 bits are generated using [stateless autoconfiguration](../../ipv6#stateless-autoconfiguration). Every [IPv6](../)-enabled interface must have a link-local address, so applications can rely on its existence even without [IPv6](../) routing.

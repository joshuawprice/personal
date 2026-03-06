resource "cloudflare_dns_record" "asgard" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "asgard.jprice.uk"
  ttl     = 1
  type    = "A"
  content = var.asgard.public_ip
  proxied = false
}

resource "cloudflare_dns_record" "asgard_ipv6" {
  count   = var.asgard.ipv6_address_count
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "asgard.jprice.uk"
  ttl     = 1
  type    = "AAAA"
  content = var.asgard.ipv6_addresses[count.index]
  proxied = false
}

resource "cloudflare_dns_record" "jf_jprice_uk" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "jf.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = cloudflare_dns_record.asgard.name
  proxied = false
}

resource "cloudflare_dns_record" "tr_jprice_uk" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "tr.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = cloudflare_dns_record.asgard.name
  proxied = false
}

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

# Nidavellir's DDNS record
resource "cloudflare_dns_record" "nidavellir" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "nidavellir.jprice.uk"
  ttl     = 1
  type    = "A"
  proxied = false
}

resource "cloudflare_dns_record" "jf" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "jf.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = cloudflare_dns_record.asgard.name
  proxied = false
}

resource "cloudflare_dns_record" "tr" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "tr.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = cloudflare_dns_record.asgard.name
  proxied = false
}

resource "cloudflare_dns_record" "asgard_caa" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = cloudflare_dns_record.asgard.name
  ttl     = 1
  type    = "CAA"
  data = {
    flags = 0
    tag = "issue"
    value = "letsencrypt.org"
  }
  proxied = false
}

resource "cloudflare_dns_record" "bifrost" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "bifrost.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = cloudflare_dns_record.asgard.name
  proxied = false
}

resource "cloudflare_dns_record" "aws_cert" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  comment = "AWS Certificate"
  name    = "_c7de96e04f07abbac80337066d72ed58.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = "_77c7ae59b98da89d92824489c8cdd38b.djqtsrsxkq.acm-validations.aws"
  proxied = false
}

resource "cloudflare_dns_record" "files" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "files.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = "de3ay9npuvp7d.cloudfront.net"
  proxied = false
}

resource "cloudflare_dns_record" "quackathon_2024" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "quack.jprice.uk"
  comment = "Quackathon 2024 Entry"
  ttl     = 1
  type    = "CNAME"
  content = "hsbsea.pages.dev"
  proxied = true
}

resource "cloudflare_dns_record" "test" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "test.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = cloudflare_dns_record.asgard.name
  proxied = false
}

resource "cloudflare_dns_record" "www" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "www.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = "jprice-uk.pages.dev"
  proxied = true
}

resource "cloudflare_dns_record" "apex" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = "www.jprice.uk"
  proxied = true
}

resource "cloudflare_dns_record" "simplelogin_dkim" {
  for_each = toset( ["dkim._domainkey", "dkim02._domainkey", "dkim03._domainkey"] )
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "${each.key}.jprice.uk"
  ttl     = 1
  type    = "CNAME"
  content = "${each.key}.simplelogin.co"
  proxied = false
}

resource "cloudflare_dns_record" "simplelogin_mx" {
  for_each = {
    mx1 = "10"
    mx2 = "20"
  }
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "jprice.uk"
  ttl     = 1
  type    = "MX"
  content = "${each.key}.simplelogin.co"
  priority = each.value
  proxied = false
}

resource "cloudflare_dns_record" "simplelogin_dmarc" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "_dmarc.jprice.uk"
  ttl     = 1
  type    = "TXT"
  content = "\"v=DMARC1; p=quarantine; pct=100; adkim=s; aspf=s\""
  proxied = false
}

resource "cloudflare_dns_record" "simplelogin_spf" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "jprice.uk"
  ttl     = 1
  type    = "TXT"
  content = "\"v=spf1 include:simplelogin.co ~all\""
  proxied = false
}

resource "cloudflare_dns_record" "simplelogin_verification" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "jprice.uk"
  ttl     = 1
  type    = "TXT"
  content = "\"sl-verification=zitxlyudxexnxvbygrdtlrpqkrjonh\""
  proxied = false
}

# Temporary
resource "cloudflare_dns_record" "oldasgard" {
  zone_id = "d4559b15079141dd3ce0f9332a07c571"
  name    = "oldasgard.jprice.uk"
  ttl     = 1
  type    = "A"
  content = "18.130.45.87"
  proxied = false
}

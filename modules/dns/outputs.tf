output "nidavellir_ip_addr" {
  value = cloudflare_dns_record.nidavellir.content
}

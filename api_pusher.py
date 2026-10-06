import requests
from db import get_old_records

# 🔼 PUSH APIs — These are triggered from interface.py on submit
def push_ips(ip_list):
    for ip in ip_list:
        try:
            response = requests.post("http://localhost/api/ip_push", json={"ip": ip})
            print(f"IP PUSH: {ip} → {response.status_code}")
        except Exception as e:
            print(f"Error pushing IP {ip}: {e}")

def push_domains(domain_list):
    for domain in domain_list:
        try:
            response = requests.post("http://localhost/api/domain_push", json={"domain": domain})
            print(f"DOMAIN PUSH: {domain} → {response.status_code}")
        except Exception as e:
            print(f"Error pushing Domain {domain}: {e}")

def push_hashes(hash_list):
    for h in hash_list:
        try:
            response = requests.post("http://localhost/api/hash_push", json={"hash": h})
            print(f"HASH PUSH: {h} → {response.status_code}")
        except Exception as e:
            print(f"Error pushing Hash {h}: {e}")

# 🔽 DELETE APIs — This runs automatically every night at 2 AM via Task Scheduler
def delete_old_from_firewall():
    for table, endpoint in [
        ("ips", "http://localhost/api/ip_delete"),
        ("domains", "http://localhost/api/domain_delete"),
        ("hashes", "http://localhost/api/hash_delete")
    ]:
        try:
            old_data = get_old_records(table)
            for record in old_data:
                value = record[1]  # Assuming 2nd column is value (ip, domain, hash)
                response = requests.post(endpoint, json={"value": value})
                print(f"{table.upper()} DELETE: {value} → {response.status_code}")
        except Exception as e:
            print(f"Error deleting from {table}: {e}")

if __name__ == "__main__":
    delete_old_from_firewall()

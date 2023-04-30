import json, netifaces, socket

with open("constants.json") as f:
    data = json.load(f)

port = data["PORT"]

ips = []
interfaces = netifaces.interfaces()
for intr in interfaces:
    addr = netifaces.ifaddresses(intr)
    if netifaces.AF_INET in addr:
        for a in addr[netifaces.AF_INET]:
            ips.append(a["addr"])

print("Potential ip addresses:")
print(ips)
print("Establishing connection...")
message = bytes(data["MESSAGE"], "utf-8")
for ip in ips:
    addr = (ip, port)
    sock.bind(addr)
    data, address = sock.recvfrom(4096)
    if data == message:
        print(s)
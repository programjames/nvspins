import json, socket, netifaces

with open("constants.json") as f:
    data = json.load(f)

port = data["PORT"]
message = bytes(data["MESSAGE"], "utf-8")

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
for ip in ips:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)  # Set a timeout of 1 second for the socket
    try:
        sock.sendto(message, (ip, port))
        data, address = sock.recvfrom(4096)
        if data == message:
            print("Connection established with:", ip)
            break  # Break out of the loop if connection is successful
    except socket.timeout:
        pass  # Ignore timeout errors and try the next IP address

print("All messages sent.")
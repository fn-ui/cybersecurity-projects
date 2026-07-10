import socket

target = input(
    "Enter IP address to scan: "
)
start_port = int(
    input(
        "Enter starting port: "
    )
)

end_port = int(
    input(
        "Enter ending port: "
    )
)

print("\nScanning ports......\n")
for port in range(
    start_port,
    end_port + 1
     ):

    sock =socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
     )
    sock.settimeout(0.5)


    result = sock.connect_ex(
    (target,port)
     )

    if result == 0 :
        print(
            f"✅ port {port} is open"
            )
    else :
        print(
            f"❌ port {port} is closed"
        )
    sock.close()

print("\nScan complted.")
import socket
import threading
import queue

NUM_THREADS = 50  # Number of threads for concurrent scanning
OUTPUT_FILE = "open_ports.txt"  # Output file to store information about open ports

def port_scan(target_host, port, open_ports):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set socket timeout to 1 second
        result = sock.connect_ex((target_host, port))
        if result == 0:
            print(f"Port {port}: Open")
            open_ports.append(port)  # Collect open port numbers
        sock.close()
    except socket.error:
        pass  # Handle socket errors gracefully (e.g., connection refused)

def get_device_info(target_host):
    try:
        host_name = socket.gethostbyaddr(target_host)[0]
        return host_name
    except socket.herror:
        return "(Unknown)"

def worker(open_ports):
    while True:
        port = port_queue.get()
        port_scan(target_host, port, open_ports)
        port_queue.task_done()

if __name__ == "__main__":
    target_host = input("Enter the target host IP address or domain name: ")
    start_port = int(input("Enter the starting port number: "))
    end_port = int(input("Enter the ending port number: "))

    # Display device info if input is an IP address
    if target_host.replace('.', '').isdigit():  # Check if input is an IP address
        device_name = get_device_info(target_host)
        print(f"Device Name: {device_name}")
        print(f"IP Address: {target_host}")

    open_ports = []

    port_queue = queue.Queue()

    # Create worker threads
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=worker, args=(open_ports,))
        t.daemon = True
        t.start()

    # Enqueue ports to be scanned
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Wait for all tasks to be completed
    port_queue.join()

    # Write information about open ports to output file
    with open(OUTPUT_FILE, "w") as file:
        file.write(f"Device Name: {device_name}\n")
        file.write(f"IP Address: {target_host}\n")
        file.write(f"Open Ports: {' '.join(map(str, open_ports))}\n")

    print(f"Open ports information written to '{OUTPUT_FILE}'")

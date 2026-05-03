import socket
import threading
from queue import Queue

# 配置
TARGET = "127.0.0.1"  # 目标IP，可修改为你要扫描的地址
PORT_RANGE = range(1, 1025)  # 扫描1-1024端口
THREADS = 100  # 线程数，控制扫描速度

# 队列和线程锁
queue = Queue()
open_ports = []
print_lock = threading.Lock()

def port_scan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((TARGET, port))
        if result == 0:
            # 尝试获取服务信息
            try:
                service = socket.getservbyport(port, "tcp")
            except:
                service = "unknown"
            with print_lock:
                print(f"[+] Port {port} is open | Service: {service}")
                open_ports.append((port, service))
        sock.close()
    except Exception as e:
        pass

def threader():
    while True:
        port = queue.get()
        port_scan(port)
        queue.task_done()

def main():
    print(f"Scanning target: {TARGET}")
    print(f"Scanning ports: 1-1024 with {THREADS} threads\n")

    # 启动线程池
    for _ in range(THREADS):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    # 填充端口队列
    for port in PORT_RANGE:
        queue.put(port)

    queue.join()

    print("\nScan complete!")
    if open_ports:
        print("Open ports found:")
        for port, service in open_ports:
            print(f"  - Port {port}: {service}")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
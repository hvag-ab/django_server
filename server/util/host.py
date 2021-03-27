import socket
import platform


def get_host_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip


def get_os_name():
    return platform.system().lower()


host_ip = get_host_ip()
host_os = get_os_name()


def is_dev(ips: [list or str] = None):
    if ips:
        ips = list(ips)
        if host_ip in ips:
            return True
    else:
        if host_os != 'linux':
            return True


if __name__ == '__main__':
    print(get_host_ip())
    print(get_os_name())
    print(is_dev())


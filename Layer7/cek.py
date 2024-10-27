import random
import requests
import threading

def generate_random_proxy():
    ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
    
    proxy_type = random.choice(["http", "https", "socks4", "socks5"])
    
    # Tentukan port yang lebih variatif untuk setiap jenis proxy
    if proxy_type == "http":
        port = random.choice([80, 8080, 3128, 8000, 8888, 8880])
    elif proxy_type == "https":
        port = random.choice([443, 8443, 8442, 9443])
    elif proxy_type == "socks4":
        port = random.choice([1080, 1081, 1082, 9999])
    elif proxy_type == "socks5":
        port = random.choice([1080, 1081, 1082, 9999])
    
    return f"{proxy_type}://{ip}:{port}"

def check_proxy(proxy):
    proxies = {
        "http": proxy,
        "https": proxy,
        "socks4": proxy,
        "socks5": proxy,
    }
    for _ in range(3):  # Retry mechanism
        try:
            response = requests.get("http://www.google.com", proxies={proxy.split('://')[0]: proxy}, timeout=10)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            continue
    return False

def worker(valid_proxies, lock):
    proxy = generate_random_proxy()
    if check_proxy(proxy):
        with lock:
            valid_proxies.append(proxy)
            print(f"Valid proxy found: {proxy}")
    else:
        print(f"Invalid proxy: {proxy}")

def main():
    total_proxies = 1000
    valid_proxies = []
    lock = threading.Lock()

    open("proxy.txt", "w").close()

    threads = []
    for _ in range(total_proxies):
        t = threading.Thread(target=worker, args=(valid_proxies, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if valid_proxies:
        with open("proxy.txt", "w") as file:
            for proxy in valid_proxies:
                file.write(proxy + "\n")

    print(f"\nTotal proxies generated: {total_proxies}")
    print(f"Total valid proxies: {len(valid_proxies)}")

if __name__ == "__main__":
    main()


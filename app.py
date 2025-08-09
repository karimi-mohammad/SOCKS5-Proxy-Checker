import socks
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import threading

PROXY_FILE = "socks5.txt"
LOG_FILE = "checked_proxies.txt"
WORKING_FILE = "working_proxies.txt"
MAX_THREADS = 1500
TIMEOUT = 5

# Lock to prevent race conditions between threads
lock = threading.Lock()
completed_count = 0
total_to_test = 0

def check_socks5(proxy, timeout=5):
    ip, port = proxy.split(":")
    try:
        s = socks.socksocket()
        s.set_proxy(socks.SOCKS5, ip, int(port))
        s.settimeout(timeout)

        start = time.time()
        s.connect(("www.google.com", 80))
        end = time.time()
        s.close()

        ping = (end - start) * 1000  # in milliseconds
        return proxy, True, ping
    except:
        return proxy, False, None

def load_proxies():
    with open(PROXY_FILE, encoding="utf-8") as f:
        all_proxies = {line.strip() for line in f if line.strip()}

    # Remove proxies already logged
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            checked = {line.strip().split()[1] for line in f if line.strip()}
    else:
        checked = set()

    # Exclude proxies that have been tested before
    return sorted(all_proxies - checked)

def save_result(proxy, success, ping=None):
    with lock:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            if success:
                f.write(f"[+] {proxy} ✅ {ping:.2f}ms\n")
            else:
                f.write(f"[-] {proxy} ❌\n")

        if success:
            with open(WORKING_FILE, "a", encoding="utf-8") as wf:
                wf.write(f"{proxy} | {ping:.2f} ms\n")

def main():
    global completed_count, total_to_test

    proxies = load_proxies()
    total_to_test = len(proxies)

    if total_to_test == 0:
        print("✅ All proxies have already been checked or are duplicates.")
        return

    print(f"🔁 Starting to check {total_to_test} proxies... (Press Ctrl+C to stop)")

    try:
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = {executor.submit(check_socks5, proxy): proxy for proxy in proxies}

            for future in as_completed(futures):
                proxy = futures[future]
                success, ping = False, None
                try:
                    proxy, success, ping = future.result()
                except Exception:
                    pass

                # Save result and update counter
                save_result(proxy, success, ping)

                with lock:
                    completed_count += 1
                    status = f"[{completed_count}/{total_to_test}]"

                if success:
                    print(f"{status} [+] ✅ {proxy} | 🕒 {ping:.2f} ms")
                else:
                    print(f"{status} [-] ❌ {proxy} failed")

    except KeyboardInterrupt:
        print("\n⏸️ Checking stopped. Next run will resume from here.")
        return

if __name__ == "__main__":
    main()

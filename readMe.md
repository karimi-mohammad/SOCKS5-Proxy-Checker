
# SOCKS5 Proxy Checker

This is a Python script to check the availability and response time (ping) of SOCKS5 proxies from a list.

## Features

* Loads proxies from `socks5.txt`
* Skips proxies already tested (tracked in `checked_proxies.txt`)
* Checks proxies concurrently with multithreading for speed
* Saves working proxies with their ping to `working_proxies.txt`
* Logs all results in `checked_proxies.txt`
* Handles large proxy lists efficiently

## Requirements

* Python 3.x
* `PySocks` library (install with `pip install pysocks`)

## Usage

1. Put your SOCKS5 proxies (format: `ip:port`) in `socks5.txt`, one per line.
2. Run the script:

   ```bash
   python proxy_checker.py
   ```

3. The script will test each proxy and output progress in the console.
4. Working proxies and their ping times will be saved in `working_proxies.txt`.

## Notes

* Use Ctrl+C to stop the script; it will resume from where it left off next time.
* Adjust `MAX_THREADS` and `TIMEOUT` in the script for performance tuning.

## Disclaimer

This tool is intended for testing SOCKS5 proxies and educational purposes only.
The author is not responsible for any misuse or illegal activities conducted using this software.
Users must comply with all applicable laws and regulations in their country when using this tool.
Do not use this software for unauthorized access, attacks, or any malicious purposes.

---
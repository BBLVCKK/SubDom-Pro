import requests
import sys
import time
import argparse
import threading
from colorama import Fore, Style, init
import os
import random
import subprocess

init(autoreset=True)

discovered_subdomains = []
stop_event = threading.Event()

def Banner():
    tool_name = f"""{Fore.RED}

   _____       _     _____                    _____           
  / ____|     | |   |  __ \                  |  __ \          
 | (___  _   _| |__ | |  | | ___  _ __ ___   | |__) | __ ___  
  \___ \| | | | '_ \| |  | |/ _ \| '_ ` _ \  |  ___/ '__/ _ \ 
  ____) | |_| | |_) | |__| | (_) | | | | | | | |   | | | (_) |
 |_____/ \__,_|_.__/|_____/ \___/|_| |_| |_| |_|   |_|  \___/ 
                                                                                                
    {Style.RESET_ALL}"""
    dev_info = f"""{Fore.GREEN}___ Dev GitHub: BBLVCKK ___{Style.RESET_ALL}"""

    print("\n" + tool_name.center(80))
    print(dev_info.center(80))
    print("\n")

def request(url, timeout):
    try:
        get_response = requests.head("http://" + url, timeout=timeout, allow_redirects=True)
        return get_response
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_status(total_subdomains, checked_subdomains, working_subdomains, color_output):
    clear_screen()
    Banner()
    
    # Print all discovered subdomains
    for subdomain in discovered_subdomains:
        if color_output:
            print(Fore.CYAN + f"{subdomain}")
        else:
            print(subdomain)
            
    # Calculate and print progress
    progress = (checked_subdomains[0] / total_subdomains) * 100
    print(f"\nProgress: {progress:.2f}% ({checked_subdomains[0]}/{total_subdomains} subdomains checked)")
    print(f"Working Subdomains Found: {working_subdomains[0]}")

def progress_updater(total_subdomains, checked_subdomains, working_subdomains, color_output):
    while not stop_event.is_set() and checked_subdomains[0] < total_subdomains:
        print_status(total_subdomains, checked_subdomains, working_subdomains, color_output)
        time.sleep(20)

def calculate_timeout(domain):
    try:
        ping_response = subprocess.run(["ping", "-c", "1", domain], capture_output=True, text=True)
        if ping_response.returncode == 0:
            output_lines = ping_response.stdout.split("\n")
            rtt_line = [line for line in output_lines if "time=" in line]
            print("Determining best time out settings")
            if rtt_line:
                rtt_time = float(rtt_line[0].split("time=")[1].split()[0])
                return rtt_time * 2.5
    except Exception:
        pass
    return 2.5  # Default timeout

def main(target_url, timeout, save_to_file, color_output, wordlist, first_n=None, last_n=None, random_n=None):
    subdomains = []
    
    # Load subdomains from custom wordlist or default wordlist
    wordlist_file = wordlist if wordlist else "domains_list.txt"
    with open(wordlist_file) as wl_file:
        subdomains.extend([line.strip() for line in wl_file])
    
    if first_n:
        subdomains = subdomains[:first_n]
    elif last_n:
        subdomains = subdomains[-last_n:]
    elif random_n:
        subdomains = random.sample(subdomains, random_n)
    
    total_subdomains = len(subdomains)
    checked_subdomains = [0]
    working_subdomains = [0]

    # Start progress thread
    progress_thread = threading.Thread(target=progress_updater, args=(total_subdomains, checked_subdomains, working_subdomains, color_output))
    progress_thread.start()

    try:
        for word in subdomains:
            if stop_event.is_set():
                break
            test_url = word + "." + target_url
            response = request(test_url, timeout)
            
            if response and response.status_code in [200, 301, 302, 304, 307]:
                discovered_subdomains.append(f"{test_url}")
                working_subdomains[0] += 1
            
            checked_subdomains[0] += 1

    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        stop_event.set()
    finally:
        stop_event.set()
        progress_thread.join()
        print_status(total_subdomains, checked_subdomains, working_subdomains, color_output)

        # Save discovered subdomains to a file if specified
        if save_to_file:
            with open(save_to_file, 'w') as f:
                for subdomain in discovered_subdomains:
                    f.write(f"{subdomain}\n")
        
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sub Domains Enumeration Tool")
    parser.add_argument("-d", "--domain", help="Target domain to scan subdomains", required=True)
    parser.add_argument("-t", "--timeout", type=float, help="Set timeout for each request (in seconds). If not provided, it will be calculated dynamically based on the RTT of a ping request.")
    parser.add_argument("-s", "--save", help="Save discovered subdomains to a file.")
    parser.add_argument("-w","--wordlist", help="Provide a custom wordlist file for subdomains.")
    parser.add_argument("-head","--first", type=int, help="Scan the first N subdomains from the wordlist.")
    parser.add_argument("-tail","--last", type=int, help="Scan the last N subdomains from the wordlist.")
    parser.add_argument("--random", type=int, help="Randomly scan N subdomains from the wordlist.")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output.")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    color_output = not args.no_color

    timeout = args.timeout if args.timeout else calculate_timeout(args.domain)

    main(args.domain, timeout, args.save, color_output, args.wordlist, args.first, args.last, args.random)

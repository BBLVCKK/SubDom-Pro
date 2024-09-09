**SubDom Pro: Powerful Subdomain Enumeration Tool**

**Introduction**

SubDom Pro is a Python-based command-line tool designed to efficiently enumerate subdomains for a target domain. It leverages a customizable wordlist or the default `domains_list.txt` file to identify potential subdomains and validates their existence using HTTP requests.

**Key Features**

- **Comprehensive Subdomain Discovery:** Explore a wide range of subdomains using a built-in wordlist or your custom list.
- **Custom Wordlist Support:** Employ your own wordlist containing potential subdomains for tailored enumeration.
- **First/Last N Subdomain Selection:** Scan the first or last N subdomains from your wordlist for targeted exploration.
- **Random Subdomain Selection:** Sample N subdomains from your wordlist for a randomized approach.
- **Dynamic Timeout Calculation (Optional):** Based on the target domain's RTT (round-trip time) estimated through a ping request, SubDom Pro can dynamically adjust the timeout value for each request, optimizing performance. Fixed timeout can also be set manually.
- **Progress Monitoring:** Track scan progress with clear status updates, including the number of checked and working subdomains.
- **Colored Output (Optional):** Enhance readability with color-coded output (can be disabled).
- **Output File Generation (Optional):** Save discovered subdomains to a file for further analysis or reference.

**Installation**

1. **Prerequisites:** Ensure you have Python 3.x([https://www.python.org/](https://www.python.org/)) and pip (Python's package installer) installed on your system.
2. **Clone the Repository:**
   ```bash
   git clone https://github.com/BBLVCKK/SubDom-Pro.git
   ```
3. **Navigate to the Project Directory:**
   ```bash
   cd SubDom-Pro
   ```
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   These dependencies are crucial for making HTTP requests and enhancing output readability, respectively.

**Usage**

Run SubDom Pro from the command line using the following syntax:

```bash
python SubDomsPro.py -d <target_domain> [options]
```

**Required Argument:**

- `-d <target_domain>`: Specify the target domain for which you want to enumerate subdomains.

**Optional Arguments:**

- `-t <timeout>` (float): Set the timeout value (in seconds) for each HTTP request. If not provided, dynamic calculation based on RTT will be used.
- `-s <output_file>`: Save discovered subdomains to the specified file.
- `-w <wordlist>`: Provide a custom wordlist file containing potential subdomains (default: `domains_list.txt`).
- `--first <number>`: Scan the first N subdomains from the wordlist.
- `--last <number>`: Scan the last N subdomains from the wordlist.
- `--random <number>`: Randomly scan N subdomains from the wordlist.
- `--no-color`: Disable colored output.

**Example Usage**

To scan the target domain `example.com` with dynamic timeout calculation, colored output, and saving discovered subdomains to `discovered_subdomains.txt`, use:

```bash
python SubDomsPro.py -d example.com -s discovered_subdomains.txt
```

**Help**

For a detailed list of arguments and usage instructions, run:

```bash
python SubDomsPro.py -h
```

**Contributing**

We welcome contributions to SubDom Pro! If you have improvements or suggestions, feel free to create a pull request on the GitHub repository.

**Disclaimer**

SubDom Pro is intended for educational and ethical purposes only. Do not use this tool for malicious activities or without proper authorization.

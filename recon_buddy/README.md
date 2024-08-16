# Recon Buddy

Recon Buddy is a powerful and flexible reconnaissance tool designed for Capture The Flag (CTF) challenges and ethical hacking practice. It automates various recon tasks to help you gather information about your target quickly and efficiently.

## Features

- Automated Nmap scanning with quick and detailed scan options
- Gobuster directory enumeration for web servers
- Parallel execution of tools for efficiency
- Organized output in a configurable working directory
- Force option to re-run scans and overwrite existing results
- Comprehensive JSON report of all gathered information

## Requirements

- Python 3.6+
- Nmap
- Gobuster
- Terminator

### About Terminator

Terminator is a terminal emulator that allows multiple terminals in a single window. Recon Buddy uses Terminator to launch Gobuster scans in a separate window, allowing you to monitor the progress while the main script continues to run.

### Installing Terminator

To install Terminator, use one of the following commands based on your operating system:

- For Ubuntu/Debian:
  ```
  sudo apt-get install terminator
  ```
- For Fedora:
  ```
  sudo dnf install terminator
  ```
- For Arch Linux:
  ```
  sudo pacman -S terminator
  ```

If your system is not listed here, please refer to the official Terminator documentation for installation instructions.

## Configuration

1. Create a `config.ini` file in the same directory as the script with the following content:
   ```ini
   [DEFAULT]
   WORKING_DIR = /path/to/your/working/directory
   ```
   Replace `/path/to/your/working/directory` with the desired output directory for scan results.

## Usage

Run Recon Buddy using the following command:

```
python recon_buddy.py -i TARGET_IP -n TARGET_HOSTNAME [-f]
```

Arguments:
- `-i`, `--ip`: Target IP address (required)
- `-n`, `--hostname`: Target hostname (required)
- `-f`, `--force`: Force re-run of all tools, overwriting existing results (optional)

Example:
```
python recon_buddy.py -i 192.168.1.100 -n example.com
```

## What Recon Buddy Does

1. Performs a quick Nmap scan of the top 1000 ports on the target.
2. If port 80 or 443 is open, launches a Gobuster scan in a new Terminator window for directory enumeration.
3. Conducts a detailed Nmap scan with version detection and default scripts.
4. Saves all scan results in the configured working directory.
5. Generates a comprehensive `recon_info.json` file containing all gathered information.

## Output Structure

```
WORKING_DIR/
└── TARGET_HOSTNAME/
    ├── nmap_quick_scan_TARGET_IP.nmap
    ├── nmap_quick_scan_TARGET_IP.gnmap
    ├── nmap_quick_scan_TARGET_IP.xml
    ├── nmap_detailed_scan_TARGET_IP.nmap
    ├── nmap_detailed_scan_TARGET_IP.gnmap
    ├── nmap_detailed_scan_TARGET_IP.xml
    ├── TARGET_HOSTNAME_gobuster.txt
    └── recon_info.json
```

The `recon_info.json` file contains a summary of all the reconnaissance information gathered, including open ports, services, and Gobuster results.

## Disclaimer

Recon Buddy is intended for use in authorized testing and CTF environments only. Always ensure you have permission before scanning any targets. The authors are not responsible for any misuse or damage caused by this tool.
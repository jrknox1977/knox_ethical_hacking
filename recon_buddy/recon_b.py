#!/usr/bin/env python3

import argparse
import configparser
import subprocess
import os
import sys
import json
import re
import shutil
from datetime import datetime
import providers
import buddy

def parse_arguments():
    parser = argparse.ArgumentParser(description="CTF Recon Tool")
    parser.add_argument("-i", "--ip", required=True, help="Target IP address")
    parser.add_argument("-n", "--hostname", required=True, help="Target hostname")
    parser.add_argument("-f", "--force", action="store_true", help="Force rerun of all tools")
    return parser.parse_args()

def load_config():
    config = configparser.ConfigParser()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.ini')
    if not os.path.exists(config_path):
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)
    config.read(config_path)
    return config

NMAP_SCANS = {
    "quick_scan": {
        "description": "Quick scan of top 1000 ports",
        "args": ["--top-ports", "1000"]
    },
    "detailed_scan": {
        "description": "Detailed scan with version detection and default scripts",
        "args": ["-sC", "-sV", "--top-ports", "1000"]
    }
}

def parse_nmap_output(output):
    open_ports = {}
    port_pattern = r"^(\d+)/tcp\s+open\s+(\S+)(?:\s+(.+))?$"
    
    for line in output.split('\n'):
        match = re.match(port_pattern, line.strip())
        if match:
            port, service, version = match.groups()
            open_ports[port] = {
                'service': service,
                'version': version if version else 'Unknown'
            }
    
    return open_ports

def run_nmap_scan(ip, output_prefix, scan_type, force=False):
    if scan_type not in NMAP_SCANS:
        print(f"Error: Unknown scan type '{scan_type}'")
        return None, None, f"Unknown scan type: {scan_type}"

    scan_info = NMAP_SCANS[scan_type]
    
    if not force and all(os.path.exists(f"{output_prefix}.{ext}") for ext in ["nmap", "gnmap", "xml"]):
        print(f"Nmap {scan_type} results already exist for {output_prefix}. Skipping scan.")
        with open(f"{output_prefix}.nmap", 'r') as f:
            output = f.read()
        open_ports = parse_nmap_output(output)
        return output, open_ports, None

    nmap_command = ["nmap", "-oA", output_prefix] + scan_info["args"] + [ip]
    
    try:
        print(f"Running Nmap {scan_type}: {' '.join(nmap_command)}")
        result = subprocess.run(nmap_command, check=True, capture_output=True, text=True)
        print(f"Nmap {scan_type} completed. Results saved with prefix: {output_prefix}")
        open_ports = parse_nmap_output(result.stdout)
        return result.stdout, open_ports, None
    except subprocess.CalledProcessError as e:
        print(f"Error running nmap {scan_type}: {e}")
        print("Error output:")
        print(e.stderr)
        return None, None, str(e)

def perform_nmap_scan(ip, hostname, working_dir, scan_type, force=False):
    output_dir = os.path.join(working_dir, hostname)
    os.makedirs(output_dir, exist_ok=True)
    output_prefix = os.path.join(output_dir, f"nmap_{scan_type}_{ip.replace('.', '_')}")
    
    output, open_ports, error = run_nmap_scan(ip, output_prefix, scan_type, force)
    
    scan_info = NMAP_SCANS[scan_type].copy()
    scan_info.update({
        'command': f"nmap {' '.join(NMAP_SCANS[scan_type]['args'])} {ip}",
        'output': output,
        'open_ports': open_ports,
        'error': error,
        'output_files': [f"{output_prefix}.{ext}" for ext in ["nmap", "gnmap", "xml"]]
    })
    
    return scan_info

def save_info_dict(info_dict, output_dir):
    output_file = os.path.join(output_dir, "recon_info.json")
    with open(output_file, 'w') as f:
        json.dump(info_dict, f, indent=4)
    print(f"Reconnaissance information saved to {output_file}")

def check_terminator_installed():
    if shutil.which("terminator") is None:
        print("Terminator is not installed. Gobuster scan will run in the background instead.")
        print("To install Terminator, you can use one of the following commands:")
        print("  For Ubuntu/Debian: sudo apt-get install terminator")
        print("  For Fedora: sudo dnf install terminator")
        print("  For Arch Linux: sudo pacman -S terminator")
        return False
    return True

def launch_gobuster_scan(ip, hostname, working_dir):
    output_dir = os.path.join(working_dir, hostname)
    output_file = os.path.join(output_dir, f"{hostname}_gobuster.txt")
    
    gobuster_command = [
        "gobuster", "dir",
        "-u", f"http://{ip}/",
        "-w", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
        "-x", "php,html,txt",
        "-o", output_file
    ]
    
    if check_terminator_installed():
        # Check if Gobuster is already running in a Terminator window
        ps_command = ["ps", "aux"]
        ps_output = subprocess.check_output(ps_command).decode('utf-8')
        if "terminator" in ps_output and "gobuster" in ps_output:
            print("Gobuster scan is already running in a Terminator window.")
            return

        terminator_command = [
            "terminator",
            "-e", f"bash -c '{' '.join(gobuster_command)}; echo Press Enter to close this window...; read'"
        ]
        try:
            subprocess.Popen(terminator_command)
            print(f"Launched Gobuster scan in a new window. Results will be saved to {output_file}")
        except Exception as e:
            print(f"Error launching Gobuster scan in Terminator: {e}")
            print("Falling back to background execution.")
            launch_gobuster_background(gobuster_command, output_file)
    else:
        launch_gobuster_background(gobuster_command, output_file)

def launch_gobuster_background(gobuster_command, output_file):
    # Check if Gobuster is already running in the background
    ps_command = ["ps", "aux"]
    ps_output = subprocess.check_output(ps_command).decode('utf-8')
    if "gobuster" in ps_output:
        print("Gobuster scan is already running in the background.")
        return

    try:
        subprocess.Popen(gobuster_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Launched Gobuster scan in the background. Results will be saved to {output_file}")
    except Exception as e:
        print(f"Error launching Gobuster scan: {e}")


# If gobuster output exists, grab the output and add it to the info_dict
def check_gobuster_output(target_hostname, working_dir, info_dict):
    gobuster_output_file = os.path.join(working_dir, target_hostname, f"{target_hostname}_gobuster.txt")
    print(f"Checking Gobuster output from {gobuster_output_file}...")
    # Parse the gobuster output file and grab only the URLs that have a status code of 200
    with open(gobuster_output_file, 'r') as f:
        info_dict['gobuster_output'] = []
        for line in f:
            if "(Status: 200)" in line or "(Status: 301)" in line:
                url = line.split(" ")[0]
                info_dict['gobuster_output'].append(url)


def crawl_gobuster_output(target_hostname, working_dir, info_dict):
    info_dict['crawl_results'] = []
    target_ip = info_dict['target_ip']
    output_file = os.path.join(working_dir, target_hostname, f"{target_hostname}_crawl_results.txt")
    
    with open(output_file, 'w') as f:
        for url in info_dict.get('gobuster_output', []):
            full_url = f"http://{target_ip}{url}"
            print(f"Crawling {full_url}...")
            content_file = os.path.join(working_dir, target_hostname, f"{target_hostname}_{url.replace('/', '_')}.html")
            curl_command = ["curl", "-s", "-L", "-o", content_file, "-w", "%{http_code}", full_url]
            try:
                result = subprocess.run(curl_command, check=True, capture_output=True, text=True)
                status_code = result.stdout.strip()
                crawl_result = {
                    'url': full_url,
                    'status_code': status_code,
                    'content_file': content_file
                }
                info_dict['crawl_results'].append(crawl_result)
                f.write(f"{full_url} - Status Code: {status_code} - Content saved to: {content_file}\n")
                print(f"Crawl completed for {full_url} - Status Code: {status_code} - Content saved to: {content_file}")
            except subprocess.CalledProcessError as e:
                print(f"Error crawling {full_url}: {e}")
                error_result = {
                    'url': full_url,
                    'error': str(e)
                }
                info_dict['crawl_results'].append(error_result)
                f.write(f"{full_url} - Error: {str(e)}\n")
    
    print(f"Crawl results saved to {output_file}")
    
    # Save the updated info_dict
    output_dir = os.path.join(working_dir, target_hostname)
    save_info_dict(info_dict, output_dir)


    


def main():
    args = parse_arguments()
    config = load_config()
    
    working_dir = config.get('DEFAULT', 'WORKING_DIR', fallback='.')
    if not os.path.isdir(working_dir):
        print(f"Error: Working directory {working_dir} does not exist.")
        sys.exit(1)
    
    target_ip = args.ip
    target_hostname = args.hostname
    force_rerun = args.force
    
    print("\n" + "="*50)
    print(f"Target IP:          {target_ip}")
    print(f"Target Hostname:    {target_hostname}")
    print(f"Working Directory:  {working_dir}")
    print(f"Force Rerun:        {force_rerun}")
    print("="*50 + "\n")
    
    # Initialize info dictionary
    info_dict = {
        'target_ip': target_ip,
        'target_hostname': target_hostname,
        'recon_date': datetime.now().isoformat(),
        'nmap_scans': {}
    }
    
    # Run quick nmap scan
    print("Starting quick Nmap scan...")
    quick_scan_info = perform_nmap_scan(target_ip, target_hostname, working_dir, "quick_scan", force_rerun)
    info_dict['nmap_scans']['quick_scan'] = quick_scan_info
    
    # Print open ports from quick scan
    print("\nOpen ports from quick scan:")
    for port, info in quick_scan_info['open_ports'].items():
        print(f"Port {port}: {info['service']} ({info['version']})")
    
    # Launch Gobuster if port 80 or 443 is open
    if '80' in quick_scan_info['open_ports'] or '443' in quick_scan_info['open_ports']:
        print("\nLaunching Gobuster scan...")
        launch_gobuster_scan(target_ip, target_hostname, working_dir)
    
    # Run detailed nmap scan
    print("\nStarting detailed Nmap scan...")
    detailed_scan_info = perform_nmap_scan(target_ip, target_hostname, working_dir, "detailed_scan", force_rerun)
    info_dict['nmap_scans']['detailed_scan'] = detailed_scan_info
    
    # Print open ports from detailed scan
    print("\nOpen ports from detailed scan:")
    for port, info in detailed_scan_info['open_ports'].items():
        print(f"Port {port}: {info['service']} ({info['version']})")
    
    # Check gobuster output
    print("\nChecking Gobuster output...")
    check_gobuster_output(target_hostname, working_dir, info_dict)
    
    # Crawl the URLs in the gobuster output and save the response to the working_dir/target_hostname/crawl_gobuster_output.txt
    print("\nCrawling Gobuster output...")
    crawl_gobuster_output(target_hostname, working_dir, info_dict)

    # Get advise from buddy
    advise = buddy.get_advise_from_buddy(info_dict)
    print(f"\nAdvise from buddy: {advise}")

    # Save info_dict to file
    output_dir = os.path.join(working_dir, target_hostname)
    save_info_dict(info_dict, output_dir)

if __name__ == "__main__":
    main()
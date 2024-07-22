# Kali Linux Setup Walkthrough: Installing Cursor, VMware Workstation, and Kali Linux

## Part 1: Installing Cursor

1. Visit the Cursor website: https://cursor.sh/
2. Sign in to create an account
3. Download Cursor
4. Run the installer and follow the installation steps

Note: You can use your own API from OpenAI or Anthropic if you don't want to pay for an account.

## Part 2: Installing VMware Workstation Pro

1. Visit the VMware support website: https://www.vmware.com/support.html
2. Register for an account (if you don't have one)
3. Navigate to the download page for VMware Workstation Pro
4. Select "For Personal Use" option
5. Choose version 17.5.2 (or the latest version available)
6. Agree to the terms and conditions
7. Complete the additional verification (provide address and other required information)
8. Download the installer
9. Run the installer:
   - Click "Next" on the welcome screen
   - Agree to the license terms
   - Choose to install enhanced keyboard drivers
   - Decide whether to add tools to the system PATH
   - Choose whether to create desktop shortcuts
   - Complete the installation and click "Finish"
10. Launch VMware Workstation Pro
11. Pin the application to your taskbar for easy access

## Part 3: Downloading Kali Linux ISO

1. Visit the Kali Linux download page: https://www.kali.org/get-kali/
2. Click on "Recommended" under "Installer Images"
3. Download the 64-bit version (approximately 4GB file)

## Part 4: Creating a Kali Linux VM

1. Open VMware Workstation Pro
2. Click "Create a New Virtual Machine"
3. Choose "Typical" configuration
4. Select the downloaded Kali Linux ISO as the installer disc
5. Choose "Linux" as the guest operating system
6. Select "Debian" as the version (latest version available)
7. Name your virtual machine (e.g., "Kali") and choose a location to store it
8. Set the disk size (recommended: 40GB)
9. Before finishing, click "Customize Hardware":
   - Allocate RAM (recommended: 8GB if available)
   - Set number of processors and cores (e.g., 4 processors, 2 cores each)
10. Click "Finish" to create the VM

## Part 5: Installing Kali Linux

1. Power on the virtual machine
2. Choose "Graphical Install" from the boot menu
3. Follow the installation steps:
   - Choose language, location, and keyboard layout
   - Set a hostname (e.g., "Spectre")
   - Create a user account and set a strong password
   - Configure the time zone
   - Choose disk partitioning (guided - use entire disk)
   - Select desktop environment (KDE Plasma recommended, or XFCE for lower-resource machines)
   - Install GRUB boot loader
4. Reboot the virtual machine
5. Log in to your new Kali Linux system

## Troubleshooting

If you encounter any issues during the installation process, please leave a comment on the video for assistance.
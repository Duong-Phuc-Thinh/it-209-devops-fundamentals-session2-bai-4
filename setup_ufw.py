import subprocess
import sys
import os

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def is_root():
    try:
        return os.getuid() == 0
    except AttributeError:
        return False

def configure_ufw():
    if not is_root():
        print("[-] Error: This script must be run with root/sudo privileges to configure UFW.")
        print("Please re-run with: sudo python3 setup_ufw.py")
        sys.exit(1)

    print("[*] Step 1: Setting default deny incoming...")
    success, out = run_command("ufw --force default deny incoming")
    if not success:
        print(f"[-] Failed to set default incoming rule: {out}")
        sys.exit(1)

    print("[*] Step 2: Setting default allow outgoing...")
    success, out = run_command("ufw --force default allow outgoing")
    if not success:
        print(f"[-] Failed to set default outgoing rule: {out}")
        sys.exit(1)

    print("[*] Step 3: Allowing Port 22/tcp (SSH)...")
    success, out = run_command("ufw allow 22/tcp")
    if not success:
        print(f"[-] Failed to allow port 22/tcp: {out}")
        sys.exit(1)

    print("[*] Step 4: Allowing Port 80/tcp (HTTP)...")
    success, out = run_command("ufw allow 80/tcp")
    if not success:
        print(f"[-] Failed to allow port 80/tcp: {out}")
        sys.exit(1)

    print("[*] Step 5: Enabling UFW...")
    success, out = run_command("ufw --force enable")
    if not success:
        print(f"[-] Failed to enable UFW: {out}")
        sys.exit(1)

    print("\n[+] UFW Configuration Completed Successfully!")
    print("=" * 40)
    print("Current UFW Status Output:")
    print("=" * 40)
    _, status_out = run_command("ufw status verbose")
    print(status_out)

def check_current_status():
    print("[*] Checking current UFW status...")
    if os.name != 'posix':
        print("[-] Non-POSIX system detected. UFW is only available on Linux (Ubuntu).")
        return
    
    success, out = run_command("sudo ufw status verbose")
    if success:
        print(out)
    else:
        print(f"[-] Could not retrieve UFW status: {out}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--status':
        check_current_status()
    else:
        configure_ufw()
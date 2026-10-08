import subprocess


def get_current_user():
    result = subprocess.run(
        ["whoami"],
        capture_output=True,
        text=True
    )

    return result.stdout.strip()

def get_os():
	with open("/etc/os-release", "r") as file:
		for line in file:
			if line.startswith("PRETTY_NAME"):
				return line.split("=")[1].strip().strip("")

def get_kernel():
    result = subprocess.run(
        ["uname", "-r"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def check_firewall():
    result = subprocess.run(
	["sudo", "ufw",  "status"],
		capture_output=True,
		text=True
    )

def check_ssh():
    result = subprocess.run(
        ["dpkg", "-s", "openssh-server"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return True
    else:
        return False

def get_users():
    users = []

    with open("/etc/passwd", "r") as file:
        for line in file:
            parts = line.strip().split(":")

            username = parts[0]
            uid = int(parts[2])

            if uid >= 1000:
                users.append(username)

    return users




print("================================")
print("       LINUX SECURITY AUDIT"   )
print("================================")

user = get_current_user()
os = get_os()
kernel = get_kernel()
firewall = check_firewall()
ssh = check_ssh()
users = get_users()


print(f"Current user: {user}")
print(f"Operating System: {os}")
print(f"Kernel: {kernel}")

if firewall:
    print("[PASS] Firewall is enabled")
else:
    print("[WARN] Firewall is disabled")

if ssh:
    print("[PASS] SSH server is installed")
else:
    print("[INFO] SSH server is not installed")

print("Users: ")
for username in users:
    print(f" - {username}")

print("\nSystem Updates:")

updates = subprocess.run(
	["apt", "list", "--upgradeable"],
	capture_output=True,
	text=True
)

update_lines = updates.stdout.strip().split("\n")

if len(update_lines) > 1:
	update_count = len(update_lines) - 1
	print(f"[WARN] {update_count} system updates are available")
else:
	print("[PASS] system is up to date")

print ("\nDisk Usage:")

disk = subprocess.run(
	["df", "/"],
	capture_output=True,
	text=True
)

disk_lines = disk.stdout.strip().split("\n")
disk_data = disk_lines[1].split()

disk_usage = int(disk_data[4].replace("%", ""))

if disk_usage >= 90:
	print(f"[WARN] Disk usage is {disk_usage}%")
else:
	print(f"[PASS] Disk usage is {disk_usage}%")

print("\nListening Services:")

services = subprocess.run(
    ["ss", "-tuln"],
    capture_output=True,
    text=True
)

service_lines = services.stdout.strip().split("\n")

if len(service_lines) > 1:
    print(f"[INFO] {len(service_lines) - 1} listening network sockets detected")

    for line in service_lines[1:]:
        parts = line.split()

        if len(parts) >= 5:
            address = parts[4]
            print(f" - {address}")

else:
    print("[PASS] No listening network sockets detected")

print("\nFailed Login Attempts:")

failed_logins = subprocess.run(
    ["sudo", "grep", "-c", "Failed password", "/var/log/auth.log"],
    capture_output=True,
    text=True
)

if failed_logins.returncode == 0:
    failed_count = int(failed_logins.stdout.strip())

    if failed_count > 0:
        print(f"[WARN] {failed_count} failed login attempts detected")
    else:
        print("[PASS] No failed login attempts detected")
else:
    print("[INFO] Unable to read authentication log")

print("\nAdministrative Users:")

sudo_users = subprocess.run(
    ["getent", "group", "sudo"],
    capture_output=True,
    text=True
)

if sudo_users.stdout:
    sudo_data = sudo_users.stdout.strip().split(":")
    admin_users = sudo_data[-1].split(",")

    print("[INFO] Users with sudo privileges:")

    for username in admin_users:
        if username:
            print(f" - {username}")
else:
    print("[INFO] No sudo users detected")

print("\n================================")
print("          AUDIT SUMMARY")
print("================================")

warnings = 0
passes = 0
info = 0

if firewall:
    passes += 1
else:
    warnings += 1

if ssh:
    info += 1
else:
    passes += 1

if disk_usage < 90:
    passes += 1
else:
    warnings += 1
if update_count > 0:
    warnings += 1
else:
    passes += 1
if failed_count > 0:
    warnings += 1
else:
    passes += 1

print(f"\nWarnings: {warnings}")
print(f"Passes:   {passes}")
print(f"Info:     {info}")

if warnings == 0:
    print("Security Status: GOOD")
elif warnings <= 2:
    print("Security Status: MODERATE")
else:
    print("Security Status: NEEDS ATTENTION")

score = passes * 20

print(f"Security Score: {score}/100")

from datetime import datetime

report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("audit_report.txt", "w") as report:
    report.write("========================================\n")
    report.write("          LINUX SECURITY AUDIT\n")
    report.write("========================================\n\n")

    report.write(f"Audit Date: {report_time}\n")
    report.write(f"Current User: {user}\n")
    report.write(f"Operating System: {os}\n")
    report.write(f"Kernel: {kernel}\n\n")

    report.write("SECURITY FINDINGS\n")
    report.write("----------------------------------------\n")

    report.write(f"Firewall Enabled: {firewall}\n")
    report.write(f"SSH Installed: {ssh}\n")
    report.write(f"System Updates Available: {update_count}\n")
    report.write(f"Disk Usage: {disk_usage}%\n")
    report.write(f"Failed Login Attempts: {failed_count}\n")
    report.write(f"Administrative Users: {', '.join(admin_users)}\n\n")

    report.write("AUDIT SUMMARY\n")
    report.write("----------------------------------------\n")
    report.write(f"Warnings: {warnings}\n")
    report.write(f"Passes: {passes}\n")
    report.write(f"Info: {info}\n")
    report.write(f"Security Score: {score}/100\n")

    if warnings == 0:
        report.write("Security Status: GOOD\n")
    elif warnings <= 2:
        report.write("Security Status: MODERATE\n")
    else:
        report.write("Security Status: NEEDS ATTENTION\n")

print("\n[INFO] Audit report saved to audit_report.txt")

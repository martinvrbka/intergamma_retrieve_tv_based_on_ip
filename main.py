import paramiko
import os
import csv
import re
import winreg

def retrieve_id_linux(ip, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command("cat ~/.config/teamviewer*/teamviewer*.conf | grep ClientID")
        id = stdout.read().decode("utf-8").strip()
        return id
    except Exception as e:
        return f"Error: {e}"
    finally:
        ssh.close()

def retrieve_id_windows(ip, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command("reg query HKLM\\SOFTWARE\\WOW6432Node\\TeamViewer /v ClientID")
        result = stdout.read().decode("utf-8").strip()
        match = re.search(r"ClientID\s+REG_SZ\s+(\S+)", result)
        if match:
            return match.group(1)
        else:
            return "Error: Unable to retrieve ID"
    except Exception as e:
        return f"Error: {e}"
    finally:
        ssh.close()

def detect_os(ip, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command("uname")
        result = stdout.read().decode("utf-8").strip()
        if result == "Linux":
            return "linux"
        elif result == "Windows":
            return "windows"
        else:
            return "unknown"
    except Exception as e:
        return "error"
    finally:
        ssh.close()

if __name__ == "__main__":
    ips = input("Enter the list of IPs: ").split(", ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    results = []
    for ip in ips:
        os_type = detect_os(ip, username, password)
        if os_type == "linux":
            id = retrieve_id_linux(ip, username, password)
        elif os_type == "windows":
            id = retrieve_id_windows(ip, username, password)
        else:
            id = f"Error: Unable to detect OS ({os_type})"
        results.append([ip, id])
    with open("results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["IP", "TeamViewer ID"])
        for result in results:
            writer.writerow(result)
    print("Results saved to 'results.csv'")
import paramiko
import os
import csv

def retrieve_id(ip, username, password):
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

if __name__ == "__main__":
    ips = input("Enter the list of IPs: ").split(", ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    results = []
    for ip in ips:
        id = retrieve_id(ip, username, password)
        results.append([ip, id])
    with open("results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)
    print("Results saved to results.csv")
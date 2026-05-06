from netmiko import ConnectHandler 
import csv
cmdFile = "cmd.txt"
deviceFile = "device.txt"
outFile = "output.csv"
username= input("Enter username: ")
password = input("Enter Password: ")

#Check cmd execution 
def check_output(output):

    error_patterns = [
        "% Invalid input",
        "% Incomplete command",
        "% Ambiguous command",
        "% Error",
        "^"
    ]

    if any(err in output for err in error_patterns):
        return "FAILURE"
    else:
        return "SUCCESS"
    
with open(deviceFile, "r", encoding="utf-8") as dtxt:
    dlines= dtxt.readlines()
    with open(cmdFile, "r", encoding="utf-8") as ctxt:
        clines= ctxt.readlines()

        # Write each line into a single column in CSV
    # with open(outFile, "w", newline="", encoding="utf-8") as csv_file:
    #     writer = csv.writer(csv_file)
    #     for line in lines:
    #         writer.writerow([line.strip()])  # strip removes newline characters

        for dline in dlines: 
            device = {
                "device_type": "cisco_nxos",   # Change to 'cisco_nxos' for Nexus, etc.
                "host": dline.strip(),        # IP address of the device
                "username": "admin",          # Your username
                "password": password,    # Your password
                "secret": password,  # Optional: enable password
            }
            # Establish SSH connection
            net_connect = ConnectHandler(**device)
            dlineList = []
            for cline in clines: 
                cline = cline.strip()
                if not cline:
                    continue
                output = net_connect.send_command(cline, expect_string=r"#")
                status = check_output(output)
                if status =='SUCCESS':
                    dlineList.append([cline,cline])
                else:
                    dlineList.append([cline,status])
            with open (outFile, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["COMMAND", "STATUS"])
                writer.writerows(dlineList)









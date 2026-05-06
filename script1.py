from netmiko import ConnectHandler
import csv

cmdFile = "cmd.txt"
deviceFile = "device.txt"
outFile = "output.csv"

username = input("Enter username: ")
password = input("Enter Password: ")


# Check cmd execution
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


# Read device list
with open(deviceFile, "r", encoding="utf-8") as dtxt:
    dlines = dtxt.readlines()


# Read command list
with open(cmdFile, "r", encoding="utf-8") as ctxt:
    clines = ctxt.readlines()


# Open CSV once
with open(outFile, "w", newline="", encoding="utf-8") as csv_file:

    writer = csv.writer(csv_file)

    writer.writerow(["COMMAND", "STATUS"])

    # Loop through devices
    for dline in dlines:

        device = {
            "device_type": "cisco_nxos",
            "host": dline.strip(),
            "username": username,
            "password": password,
            "secret": password,
        }

        try:

            # Establish SSH connection
            net_connect = ConnectHandler(**device)

            dlineList = []

            # Loop through commands
            for cline in clines:

                cline = cline.strip()

                if not cline:
                    continue

                output = net_connect.send_command(
                    cline,
                    expect_string=r"#"
                )

                status = check_output(output)

                # If success write command itself
                result = cline if status == "SUCCESS" else "FAILURE"

                dlineList.append([cline, result])

            writer.writerows(dlineList)

            net_connect.disconnect()

        except Exception as e:

            writer.writerow(
                [f"Device {dline.strip()}", f"ERROR: {e}"]
            )

print("Completed")
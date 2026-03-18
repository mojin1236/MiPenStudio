print("Welcome to the BiRelaod bid System")
print("Version 0.1 alpha")

def help_command():
    print("Available commands:")
    print("  exit - Exit the system")
    print("  help - Display help information")
    print("  bid [parameters] - Perform a bid operation")

while True:
    i = input("shell >> ")
    if i == "exit":
        print("Exiting the system...")
        break
    elif i == "help":
        help_command()
    elif len(i) >= 5:
        if i[:3] == "bid":
            a = i.split()
    else:
        print("Invalid command.")

#checks if the file is there and simply prints the data
def read():
    """Read the contents of 'info.txt'."""
    try:
        with open("info.txt", "r") as file:
            content = file.readlines()
        for line in content:
            print(line.strip())
    except FileNotFoundError:
        print("Error: 'info.txt' not found.")
        return []
# Import necessary modules
from read import read
from datetime import datetime
from operation import buy, sell

# Get the current date and time
now = datetime.now()

# Print a welcome message
print("Welcome to the File Based System:")

# Define the available commands and their descriptions
txt = '''
Following are the options for your commands: 
"0" to quit 
"1" to see the current list of available furnitures 
"2" to buy
"3" to sell
"4" to see command
'''

# List of furniture names and command options
names = ["hni corporation", "hni corporationhaworth inc.", "achham furniture", "kimball international inc.", "kohler co.", "masco corporation"]
commands = [0, 1, 2, 3, 4]

# Initialize the main loop control variable
run = True

# Print the basic features and available commands
print(txt)

# Main loop to process user commands0
while run:
    # Get user input and cut any extra whitespace
    inp = input("Enter your command: ").strip()
    
    # Check if the input is a digit
    if inp.isdigit():
        inp = int(inp)
        
        # Check if the input is a valid command
        if inp in commands:
            if inp == 0:
                # Exit the loop if the command is 0
                run = False
            elif inp == 1:
                # Call the read function to display available furniture
                read()
            elif inp == 2:
                # Call the buy function to handle purchasing
                buy()
            elif inp == 3:
                # Call the sell function to handle selling
                sell()
            elif inp == 4:
                # Print the available commands again
                print(txt)
        else:
            # Print an error message for invalid commands
            print("Not a valid command")
    else:
        # Print an error message if the input is not a number
        print("Enter a number")
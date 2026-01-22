# William, a virtual assistant that relies on voice commands to perform tasks in your computer.


# Importing the speech recognition library
import speech_recognition as sr

# Importing os library to clear terminal
import os

# Importing time library for sleep function
import time

# Importing webbrowser library to open websites and search stuff
import webbrowser

# Function to listen for any commands
def listen():
    #Microphone for main computer with headphones pluggedis 1 (Need to check for on laptop)

    # Sets up the micophone
    mic_index = 1  
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=mic_index)

    # Listens for commands
    with mic as source:
        os.system("cls")
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Converts the audio to text
    try:
        command = recognizer.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        print("Didn’t catch that — try again.")
        return listen()

# The open function contains all open commands and their paths.
def open_target(target):

    # Opens youtube
    if "youtube" in target:
        print("Working")
        webbrowser.open("https://www.youtube.com")

    # Opens anime
    elif "anime" in target:
        webbrowser.open("https://hianime.to/home")

    # Opens pinterest
    elif "pinterest" in target:
        webbrowser.open("https://au.pinterest.com")

    # Opens steam
    elif "steam" in target:
        os.startfile(r"C:\Program Files (x86)\Steam\steam.exe")

    # FIX THIS DOES NOT OPEN
    # Opens discord
    elif "discord" in target:
        os.startfile(r"C:\Users\kruge\Desktop\Discord.lnk")
        

    # Tells the user what is being opened and gives time till next command
    print(f"Opening {target}...")
    time.sleep(1.2)
    os.system("cls")

def search_target(target):

    # Search in youtube
    if "youtube" in target:
        target=target.replace("youtube", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={target}")
        

    # Search in youtube
    elif "anime" in target:
        target=target.replace("anime", "").strip()
        webbrowser.open(f"https://hianime.to/search?keyword={target}")

    # Google search
    else:
        target=target.replace("google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={target}")
        

    print(f"Searching for {target}...")

# Startup with seeting variables
language = 'en'
print("William: Starting program...")
os.system("cls")

# Always checking for commands
while True:
    # Any input from the microphone is a command
    command = listen()
    
    # Checks to see if the user wants william to do something
    if "william" in command:

        # Removes will to make it better for the program to understand
        command = command.replace("william", "").strip()

        # Clears the terminal
        os.system("cls")
        
        # This opens up chill with you so it would be easier to work
        if "time to work" in command:
            os.startfile(r"C:\Users\kruge\Documents\Chill.With.You.Lo.Fi.Story.v1.0.10\Chill.With.You.Lo.Fi.Story.v1.0.10\Chill With You.exe")
            print("William: Time to be productive...")

        # If open is in the command it will go to the open function
        elif "open" in command:
            target=command.replace("open", "").strip()
            open_target(target)
        
        # If open is in the command it will go to the open function
        elif "search" in command:
            target=command.replace("search", "").strip()
            search_target(target)
        
        # When user says hello william will reply hello back
        elif command=="hello":
            print("William: Hello!")

        # When user says goodbye william will reply goodbye back
        elif command=="goodbye":
            print("William: Goodbye!")
            exit()

    # If no audio/command is detected         
    elif command == None:
        continue

    # Loops if anything other then a command is given
    else:
        continue 

    # Gives a breather to make it seem more natural and clears the terminal
    time.sleep(0.8)
    os.system("cls")





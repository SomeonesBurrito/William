# William, a virtual assistant that relies on voice commands to perform tasks in your computer.


# Importing the speech recognition library
import speech_recognition as sr

# Importing os library to clear terminal
import os

# Importing time library for sleep function
import time

# Function to listen for any commands
def listen():
    #Microphone for main computer with headphones pluggedis 1 (Need to check for on laptop)

    # Sets up the micophone
    mic_index = 1  
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=mic_index)

    # Listens for commands
    with mic as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Converts the audio to text
    try:
        command = recognizer.recognize_google(audio)
        return command
    except sr.UnknownValueError:
        listen() 

# Startup with seeting variables
language = 'en'
print("William: Starting program...")
os.system("cls")

# Always checking for commands
while True:
    # Any input from the microphone is a command
    command = listen()

    # Clears the terminal
    os.system("cls")

    # When user says hello william will reply hello back
    if command=="hello":
        print("William: Hello!")

    # When user says goodnight william will reply goodnight back
    elif command=="goodbye":
        print("William: Goodbye!")
        exit()
    # Gives a breather to make it seem more natural and clears the terminal
    time.sleep(0.8)
    os.system("cls")





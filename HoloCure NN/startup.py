# import necessary modules
import subprocess
from NNINPUT import get_screen
import numpy as np
import win32api
import win32con
import pyautogui
import time
import random
import pytesseract
import re
from PIL import ImageGrab
def looktime():
    image = ImageGrab.grab()
    # Define the regular expression for the number format you're looking for
    pattern = r'\d{2}:\d{2}'

    # Set the configuration options for Pytesseract
    config = f'--psm 6 --oem 1 -c tessedit_char_whitelist=0123456789:'

    # Apply OCR to the image and extract the text
    text = pytesseract.image_to_string(image, config=config)

    # Search for the pattern in the OCR output
    match = re.search(pattern, text)

    # If a match is found, extract the number
    if match:
        number = match.group(0)
        print(f'Found number: {number}')
        return number
    else:
        print('No matching number found')
# define the neural network
num_inputs = 1080 * 1920 * 3  # number of pixels on screen
num_outputs = 6  # number of possible key press outputs
hidden_layers = [100, 50, 25, 12, 6]  # define the hidden layers

# initialize the weights
weights = []
for i in range(len(hidden_layers) + 1):
    if i == 0:
        weights.append(np.random.randn(num_inputs, hidden_layers[i]))
    elif i == len(hidden_layers):
        weights.append(np.random.randn(hidden_layers[-1], num_outputs))
    else:
        weights.append(np.random.randn(hidden_layers[i - 1], hidden_layers[i]))

def up():
    win32api.keybd_event(0x26, 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(0x26, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.01)
def down():
    win32api.keybd_event(0x28, 0, 0, 0)
    time.sleep(0.01)
    win32api.keybd_event(0x28, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.01)
# define the activation function
def sigmoid(x):
    x = np.clip(x, -500, 500) # clip the input to the sigmoid function
    return 1 / (1 + np.exp(-x))

# define the neural network function
def neural_network(inputs, weights):
    for i in range(len(weights)):
        inputs = sigmoid(np.dot(inputs, weights[i]))
    return inputs

# define the key press outputs
key_codes = {
    "left": 0x25,
    "up": 0x26,
    "right": 0x27,
    "down": 0x28,
    "Z": 0x5A,
    "x": 0x58
}

# define the output function
def output(outputs):
    for i, output in enumerate(outputs):
        if output > 0.5:
            win32api.keybd_event(key_codes[list(key_codes.keys())[i]], 0, 0, 0)
        else:
            win32api.keybd_event(key_codes[list(key_codes.keys())[i]], 0, win32con.KEYEVENTF_KEYUP, 0)

# run the first script
subprocess.run(['python', 'Holocure Detector New.py'])

# call get_screen function and neural network
while True:
    screen = get_screen()

    # check if game over screen has been detected
    if str(screen) == 'GameOver':
        print('Game over')
        # save the weights to file
        with open('best.txt', 'w') as file:
            for i in range(len(weights)):
                np.savetxt(file, weights[i])
            np.savetxt(file, f"time was {looktime()[0,1]}:{looktime()[2,3]}")
        break
    if str(screen) == 'Upgrades':
        if pyautogui.locateOnScreen('templates/findlvlup.png', confidence=.8):
            for i in range(random.randint(1, 100)):
                upordown = random.randint(1, 2)
                if upordown == 1:
                    up()
                else:
                    down()
        win32api.keybd_event(0x5A, 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(0x5A, 0, win32con.KEYEVENTF_KEYUP, 0)
        pass
    else:
        # flatten the screen into an input vector
        inputs = screen.flatten()

        # feed the input vector to the neural network
        outputs = neural_network(inputs, weights)

        # send the outputs to the game through key presses
        output(outputs)
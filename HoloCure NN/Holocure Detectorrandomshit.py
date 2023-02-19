import subprocess
import win32api
import win32con
import pyautogui
import time
import random

# Define key combinations
keys = {
    'up': (0x26, 0),
    'down': (0x28, 0),
    'left': (0x25, 0),
    'right': (0x27, 0),
    'x': (0x58, 0),
    'z': (0x5A, 0)
}

# Define function to press keys
def press_keys(key_list):
    for key in key_list:
        win32api.keybd_event(keys[key][0], 0, keys[key][1], 0)

# Define function to release keys
def release_keys(key_list):
    for key in key_list:
        win32api.keybd_event(keys[key][0], 0, win32con.KEYEVENTF_KEYUP, 0)

# Run the first script
subprocess.run(['python', 'Holocure Detector New.py'])

# Call get_screen function and neural network
while True:
    # Check if game over screen has been detected
    if pyautogui.locateOnScreen('templates/gameover.png', confidence=.8):
        print('Game over')
        break
    if pyautogui.locateOnScreen('templates/up.png', confidence=.8):
        if pyautogui.locateOnScreen('templates/findlvlup.png', confidence=.8):
            for i in range(random.randint(1, 100)):
                key_list = ['up', 'down']
                random.shuffle(key_list)
                press_keys(key_list)
            press_keys(['z'])
        pass
    else:
        # Randomly choose a key combination
        key_combination = random.sample(list(keys.keys()), random.randint(1, len(keys)))

        # Press the key combination
        press_keys(key_combination)

        # Wait for a bit before releasing the key combination
        time.sleep(random.uniform(.001, 2))

        # Release the key combination
        release_keys(key_combination)

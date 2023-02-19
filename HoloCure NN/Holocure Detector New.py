import cv2
import numpy as np
import time
import win32gui
import win32con
import win32api
from PIL import ImageGrab
import threading

# Define the inputs for the mouse_event function
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

def click_button(x, y):
    win32api.SetCursorPos((x, y))
    threading.Timer(0.1, win32api.mouse_event, [win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0]).start()
    threading.Timer(0.1, win32api.mouse_event, [win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0]).start()
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
# Define image templates
play_template = cv2.imread('templates/play_button.png', 0)
question_template = cv2.imread('templates/question_button.png', 0)

# Find window handle for HoloCure
hwnd = win32gui.FindWindow(None, 'HoloCure')

# Unhide the window if it's minimized
if hwnd:
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

# Bring the window to the front
if hwnd:
    win32gui.SetForegroundWindow(hwnd)
else:
    print('HoloCure window not found')
    exit()

# Wait for the window to come to the front
time.sleep(0.3)

# Get the dimensions of the window
window_rect = win32gui.GetWindowRect(hwnd)
x, y, w, h = window_rect

# Take a screenshot of the window and convert to grayscale
screenshot = np.array(ImageGrab.grab(bbox=(x, y, x+w, y+h)))
gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

# Find Play button in screenshot
result = cv2.matchTemplate(gray_screenshot, play_template, cv2.TM_CCOEFF_NORMED)
play_loc = np.where(result >= 0.9)
print(play_loc)
if len(play_loc[0]) > 0:
    print('Play button found!')
    # Move mouse to Play button location
    x_play = play_loc[1][0] + x + 5
    y_play = play_loc[0][0] + y + 5
    print(f'Moving mouse to ({x_play}, {y_play}) and clicking')
    time.sleep(0.1)  # add delay
    click_button(x_play, y_play)
    print("should've clicked")


    # Wait for game to load
    time.sleep(1.5)

    # Find "?" button in screenshot
    screenshot = np.array(ImageGrab.grab(bbox=(x, y, x+w, y+h)))
    gray_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray_screenshot, question_template, cv2.TM_CCOEFF_NORMED)
    question_loc = np.where(result >= 0.9)
    if len(question_loc[0]) > 0:
        print('? button found!')
        x_ques = question_loc[1][0] + x + 5
        y_ques = question_loc[0][0] + y + 5
        click_button(x_ques, y_ques)
        time.sleep(0.1)
        win32api.keybd_event(0x28, 0, 0, 0)  # 0x28 is the virtual key code for the down arrow key
        time.sleep(0.1)
        win32api.keybd_event(0x28, 0, win32con.KEYEVENTF_KEYUP, 0)
        # Press z
        for i in range(4):
            win32api.keybd_event(0x5A, 0, 0, 0)# 0x5A is the virtual key code for the 'z' key
            time.sleep(.1)
            win32api.keybd_event(0x5A, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.1)
    else:
        print('? button not found')
else:
    print('Play button not found')
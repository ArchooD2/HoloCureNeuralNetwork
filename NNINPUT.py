import pyautogui
import numpy as np
from PIL import ImageGrab

# define template images
template1 = 'templates/GameOver.PNG'
template11 = 'templates/GameOver1.PNG'
template111 = 'templates/GameOver2.PNG'
template2 = 'templates/UP.png'

def get_screen():
    # check if game over template 1 is present on the screen
    if pyautogui.locateOnScreen(template1 or template11 or template111) or pyautogui.locateOnScreen(template1) or pyautogui.locateOnScreen(template11) or pyautogui.locateOnScreen(template111) is not None:
        print("gameover should happen now.")
        return 'GameOver'# return GameOver

    # check if game over template 2 is present on the screen
    if pyautogui.locateOnScreen(template2) is not None:
        return 'Upgrades'  # return Upgrades

    # if none of the templates are present, capture the screen and return the image
    screen = ImageGrab.grab()
    screen = np.array(screen)
    return screen

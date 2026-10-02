import pyautogui
import time


def open_application(application_name):
    pyautogui.hotkey("win", "r")
    time.sleep(1)

    pyautogui.write(application_name)
    pyautogui.press("enter")

    time.sleep(2)
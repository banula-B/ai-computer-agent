import pyautogui
import time


def switch_window():
    pyautogui.hotkey("alt", "tab")
    time.sleep(1)
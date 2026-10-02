import pyautogui

from computer.windows import switch_window


def type_text(text):
    switch_window()

    pyautogui.write(text, interval=0.03)

    switch_window()


def press_key(key):
    switch_window()

    pyautogui.press(key)

    switch_window()
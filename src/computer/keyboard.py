import pyautogui


def type_text(text):
    pyautogui.write(text, interval=0.03)


def press_key(key):
    pyautogui.press(key)
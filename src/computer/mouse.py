import pyautogui


def move_mouse(x, y):
    pyautogui.moveTo(x, y, duration=0.5)


def click_mouse():
    pyautogui.click()


def double_click_mouse():
    pyautogui.doubleClick()
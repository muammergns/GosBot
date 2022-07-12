import cv2 as cv
import numpy as np
import pyautogui
import win32con
import win32gui
from tkinter import messagebox

cmp_val = [0.98]
pic_name = ["tap_to_start.png"]
clicking = False
show_window = False
click_pos = (0, 0)
found = False
method_index = [1]
range_count = 1
clicked = False
area_founded = False


def main():
    if pyautogui.size().width != 1920 or pyautogui.size().height != 1080:
        messagebox.showwarning(title="Error", message="Set screen size 1920x1080")
        return
    global found
    global clicked
    global area_founded
    found = False
    clicked = False
    area_founded = False
    win32gui.EnumWindows(callback, None)
    return clicked, area_founded


def callback(hwnd, extra):
    t = win32gui.GetWindowText(hwnd)
    if "BlueStacks App Player" in t:
        global found
        found = True
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        if x >= 0:
            if rect[0] != 1150 or rect[1] != 10:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 1150, 10, 580, 1005, win32con.SWP_SHOWWINDOW)
                win32gui.MoveWindow(hwnd, 1150, 10, 580, 1005, True)
                win32gui.UpdateWindow(hwnd)
            work(rect)
        else:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
            win32gui.UpdateWindow(hwnd)
            print(extra)


def work(rect):
    img_s = pyautogui.screenshot()
    img_k = cv.cvtColor(np.array(img_s), cv.COLOR_RGB2BGR)
    img = img_k  # cv.cvtColor(np.array(img_s), cv.COLOR_RGB2GRAY)
    a = int(rect[0])
    b = int(rect[1])
    c = int(rect[2])
    d = int(rect[3])
    img = img[b:d, a:c]
    img_k = img_k[b:d, a:c]
    for x in range(range_count):
        template = cv.imread("picture\\" + pic_name[x], cv.IMREAD_UNCHANGED)
        shp = template.shape
        methods = [cv.TM_CCOEFF, cv.TM_CCOEFF_NORMED, cv.TM_CCORR,
                   cv.TM_CCORR_NORMED, cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]
        result = cv.matchTemplate(img, template, methods[method_index[x]])
        min_v, max_v, min_l, max_l = cv.minMaxLoc(result)
        if show_window:
            print(pic_name[x] + ": " + str(max_v))
        if max_v > cmp_val[x]:
            global area_founded
            area_founded = True
            global click_pos
            click_pos = (max_l[0] + int(shp[1] / 2) + 4, max_l[1] + int(shp[0] / 2) + 4)
            if clicking:
                global clicked
                clicked = True
                print(str(click_pos))
                current_pos = pyautogui.position()
                pyautogui.moveTo(a + click_pos[0], b + click_pos[1])
                pyautogui.click()
                pyautogui.moveTo(current_pos)
            if show_window:
                rect_end_pos = (max_l[0] + shp[1], max_l[1] + shp[0])
                cv.rectangle(img_k, max_l, rect_end_pos, (0, 255, 0), 2)
                cv.rectangle(img_k, max_l, click_pos, (0, 255, 0), 2)
                cv.imshow("deneme", img_k)
                cv.waitKey(0)
                cv.destroyAllWindows()
            break

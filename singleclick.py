import pyautogui
import keyboard
import tkinter
import threading
import main

w = 30
h = 3
f = 25
quit_task = False
run_conf = False
r_edge = False


def task(lbl: tkinter.Label):
    global run_conf
    global r_edge
    while True:
        if quit_task:
            break
        if keyboard.is_pressed('q') and not r_edge:
            r_edge = True
            run_conf = not run_conf
            lbl.config(text="Running:" + str(run_conf))
        if not keyboard.is_pressed('q'):
            r_edge = False
        if run_conf:
            pyautogui.click()


def quit_module(top: tkinter.Tk):
    global quit_task
    quit_task = True
    top.destroy()
    main.main()


def start_task(tk: tkinter.Tk):
    tk.destroy()
    global quit_task
    global run_conf
    global r_edge
    quit_task = False
    run_conf = False
    r_edge = False
    top = tkinter.Tk()
    top.title("single click")
    tkinter.Label(
        top,
        text="For run/stop click press \"Q\"",
        width=w,
        height=h,
        font=f
    ).pack()
    lbl = tkinter.Label(
        top,
        text="Running: False",
        width=w,
        height=h,
        font=f
    )
    lbl.pack()
    tkinter.Button(
        top,
        text="QUIT",
        command=lambda: quit_module(top),
        width=w,
        height=h,
        font=f
    ).pack()
    threading.Thread(target=task, args=(lbl, )).start()
    top.mainloop()

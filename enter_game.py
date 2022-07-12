import findposition
import tkinter
import threading
import main
from tkinter import messagebox

cmp_vals = (0.7, 0.5, 0.5, 0.61)
pic_names = ("tap_to_start.png", "you_are_offline.png", "close_unused_window.png", "close_unused_window2.png")
methods = (1, 1, 1, 1)
w = 30
h = 3
f = 25
quit_task = False


def task(tk: tkinter.Label):
    while True:
        if quit_task:
            break
        findposition.main()
        if not findposition.found:
            messagebox.showwarning(title="Error", message="Please open BlueStacks App Player")
            tk.config(text="Stopped...")
            break


def quit_module(top: tkinter.Tk):
    global quit_task
    quit_task = True
    top.destroy()
    main.main()


def set_click_var(var: bool):
    findposition.clicking = var


def set_show_var(var: bool):
    findposition.show_window = var


def start_task(tk: tkinter.Tk):
    tk.destroy()
    global quit_task
    quit_task = False
    findposition.clicking = True
    findposition.show_window = False
    findposition.pic_name = pic_names
    findposition.cmp_val = cmp_vals
    findposition.method_index = methods
    findposition.range_count = 4
    top = tkinter.Tk()
    top.title("enter game")
    lbl = tkinter.Label(
        top,
        text="Running...",
        width=w,
        height=h,
        font=f
    )
    lbl.pack()
    click_var = tkinter.BooleanVar()
    click_var.set(True)
    tkinter.Checkbutton(
        top,
        text="Clicking",
        variable=click_var,
        command=lambda: set_click_var(click_var.get()),
        font=f
    ).pack()
    show_var = tkinter.BooleanVar()
    show_var.set(False)
    tkinter.Checkbutton(
        top,
        text="Show test window",
        variable=show_var,
        command=lambda: set_show_var(show_var.get()),
        font=f
    ).pack()
    tkinter.Button(
        top,
        text="QUIT",
        command=lambda: quit_module(top),
        width=w,
        height=h,
        font=f
    ).pack()
    threading.Thread(target=task, args=(lbl,)).start()
    top.mainloop()

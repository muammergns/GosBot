import findposition
import tkinter
import threading
import main
from tkinter import messagebox

cmp_val = [0.88, 0.65]
pic_name = ["gold_chest.png", "gift_given2.png", ]
method_index = [1, 1]
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


def set_gold_chest_var(var):
    findposition.cmp_val[0] = float(var)/100


def start_task(tk: tkinter.Tk):
    tk.destroy()
    global quit_task
    quit_task = False
    findposition.cmp_val = cmp_val
    findposition.pic_name = pic_name
    findposition.method_index = method_index
    findposition.range_count = 2
    findposition.clicking = True
    findposition.show_window = False
    top = tkinter.Tk()
    top.title("pick gold chest")
    sc = tkinter.DoubleVar()
    tkinter.Scale(
        top,
        from_=85,
        to=99,
        command=set_gold_chest_var,
        orient=tkinter.HORIZONTAL,
        variable=sc
    ).pack()
    sc.set(cmp_val[0]*100)
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

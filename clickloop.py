import threading
import pyautogui
import keyboard
import csv
import os
import tkinter
import main
from tkinter import messagebox

header = ['pos_x', 'pos_y']
pos_list = []
w = 30
h = 3
f = 25
new_conf_quit = False
quit_run = False


def new_configuration(top: tkinter.Tk):
    pos_list.clear()
    top.destroy()
    new_conf = tkinter.Tk()
    new_conf.title("new configuration")
    tkinter.Label(
        new_conf,
        text="Enter configuration name",
        width=w,
        height=h,
        font=f
    ).pack()
    txt = tkinter.Text(
        new_conf,
        width=w,
        height=h,
        font=f
    )
    txt.pack()
    btn = tkinter.Button(
        new_conf,
        text="Record",
        command=lambda: threading.Thread(target=new_conf_task, args=(lbl, btn, txt)).start(),
        width=w,
        height=h,
        font=f
    )
    btn.pack()
    tkinter.Button(
        new_conf,
        text="SAVE",
        command=lambda: quit_new_conf(new_conf, True, txt.get(1.0, "end-1c")),
        width=w,
        height=h,
        font=f
    ).pack()
    tkinter.Button(
        new_conf,
        text="QUIT",
        command=lambda: quit_new_conf(new_conf),
        width=w,
        height=h,
        font=f
    ).pack()
    lbl = tkinter.Label(
        new_conf,
        text="For add position press \"Q\"",
        width=w,
        height=h,
        font=f
    )
    lbl.pack()
    new_conf.mainloop()


def new_conf_task(lbl: tkinter.Label, btn: tkinter.Button, txt: tkinter.Text):
    if len(txt.get(1.0, "end-1c")) <= 0:
        messagebox.showwarning(title="Error", message="Name is empty")
        return
    txt.config(state=tkinter.DISABLED)
    btn.config(
        text="Recording",
        state=tkinter.DISABLED
    )
    s_edge = False
    while True:
        if new_conf_quit:
            break
        if keyboard.is_pressed('q') and not s_edge:
            s_edge = True
            position = pyautogui.position()
            pos_dict = {header[0]: int(position[0]), header[1]: int(position[1])}
            pos_list.append(pos_dict)
            lbl.config(text=str(position) + " is added")
        if not keyboard.is_pressed('q'):
            s_edge = False


def quit_new_conf(new_conf: tkinter.Tk, saving=False, name="default"):
    if saving:
        if len(name) <= 0:
            messagebox.showwarning(title="Error", message="Name is empty")
            return
        if len(pos_list) <= 0:
            messagebox.showwarning(title="Error", message="Please add position")
            return
        conf_save(name)
    global new_conf_quit
    new_conf_quit = True
    new_conf.destroy()
    start_task2()


def conf_save(name: str):
    my_path = os.getcwd() + "\\clicks\\"
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    if not os.path.exists(my_path + name + ".csv"):
        my_path = my_path + name + ".csv"
    elif os.path.exists(my_path + name + ".csv"):
        x = 2
        while os.path.exists(my_path + name + str(x) + ".csv"):
            x += 1
        my_path = my_path + name + str(x) + ".csv"
    with open(my_path, 'w', encoding='UTF8', newline='') as my_file:
        writer = csv.DictWriter(my_file, fieldnames=header)
        writer.writeheader()
        writer.writerows(pos_list)
    if os.path.exists(my_path):
        print(name + " created!")
        pos_list.clear()


def read_conf(name: str, list_conf: tkinter.Tk):
    list_conf.destroy()
    my_path = os.getcwd() + "\\clicks\\"
    if os.path.exists(my_path):
        if os.path.exists(my_path + name + ".csv"):
            my_path = my_path + name + ".csv"
            with open(my_path, newline='') as my_file:
                reader = csv.DictReader(my_file, fieldnames=header)
                pos_list.clear()
                first_row = False
                for row in reader:
                    if first_row:
                        pos_list.append([int(row[header[0]]), int(row[header[1]])])
                    else:
                        first_row = True
                run_configuration()


def run_quit(run_tk: tkinter.Tk):
    global quit_run
    quit_run = True
    run_tk.destroy()


def run_configuration():
    if len(pos_list) > 0:
        run_tk = tkinter.Tk()
        run_tk.title("multi click")
        tkinter.Label(
            run_tk,
            text="For run/stop click press \"Q\"",
            width=w,
            height=h,
            font=f
        ).pack()
        lbl = tkinter.Label(
            run_tk,
            text="Running: False",
            width=w,
            height=h,
            font=f
        )
        lbl.pack()
        tkinter.Button(
            run_tk,
            text="QUIT",
            command=lambda: run_quit(run_tk),
            width=w,
            height=h,
            font=f
        ).pack()
        threading.Thread(target=run_task, args=(lbl,)).start()
        run_tk.mainloop()
    else:
        start_task2()


def run_task(lbl: tkinter.Label):
    run_conf = False
    r_edge = False
    step_count = 0
    while True:
        if quit_run:
            break
        if keyboard.is_pressed('q') and not r_edge:
            r_edge = True
            run_conf = not run_conf
            lbl.config(text="Running: " + str(run_conf))
        if not keyboard.is_pressed('q'):
            r_edge = False
        if run_conf:
            pyautogui.moveTo(pos_list[step_count])
            pyautogui.click()
            step_count += 1
            if step_count >= len(pos_list):
                step_count = 0
        else:
            step_count = 0
    start_task2()


def list_quit(list_conf: tkinter.Tk):
    list_conf.destroy()
    start_task2()


def list_configurations(top: tkinter.Tk):
    top.destroy()
    list_conf = tkinter.Tk()
    list_conf.title("Select configuration")
    my_path = os.getcwd() + "\\clicks\\"
    arr = os.listdir(my_path)
    lb = tkinter.Listbox(
        list_conf,
        width=w,
        height=int(w/2),
        font=f
    )
    for x in range(len(arr)):
        lb.insert(x, arr[x].removesuffix(".csv"))
    lb.pack()
    tkinter.Button(
        list_conf,
        text="START",
        command=lambda: read_conf(arr[lb.curselection()[0]].removesuffix(".csv"), list_conf),
        width=w,
        height=h,
        font=f
    ).pack()
    tkinter.Button(
        list_conf,
        text="QUIT",
        command=lambda: list_quit(list_conf),
        width=w,
        height=h,
        font=f
    ).pack()
    list_conf.mainloop()


def task_quit(top: tkinter.Tk):
    top.destroy()
    main.main()


def start_task2():
    global quit_run
    quit_run = False
    global new_conf_quit
    new_conf_quit = False
    top = tkinter.Tk()
    top.title("click loop")
    tkinter.Button(
        top,
        text="new configuration",
        command=lambda: new_configuration(top),
        width=w,
        height=h,
        font=f
    ).pack()
    tkinter.Button(
        top,
        text="run configuration",
        command=lambda: list_configurations(top),
        width=w,
        height=h,
        font=f
    ).pack()
    tkinter.Button(
        top,
        text="QUIT",
        command=lambda: task_quit(top),
        width=w,
        height=h,
        font=f
    ).pack()
    top.mainloop()


def start_task(tk: tkinter.Tk):
    tk.destroy()
    start_task2()

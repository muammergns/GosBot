import pick_gold_chest
import enter_game
import clickloop
import singleclick
import maritimetrade
import tkinter
import dungeondelve


w = 30
h = 3
f = 25


def main():
    top = tkinter.Tk()
    top.title("Welcome to GOS bot")
    tkinter.Button(
        top,
        text="enter game",
        command=lambda: enter_game.start_task(top),
        width=w,
        height=h,
        font=f
    ).pack()
    tkinter.Button(
        top,
        text="pick gold chest",
        command=lambda: pick_gold_chest.start_task(top),
        width=w,
        height=h,
        font=f
    ).pack()
    """
    tkinter.Button(
        top,
        text="maritime trade",
        command=lambda: maritimetrade.start_task(top),
        width=w,
        height=h,
        font=f
    ).pack()
    tkinter.Button(
        top,
        text="dungeon delve",
        command=lambda: dungeondelve.start_task(top),
        width=w,
        height=h,
        font=f
    ).pack()
    """
    tkinter.Button(
        top,
        text="click loop",
        command=lambda: clickloop.start_task(top),
        width=w,
        height=h,
        font=f
    ).pack()
    tkinter.Button(
        top,
        text="single click",
        command=lambda: singleclick.start_task(top),
        width=w,
        height=h,
        font=f
    ).pack()
    tkinter.Button(
        top,
        text="QUIT",
        command=lambda: top.destroy(),
        width=w,
        height=h,
        font=f
    ).pack()
    top.mainloop()


if __name__ == '__main__':
    main()

import winsound
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font

from datetime import datetime, timedelta
import random
import os.path


def add_time(time: int):
    cur_hour = time // 3600
    cur_min = (time // 60) % 60
    cur_sec = time % 60
    cur_time = str(cur_hour).zfill(1) + ":" + str(cur_min).zfill(2) + ":" + str(cur_sec).zfill(2)
    timedisplay0.set(cur_time)


class Timer:
    def __init__(self, target=0):
        self.start_time = None
        self.target = target
        self.is_running = False

    def reset(self):
        self.start_time = None
        self.is_running = False

    def start(self):
        self.is_running = True
        self.start_time = datetime.now()

    def time_left(self):
        cur_time = int((datetime.now() - self.start_time).total_seconds())
        return (self.target * 60) - cur_time

    def check(self):
        if self.time_left() == 0:
            return True
        else:
            return False


def trigger_timer(timer: Timer):
    if timer == timer1 and stopwatch1.is_running:
        tkinter.messagebox.showwarning(title="warning", message="스톱워치가 실행중입니다")
        return
    if timer == timer2 and stopwatch2.is_running:
        tkinter.messagebox.showwarning(title="warning", message="스톱워치가 실행중입니다")
        return
    if timer == timer3 and stopwatch3.is_running:
        tkinter.messagebox.showwarning(title="warning", message="스톱워치가 실행중입니다")
        return
    if not timer.is_running:
        timer.start()
        repeat_timer(timer)
    else:
        cur_time = int((datetime.now()-timer.start_time).total_seconds())
        global added_time
        added_time += cur_time
        add_time(added_time)
        timer.reset()


def repeat_timer(timer: Timer):
    if timer.is_running:
        if timer.check():  # finished
            global added_time
            added_time += (timer.target*60)
            add_time(added_time)
            if timer == timer1:
                timedisplay1.set("END")
            elif timer == timer2:
                timedisplay2.set("END")
            elif timer == timer3:
                timedisplay3.set("END")
            winsound.PlaySound("alarm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            timer.reset()
        else:  # not finished
            time = timer.time_left()
            cur_hour = time // 3600
            cur_min = (time // 60) % 60
            if cur_hour == 0 and cur_min == 0:
                cur_time = str(time).zfill(2)
            else:
                cur_time = str(cur_hour) + ":" + str(cur_min).zfill(2)
            if timer == timer1:
                timedisplay1.set(cur_time)
            elif timer == timer2:
                timedisplay2.set(cur_time)
            elif timer == timer3:
                timedisplay3.set(cur_time)
            window.after(1000, repeat_timer, timer)
    else:
        return


class RepeatTimer:
    def __init__(self, target1=0, target2=0):
        self.start_time = None
        self.target1 = target1
        self.target2 = target2
        self.is_running = False
        self.state = 0

    def reset(self):
        self.start_time = None
        self.state = 0
        self.is_running = False

    def start_first(self):
        self.state = 1
        self.start_time = datetime.now()
        self.is_running = True

    def start_second(self):
        self.state = 2
        self.start_time = datetime.now()
        self.is_running = True


def trigger_repeat(timer: RepeatTimer):
    if timer.state == 0:  # stopped
        timer.start_first()
        check_repeat(timer, timer.target1)
    elif timer.state == 1:  # first target
        window.after_cancel(solve)
        timer.start_second()
        check_repeat(timer, timer.target2)
    elif timer.state == 2:  # second target
        window.after_cancel(solve)
        timer.reset()
        timedisplay4.set("END")


def check_repeat(timer: RepeatTimer, target: int):
    global solve
    if timer.is_running:
        run_time = int((datetime.now() - timer.start_time).total_seconds())
        if target == run_time:  # finished
            winsound.PlaySound("alarm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
            timer.start_time = datetime.now()
            if timer.state == 1:
                timer.start_second()
                solve = window.after(1000, check_repeat, timer, timer.target2)
            elif timer.state == 2:
                timer.start_first()
                solve = window.after(1000, check_repeat, timer, timer.target1)
        else:
            time = target - run_time
            cur_hour = time // 3600
            cur_min = (time // 60) % 60
            if cur_hour == 0 and cur_min == 0:
                cur_time = str(time).zfill(2)
            else:
                cur_time = str(cur_hour) + ":" + str(cur_min).zfill(2)
            timedisplay4.set(cur_time)
            solve = window.after(1000, check_repeat, timer, target)
    else:
        return


class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.run_time = None
        self.is_running = False

    def reset(self):
        self.start_time = None
        self.end_time = None
        self.run_time = None
        self.is_running = False

    def start(self):
        self.reset()
        self.is_running = True
        self.start_time = datetime.now()

    def stop(self):
        self.is_running = False
        self.end_time = datetime.now()
        self.get_time()

    def get_time(self):
        self.run_time = int((self.end_time - self.start_time).total_seconds())

    def cur_time(self):
        cur_run_time = int((datetime.now() - self.start_time).total_seconds())
        time = timedelta(seconds=cur_run_time)
        cur_hour = time.seconds // 3600
        cur_min = (time.seconds // 60) % 60
        cur_time = str(cur_hour) + ":" + str(cur_min).zfill(2)
        return cur_time


def trigger_stopwatch(stopwatch: Stopwatch):
    if stopwatch == stopwatch1 and timer1.is_running:
        tkinter.messagebox.showwarning(title="warning", message="타이머가 실행중입니다")
        return
    if stopwatch == stopwatch2 and timer2.is_running:
        tkinter.messagebox.showwarning(title="warning", message="타이머가 실행중입니다")
        return
    if stopwatch == stopwatch3 and timer3.is_running:
        tkinter.messagebox.showwarning(title="warning", message="타이머가 실행중입니다")
        return
    if not stopwatch.is_running:
        stopwatch.start()
        repeat_stopwatch(stopwatch)
    else:
        stopwatch.stop()


def repeat_stopwatch(stopwatch: Stopwatch):
    if stopwatch.is_running:
        if stopwatch == stopwatch1:
            timedisplay1.set(stopwatch.cur_time())
        elif stopwatch == stopwatch2:
            timedisplay2.set(stopwatch.cur_time())
        elif stopwatch == stopwatch3:
            timedisplay3.set(stopwatch.cur_time())
        window.after(1000, repeat_stopwatch, stopwatch)
    else:
        stopwatch.get_time()
        time = stopwatch.run_time
        cur_hour = time // 3600
        cur_min = (time // 60) % 60
        cur_sec = time % 60
        cur_time = str(cur_hour) + ":" + str(cur_min).zfill(2) + ":" + str(cur_sec).zfill(2)
        global added_time
        added_time += time
        add_time(added_time)
        if stopwatch == stopwatch1:
            timedisplay1.set(cur_time)
        elif stopwatch == stopwatch2:
            timedisplay2.set(cur_time)
        elif stopwatch == stopwatch3:
            timedisplay3.set(cur_time)


def select_file():
    global quest_text
    file_name = "./quest_list.txt"
    if not os.path.isfile(file_name):
        file_name = tkinter.filedialog.askopenfilename(title='quest_list를 선택해주세요', initialdir='.', initialfile="quest_list.txt")

    with open(file_name, 'r', encoding='utf-8') as file:
        quest_text = file.read()
    select_quest()


def select_quest():
    quest_list = quest_text.split('\n')
    quest_list.remove('')
    quest_list.remove('')
    for i in quest_list:
        if i == "* fix":
            mode = 0
        elif i == "* flex":
            mode = 1
        elif i == "* repeat":
            mode = 2
        elif mode == 0:
            if i[0] == 'T':  # Title
                fix_list.append([])
                fix_list[-1].append(i[8:])
            elif i[0] == 'd':  # description
                fix_list[-1].append(i[13:])
            elif i[0] == 't':  # timer
                fix_list[-1].append(i[7:])
        elif mode == 1:
            if i[0] == 'T':  # Title
                flex_list.append([])
                flex_list[-1].append(i[8:])
            elif i[0] == 'd':  # description
                flex_list[-1].append(i[13:])
            elif i[0] == 't':  # timer
                flex_list[-1].append(i[7:])
        elif mode == 2:
            if timer4.target1 == 0:
                timer4.target1 = int(i) * 60
            elif timer4.target2 == 0:
                timer4.target2 = int(i) * 60

    fix_choice = random.choice(fix_list)
    titledisplay1.set(fix_choice[0])
    subtitledisplay1.set(fix_choice[1])
    if fix_choice[2] != ' ':
        timer1.target = int(fix_choice[2])

    flex_choice = random.sample(flex_list, 2)
    titledisplay2.set(flex_choice[0][0])
    subtitledisplay2.set(flex_choice[0][1])
    if flex_choice[0][2] != ' ':
        timer2.target = int(flex_choice[0][2])

    titledisplay3.set(flex_choice[1][0])
    subtitledisplay3.set(flex_choice[1][1])
    if flex_choice[1][2] != ' ':
        timer3.target = int(flex_choice[1][2])


# main window
window = Tk()
window.title("Quest")
window.geometry("450x800+100+100")
window.resizable(False, False)

# menu
menubar = Menu(window)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Reset Quest", command=select_quest)
menu1.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Option")
menubar.add_cascade(label="Option", menu=menu2)

window.config(menu=menubar)

# font
font_32 = tkinter.font.Font(size=32, weight="bold")
font_24 = tkinter.font.Font(size=24, weight="bold")
font_16 = tkinter.font.Font(size=16, weight="bold")
font_bold = tkinter.font.Font(weight="bold")

# string
timedisplay0 = StringVar()
timedisplay0.set("No timer finished")
timedisplay1 = StringVar()
timedisplay1.set("Not Running")
timedisplay2 = StringVar()
timedisplay2.set("Not Running")
timedisplay3 = StringVar()
timedisplay3.set("Not Running")
timedisplay4 = StringVar()
timedisplay4.set("Not running")
titledisplay1 = StringVar()
titledisplay1.set("quest #1")
subtitledisplay1 = StringVar()
subtitledisplay1.set("quest #1")
titledisplay2 = StringVar()
titledisplay2.set("quest #2")
subtitledisplay2 = StringVar()
subtitledisplay2.set("quest #2")
titledisplay3 = StringVar()
titledisplay3.set("quest #3")
subtitledisplay3 = StringVar()
subtitledisplay3.set("quest #3")

# frame
# frame0
frame0 = Frame(window, relief="solid", bd=1)
frame0.pack(fill="both", expand=True)

sum_timer = Label(frame0, textvariable=timedisplay0, font=font_32)
sum_timer.pack()

# frame1
frame1 = Frame(window, relief="solid", bd=1)
frame1.pack(fill="both", expand=True)

frame1_1 = Frame(frame1, relief="solid", bd=1)
frame1_1.pack(side=TOP, fill="both")
time_1 = Label(frame1_1, textvariable=timedisplay1, font=font_24)
time_1.pack(fill="both", expand=True)

frame1_2 = Frame(frame1, relief="solid", bd=1)
frame1_2.pack(side=BOTTOM, fill="both", expand=True)
frame1_2_1 = Frame(frame1_2, relief="solid", bd=1)
frame1_2_1.pack(side=LEFT, fill="both", expand=True)
title_1 = Label(frame1_2_1, textvariable=titledisplay1, font=font_16)
title_1.pack(side=TOP, fill="both", expand=True)
subtitle_1 = Label(frame1_2_1, textvariable=subtitledisplay1, wraplength=300)
subtitle_1.pack(side=BOTTOM, fill="both", expand=True)

frame1_2_2 = Frame(frame1_2, relief="solid", bd=1, padx=10, pady=10)
frame1_2_2.pack(side=RIGHT, fill="both")
timer_1 = Button(frame1_2_2, text="타이머", width=15, height=4, command=lambda: trigger_timer(timer1))
timer_1.pack(side=TOP, fill="x", expand=True)
stopwatch_1 = Button(frame1_2_2, text="스톱워치", width=15, height=4, command=lambda: trigger_stopwatch(stopwatch1))
stopwatch_1.pack(side=BOTTOM, fill="x", expand=True)

# frame2
frame2 = Frame(window, relief="solid", bd=1)
frame2.pack(fill="both", expand=True)

frame2_1 = Frame(frame2, relief="solid", bd=1)
frame2_1.pack(side=TOP, fill="both")
time_2 = Label(frame2_1, textvariable=timedisplay2, font=font_24)
time_2.pack(fill="both", expand=True)

frame2_2 = Frame(frame2, relief="solid", bd=1)
frame2_2.pack(side=BOTTOM, fill="both", expand=True)
frame2_2_1 = Frame(frame2_2, relief="solid", bd=1)
frame2_2_1.pack(side=LEFT, fill="both", expand=True)
title_2 = Label(frame2_2_1, textvariable=titledisplay2, font=font_16)
title_2.pack(side=TOP, fill="both", expand=True)
subtitle_2 = Label(frame2_2_1, textvariable=subtitledisplay2, wraplength=300)
subtitle_2.pack(fill="both", expand=True)

frame2_2_2 = Frame(frame2_2, relief="solid", bd=1, padx=10, pady=10)
frame2_2_2.pack(side=RIGHT, fill="both")
timer_2 = Button(frame2_2_2, text="타이머", width=15, height=4, command=lambda: trigger_timer(timer2))
timer_2.pack(side=TOP, fill="x", expand=True)
stopwatch_2 = Button(frame2_2_2, text="스톱워치", width=15, height=4, command=lambda: trigger_stopwatch(stopwatch2))
stopwatch_2.pack(side=BOTTOM, fill="x", expand=True)

# frame3
frame3 = Frame(window, relief="solid", bd=1)
frame3.pack(fill="both", expand=True)

frame3_1 = Frame(frame3, relief="solid", bd=1)
frame3_1.pack(side=TOP, fill="both")
time_3 = Label(frame3_1, textvariable=timedisplay3, font=font_24)
time_3.pack(fill="both", expand=True)

frame3_2 = Frame(frame3, relief="solid", bd=1)
frame3_2.pack(side=BOTTOM, fill="both", expand=True)
frame3_2_1 = Frame(frame3_2, relief="solid", bd=1)
frame3_2_1.pack(side=LEFT, fill="both", expand=True)
title_3 = Label(frame3_2_1, textvariable=titledisplay3, font=font_16)
title_3.pack(side=TOP, fill="both", expand=True)
subtitle_3 = Label(frame3_2_1, textvariable=subtitledisplay3, wraplength=300)
subtitle_3.pack(side=BOTTOM, fill="both", expand=True)

frame3_2_2 = Frame(frame3_2, relief="solid", bd=1, padx=10, pady=10)
frame3_2_2.pack(side=RIGHT, fill="both")
timer_3 = Button(frame3_2_2, text="타이머", width=15, height=4, command=lambda: trigger_timer(timer3))
timer_3.pack(side=TOP, fill="x", expand=True)
stopwatch_3 = Button(frame3_2_2, text="스톱워치", width=15, height=4, command=lambda: trigger_stopwatch(stopwatch3))
stopwatch_3.pack(side=BOTTOM, fill="x", expand=True)

# frame4
frame4 = Frame(window, relief="solid", bd=1)
frame4.pack(fill="both", expand=True)

frame4_1 = Frame(frame4, relief="solid")
frame4_1.pack(side=LEFT, fill="x", expand=True)
time_4 = Label(frame4_1, textvariable=timedisplay4, font=font_32)
time_4.pack()

frame4_2 = Frame(frame4, relief="solid", bd=1, padx=11, pady=10)
frame4_2.pack(side=RIGHT)
repeat_alarm = Button(frame4_2, text="30/10", width=10, height=4, command=lambda: trigger_repeat(timer4))
repeat_alarm.pack()

# create obj
stopwatch1 = Stopwatch()
stopwatch2 = Stopwatch()
stopwatch3 = Stopwatch()

timer1 = Timer()
timer2 = Timer()
timer3 = Timer()
timer4 = RepeatTimer()

global fix_list
global flex_list
fix_list = []
flex_list = []
added_time = 0

select_file()
# start running
window.mainloop()

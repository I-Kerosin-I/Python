import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import turtle as tur
from random import random, randint, uniform
from colorsys import hsv_to_rgb


def v_shape(turtl, config: dict):
    turtl.right(config['angle'] / 2)
    turtl.forward(config['v_length'])
    turtl.back(config['v_length'])
    turtl.left(config['angle'])
    turtl.forward(config['v_length'])
    turtl.back(config['v_length'])
    turtl.right(config['angle'] / 2)


def snowflake_arm(turtl, config: dict):
    for i in range(config['v_amount']):
        turtl.forward(config['arm_length'] / config['v_amount'])
        v_shape(turtl, config)
    turtl.back(config['arm_length'])
    screen.update()


def snowflake(turtl, config: dict):
    for i in range(config['arm_amount']):
        snowflake_arm(turtl, config)
        turtl.right(360 / config['arm_amount'])


def start():
    global stopped
    starter.start_btn.config(state='disabled')
    canvas_clear_btn.config(state='disabled')
    starter.stop_btn.config(state='normal')
    for i in range(starter.main_var.get()):
        if color.is_rand.get():
            turtle.color(color.get_color())
        else:
            try:
                turtle.color(color.get_color())
            except tur.TurtleGraphicsError:
                mb.showerror('Bad color', 'Invalid color string!\n'
                                          'Use "#RRGGBB" syntax')
                break

        turtle.pensize(pensize.get_main_var())
        snow_config['arm_amount'] = arm_amount.get_main_var()
        snow_config['arm_length'] = arm_length.get_main_var()
        snow_config['v_amount'] = v_amount.get_main_var()
        snow_config['v_length'] = v_length.get_main_var()
        snow_config['angle'] = ange.get_main_var()

        snowflake(turtle, snow_config)
        randomize_pos(turtle)
        if stopped:
            if not starter.bool_var.get():
                screen.tracer(1, 1)
            stopped = False
            break
    screen.update()
    starter.start_btn.config(state='normal')
    canvas_clear_btn.config(state='normal')
    starter.stop_btn.config(state='disabled')


def randomize_pos(turtl):
    x = canvas.winfo_width()
    y = canvas.winfo_height()
    turtl.up()
    turtl.goto(randint(-658, x - 718), randint(391 - y, 330))
    turtl.down()


def randomize_config():
    color.randomize()
    pensize.randomize()
    arm_amount.randomize()
    arm_length.randomize()
    v_amount.randomize()
    v_length.randomize()
    ange.randomize()


class ScaleWithEntry(tk.LabelFrame):
    def __init__(self, master, label_text, from_, to):
        super().__init__(master, text=label_text, bg='#333333',
                         fg='white', padx=7, pady=3)

        self.from_ = from_
        self.to = to
        self.v_cmd = (self.register(self.on_validate), '%S', '%P')
        self.bool_var = tk.BooleanVar()
        self.main_var = tk.IntVar()
        self.entry = ttk.Entry(self, width=5, textvariable=self.main_var,
                               validate='key', validatecommand=self.v_cmd)
        self.scale = ttk.Scale(self, from_=from_, to=to, command=lambda x:
                               self.main_var.set(round(float(x))))

        self.check_btn = ttk.Checkbutton(self, text='Random', onvalue=True,
                                         variable=self.bool_var, offvalue=False,
                                         command=self.disabler, takefocus=False)

        self.main_var.set(from_)

    def on_validate(self, s, p):
        for i in s:
            if i not in '0123456789':
                return False
        if p != '':
            self.scale.config(value=p)
        return True

    def disabler(self):
        if self.bool_var.get():
            self.entry.config(state='readonly')
            self.scale.config(state='disabled')
        else:
            self.entry.config(state='normal')
            self.scale.config(state='normal')

    def toggle(self, val):
        self.bool_var.set(val)
        self.disabler()

    def randomize(self):
        self.main_var.set(randint(self.from_, self.to))
        self.scale.config(value=self.main_var.get())

    def get_main_var(self):
        if self.bool_var.get():
            self.randomize()
            return self.main_var.get()
        else:
            return self.main_var.get()

    def draw(self, **kwargs):
        self.grid(kwargs, columnspan=2, sticky='nsew')
        self.entry.grid(column=0, row=0, padx=7)
        self.scale.grid(column=1, row=0)
        self.check_btn.grid(columnspan=2, sticky='e')


class StartWidget(ScaleWithEntry):
    def __init__(self, master, label_text, from_, to):
        super().__init__(master, label_text, from_, to)
        self.check_btn = ttk.Checkbutton(self, text='TURBO', onvalue=True,
                                         variable=self.bool_var, offvalue=False,
                                         command=self.turbo, takefocus=False)
        self.start_btn = tk.Button(master, bg='#222222', text='START',
                                   width=6,
                                   activebackground='#333333',
                                   font=('arial', 10, 'bold'),
                                   activeforeground='white', command=start,
                                   fg='white')
        self.stop_btn = tk.Button(master, bg='#222222', text='STOP',
                                  fg='white',
                                  activebackground='#333333',
                                  activeforeground='white',
                                  font=('arial', 10, 'bold'), state='disabled',
                                  command=self.stop)

    def turbo(self):
        if self.bool_var.get():
            screen.tracer(0, 0)
        else:
            screen.tracer(1, 1)

    def draw(self, **kwargs):
        self.start_btn.grid(column=0, row=0, sticky='w')
        self.stop_btn.grid(column=1, row=0, sticky='e')
        super().draw()

    @staticmethod
    def stop():
        global stopped
        stopped = True
        screen.tracer(0, 0)


class ColorWidget(tk.LabelFrame):
    def __init__(self, master, text, bg='#333333', fg='white'):
        super().__init__(master=master, text=text, bg=bg, fg=fg, padx=6, pady=5)
        self.color = tk.StringVar(value='#FFFFFF')
        self.is_rand = tk.BooleanVar()
        self.entry = ttk.Entry(self, width=8, textvariable=self.color)

        self.random = ttk.Checkbutton(self, text='Random', takefocus=False,
                                      variable=self.is_rand,
                                      command=self.disabler)

    def disabler(self):
        if self.is_rand.get():
            self.entry.config(state='readonly')
        else:
            self.entry.config(state='normal')

    def randomize(self):
        self.color.set('#'+''.join(
            [f'{round(i*255):X}'.zfill(2) for i in hsv_to_rgb(random(),
             uniform(*color_config['saturation']),
             uniform(*color_config['brightness']))]))

    def get_color(self):
        if self.is_rand.get():
            self.randomize()
        return self.color.get()

    def toggle(self, val):
        self.is_rand.set(val)
        self.disabler()

    def draw(self):
        self.grid(sticky='nsew')
        self.entry.grid(column=0, row=0)
        self.random.grid(column=1, row=0, padx=5, sticky='e', columnspan=2, )


class AllRandomCheckBtn(ttk.Checkbutton):
    def __init__(self, master, text):
        self.bool_var = tk.BooleanVar(value=False)
        super().__init__(master=master, text=text, variable=self.bool_var,
                         takefocus=False, command=self.toggler)

    def toggler(self):
        if self.bool_var.get():
            color.toggle(True)
            pensize.toggle(True)
            arm_amount.toggle(True)
            arm_length.toggle(True)
            v_amount.toggle(True)
            v_length.toggle(True)
            ange.toggle(True)
        else:
            color.toggle(False)
            pensize.toggle(False)
            arm_amount.toggle(False)
            arm_length.toggle(False)
            v_amount.toggle(False)
            v_length.toggle(False)
            ange.toggle(False)


# ------------------- Window, some settings -------------------

root = tk.Tk()
root.title('Snow')
root.geometry('1650x800+200+200')
root.minsize(1000, 780)
root.config(bg='#222222')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = tk.Canvas(root, width=1366, height=720)
canvas.config(highlightbackground='#333333')
canvas.grid(sticky='nsew')
screen = tur.TurtleScreen(canvas)
screen.bgcolor('#333333')
turtle = tur.RawTurtle(screen)
turtle.speed(0)
turtle.color('white')

# Vars
auto_randomize_bool = tk.BooleanVar(value=True)
stopped = False

# Ttk style
style = ttk.Style()
style.configure('.', background='#333333', foreground='white')
style.configure('TEntry', background='#333333', foreground='black')
style.configure('TLabelframe', background='#333333', foreground='#666666')
style.configure('TButton', foreground='black')

snow_config = {'arm_amount': 6, 'arm_length': 70, 'v_amount': 6,
               'v_length': 40, 'angle': 60}
color_config = {'saturation': (0.5, 1),     # Use values between 0 and 1
                'brightness': (0.7, 1)}

# ------------------- Settings frame widgets -------------------

config_menu = tk.Frame(root, bg='#333333', bd=3, relief='raised', width=300,
                       padx=5, pady=5)

start_frame = tk.Frame(config_menu, bg='#333333', bd=3, relief='raised',
                       padx=3, pady=3)

starter = StartWidget(start_frame, 'Snow flake amount', 1, 10)

canvas_clear_btn = tk.Button(config_menu, bg='#222222', text='Clear',
                             fg='white', activebackground='#333333',
                             activeforeground='white', width=10,
                             command=lambda: turtle.clear())

snowflake_config_frame = tk.Frame(config_menu, bg='#333333', relief='raised',
                                  bd=3, padx=3, pady=3)
random_frame = tk.Frame(snowflake_config_frame, bg='#333333', bd=3)

randomizer = tk.Button(random_frame, bg='#222222', text='Randomize',
                       fg='white', activebackground='#333333',
                       activeforeground='white', command=randomize_config)
all_random = AllRandomCheckBtn(random_frame, text='All rand')

color = ColorWidget(snowflake_config_frame, text='Color')

pensize = ScaleWithEntry(snowflake_config_frame, 'Pen size', 1, 3)
arm_amount = ScaleWithEntry(snowflake_config_frame, 'Arm amount', 3, 12)
arm_length = ScaleWithEntry(snowflake_config_frame, 'Arm length', 40, 100)
v_amount = ScaleWithEntry(snowflake_config_frame, '"V" amount', 3, 8)
v_length = ScaleWithEntry(snowflake_config_frame, '"V" length', 20, 60)
ange = ScaleWithEntry(snowflake_config_frame, '"V" angle', 30, 90)

# ---------------------------- Grid ----------------------------

config_menu.columnconfigure(0, weight=1)
# noinspection PyTypeChecker
config_menu.rowconfigure((0, 1, 2), weight=1)
config_menu.grid(sticky='nsew', row=0, column=1)

start_frame.grid(sticky='n')
starter.draw()

canvas_clear_btn.grid(sticky='n')

snowflake_config_frame.grid()
random_frame.grid(sticky='ew')
randomizer.grid(sticky='w')
all_random.grid(row=0, column=1, sticky='e')
color.draw()

pensize.draw()
arm_amount.draw()
arm_length.draw()
v_amount.draw()
v_length.draw()
ange.draw()

root.mainloop()

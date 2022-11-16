import turtle as tur


class Zone(tur.Turtle):
    zone_list = []

    @classmethod
    def checker(cls, plr):
        for zone in cls.zone_list:
            if zone.cords[0] <= plr.xcor() <= zone.cords[2] and \
                    zone.cords[1] <= plr.ycor() <= zone.cords[3]:
                zone.active = True
                zone.command()

    def __init__(self, start_pos, sides, color, command=lambda: ...):
        tur.Turtle.__init__(self, visible=False)
        Zone.zone_list.append(self)
        self.cords = (start_pos[0], start_pos[1],
                      start_pos[0]+sides[0], start_pos[1]+sides[1])
        self.color(color)
        self.fillcolor(color)
        self.command = command
        self.speed(0)
        self.draw(*self.cords)

    def draw(self, x1, y1, x2, y2):
        self.pu()
        self.goto(x1, y1)
        self.pd()
        self.begin_fill()
        self.setx(x2)
        self.sety(y2)
        self.setx(x1)
        self.sety(y1)
        self.end_fill()


class Player(tur.Turtle):
    def __init__(self, color='#f0f0f0'):
        tur.Turtle.__init__(self, shape='circle')
        self.color(color)
        self.pu()
        self.shapesize(0.5)
        self.moves = 0

    def move(self, ang, x=0, y=0):
        self.moves += 1
        if self.tiltangle() != ang:
            self.settiltangle(ang)
        self.goto(self.xcor() + x, self.ycor() + y)
        Zone.checker(self)


def message(turtle, text, color='#f0f0f0'):
    window.tracer(0, 0)
    turtle.clear()
    turtle.pu()
    turtle.color(color)
    turtle.goto(-100, -100)
    turtle.pd()
    turtle.write(text, font=("Arial", 12, "bold"))
    window.tracer(1, 1)


window = tur.Screen()
window.title("Circle game")
window.setup(500, 500)
window.bgcolor('#333333')
window.tracer(0, 0)
msg = tur.Turtle(visible=False)


blue_zone = Zone(start_pos=(-250, 70), sides=(53, 150), color='#4169E1',
                 command=lambda: message(msg, player.moves))
green_zone = Zone(start_pos=(100, 0), sides=(70, 30), color='#44944A',
                  command=lambda: player.shape('circle'))
red_zone = Zone(start_pos=(-70, -60), sides=(60, 50), color='#FA4545',
                command=lambda: player.color('red'))
yellow_zone = Zone(start_pos=(0, 65), sides=(40, 40), color='yellow',
                   command=lambda: player.shape('turtle'))
purple_zone = Zone(start_pos=(90, 150), sides=(90, 50), color='#B255FF',
                   command=lambda: player.shapesize(player.shapesize()[0]+0.1))
orange_zone = Zone(start_pos=(70, -150), sides=(50, 90), color='#FFA000',
                   command=lambda: player.shapesize(player.shapesize()[0]-0.1))

window.tracer(1, 1)
player = Player()

STEP = 10

tur.listen()
tur.onkeypress(lambda: player.move(y=STEP, ang=90), 'Up')
tur.onkeypress(lambda: player.move(y=-STEP, ang=270), 'Down')
tur.onkeypress(lambda: player.move(x=STEP, ang=0), 'Right')
tur.onkeypress(lambda: player.move(x=-STEP, ang=180), 'Left')
tur.done()

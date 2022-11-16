import time
from turtle import *


start_time = time.time()
tracer(0, 0)
speed(0)
bgcolor('black')
pencolor('red')

for i in range(360):
    rt(i)
    circle(125, i)
    fd(i)
    rt(180)
    update()
print("--- %s seconds ---" % (time.time() - start_time))
done()

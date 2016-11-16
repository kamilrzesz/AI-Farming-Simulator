from tkinter import *
from random import randint
import time
def move_widget(item, x, y):
    """Moves a widget(item) on the main canvas to the new coordinates(x,y)"""
    main_canvas.coords(item,x,y)
    main_canvas.update()
def plough_field(x,y, l, w):
    """ Top left conner of the farm is at coordinates (x,y)
        Creates a farm with the width of 'w' and length of 'l'
        l and w has to be in multiples of 10 """
    global ploughed_texture
    ploughed_texture = PhotoImage(file="textures/cabbage.gif")
    for i in range(x,l+x,10):
        for k in range(y,w+y,10):
            main_canvas.create_image(i,k,image=ploughed_texture, anchor = NW)
def main():
    root = Tk()
    icon = Image("photo", file="textures/tractor.gif")  
    root.tk.call('wm','iconphoto',root._w,icon) #Changes the application icon
    main_canvas = Canvas(width =600, height = 400, bg='white')#create canvas
    main_canvas.pack(expand = YES, fill = BOTH)
    bck_img = PhotoImage(file="textures/background.gif")
    global main_canvas
    main_canvas.create_image(0,0,image=bck_img,anchor=NW) # Sets background of the window to grass
    tractor_img = PhotoImage(file="textures/tractor.gif")
    x_min = 0 # min and max values used in setting boundaries on the canvas
    y_min= 0  # max values also used in setting starting coordinates for tractor
    x_max=int(main_canvas['width'])
    y_max=int(main_canvas['height'])
    rh= randint(8,12)
    rw = randint(10,14)
    plough_field(300,220,int(rw*10),int(rh*10))
    tractor1 = main_canvas.create_image(300,200,image=tractor_img, anchor = NW) #adding tractor to the canvas
    vx = 1
    vy = 1
    while True:
        x1,y1= main_canvas.coords(tractor1)  # takes current coordinates of tractor
        if x1 > 300 and x1<((rw*10)+300)and y1 > 220 and y1<((rh*10)+220):
            print("inside farm") # checks if the x coord of tractor is inside field
        if (x1+10)> x_max:
            vx=-1
        if (y1+10)> y_max:
            vy=-1
        if (y1)<y_min:
            vy = 1
        if (x1)<x_min:
            vx=1
        move_widget(tractor1, x1+vx, y1+vy)
        time.sleep(0.01)
    mainloop()
main()

from tkinter import *
from random import randint
import time
def move_widget(item, x, y):
    """Moves a widget(item) on the main canvas to the new coordinates(x,y)"""
    main_canvas.coords(item,x,y)
    main_canvas.update()
def add_cabbage_field(x,y, l, w,item):
    """ Top left conner of the farm is at coordinates (x,y)
        Creates a farm with the width of 'w' and length of 'l'
        l and w has to be in multiples of 10 """
    for i in range(x,l+x,10):
        for k in range(y,w+y,10):
            main_canvas.create_image(i,k,image=item, anchor = NW)
    existing_farms_x1.append(x)
    existing_farms_x2.append(x+l)
    existing_farms_y1.append(y)
    existing_farms_y2.append(y+w)
    print(existing_farms_x1,existing_farms_x2,existing_farms_y1,existing_farms_y2)
def inside_farm(tractor):
    x,y= main_canvas.coords(tractor)
    i = 0
    while i < len(existing_farms_x1):
        if x > existing_farms_x1[i] and x< existing_farms_x2[i] and y > existing_farms_y1[i] and y<existing_farms_y2[i]:
            #go_start_field(tractor, existing_farms_x1[i],existing_farms_y1[i])
            #Above will be used for gathering crops later
            return True
        else:
            status = False
        i+=1
    return status

def fence(x,y,l,w,item):
    """ Will make fence tileable (used in bottom of page) can be used later for
    animal fencing etc.)"""
    for a in range(x,l+x,10):
        for b in range(y,w+y,10):
            main_canvas.create_image(a,b,image=item,anchor = NW)

def go_start_field(tractor, farm_x, farm_y):
    move_widget(tractor,farm_x,farm_y)
def main():
    root = Tk()
    icon = Image("photo", file="textures/tractor.gif")  
    root.tk.call('wm','iconphoto',root._w,icon) #Changes the application icon
    global main_canvas
    fence_img = PhotoImage(file="textures/fence.gif")#Assigns fence image
    side_fence = PhotoImage(file="textures/side_fence.gif") #Assigns fence_long image
    main_canvas = Canvas(width =600, height = 400, bg='white')#create canvas
    main_canvas.pack(expand = YES, fill = BOTH)
    bck_img = PhotoImage(file="textures/background.gif")
    main_canvas.create_image(0,0,image=bck_img,anchor=NW) # Sets background of the window to grass
    main_canvas.create_image(0,0,image=bck_img,anchor=NW) # Sets background of the window to grass
    tractor_img = PhotoImage(file="textures/tractor.gif")
    x_min = 0 # min and max values used in setting boundaries on the canvas
    y_min= 0  # max values also used in setting starting coordinates for tractor
    x_max=int(main_canvas['width'])
    y_max=int(main_canvas['height'])
    rh= randint(8,12)
    rw = randint(10,14)
    global existing_farms_x1,existing_farms_x2, existing_farms_y1, existing_farms_y2
    cabbage_texture = PhotoImage(file="textures/cabbage.gif")
    existing_farms_x1,existing_farms_x2, existing_farms_y1, existing_farms_y2 = [],[],[],[]
    add_cabbage_field(100,50,int(rw*10),int(rh*10),cabbage_texture)
    add_cabbage_field(300,220,int(rw*10),int(rh*10),cabbage_texture)
    fence(1,390,int(600),int(10),fence_img)
    fence(1,5,int(600),int(10),fence_img)
    fence(1,1,int(10),int(400),side_fence)
    fence(595,1,int(10),int(400),side_fence)


    
    print(existing_farms_x1)
    tractor_img = PhotoImage(file="textures/tractor.gif")
    tractor1 = main_canvas.create_image(300,200,image=tractor_img, anchor = NW) #adding tractor to the canvas
    vx = 1
    vy = 1
    while True:
        x1,y1= main_canvas.coords(tractor1)
        if (x1+20)> x_max:
            vx=-1
        if (y1+25)> y_max:
            vy=-1
        if (y1)<y_min:
            vy = 1
        if (x1)<x_min:
            vx=1
        move_widget(tractor1, x1+vx, y1+vy)
        inside_farm(tractor1)
        time.sleep(0.01)
    mainloop()
main()

from tkinter import *
from random import randint
import time
def move_widget(item, x, y):
    """ Moves a widget(item) on the main canvas to the new coordinates(x,y)"""
    main_canvas.coords(item,x,y)
    main_canvas.update()
def add_cabbage_field(x,y, l, w,item):
    """ Top left conner of the farm is at coordinates (x,y)
        Creates a farm with the width of 'w' and length of 'l'
        l and w has to be in multiples of 10 """
    for i in range(x,l+x,10):
        for k in range(y,w+y,10):
            main_canvas.create_image(i,k,image=item, anchor = NW)
    existing_farms.append([x,x+l,y,y+w,"grown"])
    print(existing_farms)
def fence(x,y,l,w,item):
    """ Will make fence tileable (used in bottom of page) can be used later for
    animal fencing etc.)"""
    for a in range(x,l+x):
        for b in range(y,w+y):
            main_canvas.create_image(a,b,image=item,anchor = NW)
def inside_farm(tractor):
    """ Checks if the tractor is inside the farm.
        More specifcally it checks if the top left coordinate is inside the area marked by any of the cabbage fields 
        on the screen, if they were added using add_cabbage_field function
        Returns a boolean result. True if tractor is inside a farm.
        i is a global variable, sygnaling which farm the tractor is on, do not reassign else where"""
    x,y= main_canvas.coords(tractor)
    global v
    v = 0
    while v < len(existing_farms):
        if x > existing_farms[v][0] and x< existing_farms[v][1] and y > existing_farms[v][2] and y<existing_farms[v][3]:
            return True
        else:
            status = False
        v+=1
    return status
def collect_cabbage(tractor,farm,texture,trac_img):
    """Collects cabbage function"""
    farm_length = farm[1] - farm[0]
    farm_height = farm[3] - farm[2]
    cabbage_count = 0
    local_cab_var = StringVar()
    Label(root, textvariable=local_cab_var).pack()
    for k in range(0, farm_height,10):
        for w in range(0,farm_length,10):
            move_widget(tractor,farm[0]+w,farm[2]+k)
            trac_x,trac_y = main_canvas.coords(tractor)
            main_canvas.create_image(trac_x,trac_y,image=texture, anchor=NW)
            cabbage_count+=1
            local_cab_var.set("Tractor cabbages: "+str(cabbage_count))
            time.sleep(0.1)
    existing_farms[v][4] = "empty"
    main_canvas.tag_raise(tractor)
    return cabbage_count
def add_sheep (x,y,item):
    '''This adds an image of a sheep to the canvas'''
    main_canvas.create_image(x,y, image=item, anchor = NW,)
def add_hay (x,y,item):
    main_canvas.create_image(x,y,image=item,anchor = NW)
def fence(x,y,l,w,item):
    """ Will make fence tileable (used in bottom of page) can be used later for
    animal fencing etc.)"""
    for a in range(x,l+x,10):
        for b in range(y,w+y,10):
            main_canvas.create_image(a,b,image=item,anchor = NW)
def hay_button():
    add_hay(randint(50,1150), randint(50, 650),haybail)
def go_start_field(tractor, farm_x, farm_y):
    move_widget(tractor,farm_x,farm_y)
def sheep_button():
    add_sheep(randint(50, 1150), randint(50, 650), sheep1)
def main():
    global root
    root = Tk()
    icon = Image("photo", file="textures/tractor_right.gif")  
    root.tk.call('wm','iconphoto',root._w,icon) #Changes the application icon
    global main_canvas
    fence_img = PhotoImage(file="textures/fence.gif")#Assigns fence image
    side_fence = PhotoImage(file="textures/side_fence.gif") #Assigns fence_long image
    main_canvas = Canvas(width =1200, height = 720, bg='white')#create canvas
    main_canvas.pack(expand = YES, fill = BOTH)
    x_min = 0 # min and max values used in setting boundaries on the canvas
    y_min= 0  # max values also used in setting starting coordinates for tractor
    x_max=int(main_canvas['width'])
    y_max=int(main_canvas['height'])
    bck_img = PhotoImage(file="textures/background.gif")
    main_canvas.create_image(0,0,image=bck_img,anchor=NW) # Sets background of the window to grass
    barn_img = PhotoImage(file="textures/barn.gif")
    barn = main_canvas.create_image(x_max-10,y_min+20,image=barn_img,anchor=NE)
    rh= randint(8,12)
    rw = randint(10,14)
    global existing_farms, sheep1 # existsing farms is list containing a list for each individual farm. Order of items inside the inner list is: x-coord, y-coord, x2-coord, y2-coord, farm_type
    dirt_texture = PhotoImage(file="textures/dirt.gif")
    cabbage_texture = PhotoImage(file="textures/cabbage.gif")
    existing_farms = []
    add_cabbage_field(100,50,(rw*10),(rh*10),cabbage_texture)
    add_cabbage_field(300,220,(rw*10),(rh*10),cabbage_texture)
    fence(1,((y_max)-10),(x_max),int(10),fence_img)
    fence(1,(y_min)+5,(x_max),int(10),fence_img)
    fence(1,1,(x_min)+5,(y_max),side_fence)
    fence(1195,1,(x_min)+5,(y_max),side_fence)
    sheep1=PhotoImage(file='textures/sheep.gif')
    haybail = PhotoImage(file="textures/hay_bail.gif")
    global haybail
    button = Button(main_canvas, width=30, text = 'Add Sheep', command = sheep_button, bg='light green')
    button_haybail = Button(main_canvas, width=30, text = "Add Hay Bails", command=hay_button)
    button.configure(width=10)
    button_haybail.configure(width=10)
    button1 = main_canvas.create_window(1,(y_max)-30,anchor=NW,window=button)
    button2 = main_canvas.create_window(130,(y_max)-30,anchor=NW,window=button_haybail)
    tractor_img = PhotoImage(file="textures/tractor_right.gif")
    tractor1 = main_canvas.create_image(300,200,image=tractor_img, anchor = NW) #adding tractor to the canvas
    vx = -1
    vy = -1
    cabbages_global = 0
    global_cabbage_var = StringVar()
    Label(root, textvariable=global_cabbage_var).pack()
    while True:
        x1,y1= main_canvas.coords(tractor1)
        if (x1+20)> x_max and inside_farm(tractor1)==False:
            vx=-1
        if (y1+25)> y_max and inside_farm(tractor1)==False:
            vy=-1
        if (y1)<y_min and inside_farm(tractor1)==False:
            vy = 1
        if (x1)<x_min and inside_farm(tractor1)==False:
            vx=1
        if inside_farm(tractor1) == True and existing_farms[v][4]=="grown":
            cabbages_global+=collect_cabbage(tractor1, existing_farms[v],dirt_texture,tractor_img)
            print(cabbages_global)
            global_cabbage_var.set("Global cabbages: "+str(cabbages_global))
            continue
        if inside_farm(tractor1) == False or existing_farms[v][4] == "empty":
            move_widget(tractor1, x1+vx, y1+vy)

        time.sleep(0.01)
    mainloop()
main()
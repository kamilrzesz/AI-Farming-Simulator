from tkinter import *
from random import randint
import time
root = Tk()

def move_widget(item, x, y):
    """ Moves a widget(item) on the main canvas to the new coordinates(x,y)"""
    main_canvas.coords(item,x,y)
    main_canvas.update()
def add_cabbage_field(x,y, l, w,item,tractor):
    """ Top left conner of the farm is at coordinates (x,y)
        Creates a farm with the width of 'w' and length of 'l'
        l and w has to be in multiples of 10 """
    for i in range(x,l+x,10):#from x to l there is a step adding 10 pixels each time til it gets to x+l
        for k in range(y,w+y,10):#does the same but for y coord Both for loops create boxes for the cabbages to be placed (for every iteration a box is created)
            main_canvas.create_image(i,k,image=item, anchor = NW)#adds box at the coords (i and k are passed on with the image of items passed on)
    existing_farms.append([x,x+l,y,y+w,"grown"])#adds the coordinates all x and y coords to the farm (all coords of the corners) and adds stutus'grown' so later we know that the tractor doesnt have to plough the field again
    print(existing_farms)#prints the list of existing farms
    main_canvas.tag_raise(tractor)#raises the tractor so it is always visible above the farms

def fence(x,y,l,w,item):
    """ Will make fence tileable (used in bottom of page) can be used later for
    animal fencing etc.)"""
    for a in range(x,l+x):
        for b in range(y,w+y):
            main_canvas.create_image(a,b,image=item,anchor = NW)

def sheep_movement():
    vx = 1
    vy = 1
    x_min1 = 0 # min and max values used in setting boundaries on the canvas
    y_min1 = 0  # max values also used in setting starting coordinates for tractor
    x_max1 = int(main_canvas['width'])
    y_max1 = int(main_canvas['height'])
    print(main_canvas.coords(existing_sheep_widget))
    for p in range(0, len(existing_sheep)):
        x1, y1 = main_canvas.coords(existing_sheep_widget[p])
        if (x1+12)> x_max1 :
            vx = randint(-1,1)
        if (y1+9)> y_max1:
            vy = randint(-1,1)
        if (y1)<y_min1:
            vy =randint(-1,1)
        if (x1)<x_min1:
            vx = randint(-1,1)
        move_widget(existing_sheep_widget[p],(x1+vx),(y1+vy))

def inside_farm(tractor):
    """ Checks if the tractor is inside the farm.
        More specifically it checks if the top left coordinate is inside the area marked by any of the cabbage fields
        on the screen, if they were added using add_cabbage_field function
        Returns a boolean result. True if tractor is inside a farm.
        v is a global variable, signaling which farm the tractor is on, do not reassign else where"""
    x,y= main_canvas.coords(tractor)#attributes require you to pass the tractor through you we can get the coords of the tractor
    global v#indicates what farm the tractor is inside so if it returns true, v will be used to collect cabbages so we know what farm to collect cabbages from
    v = 0# the first index of the farm is 0 - checks the first farm
    while v < len(existing_farms):#every time it iterates it adds 1 - if v is smaller than length of existing farms, tells u to perform the code below so it checks every single farm
        if x > existing_farms[v][0] and x< existing_farms[v][1] and y > existing_farms[v][2] and y<existing_farms[v][3]:#if the x and y coords of the tractor are inside the farm (stops the function and returns true)
            return True
        else:
            status = False#else makes the status false and at the end if the while loop ennds  and the tractor wasnt inside the farms, it will return the status(which is false) this means the tractor is not inside the farm
        v+=1#means v = v+1  -moves on to check if the tractor is in the next farm
    return status
def go_to_barn(tractor):#all it wants is the tractor so we can extract its exact current coords
    """ Function for tractor to go to the barn"""
    vx=1#velocity of x
    vy=1#velocity of y - how much it will move by in every loop iteration in the y direction
    while True:#this loop happens all the time
        trac_x,trac_y = main_canvas.coords(tractor)#gets the coords of tractor
        barn_x,barn_y = main_canvas.coords(barn)#gets the coords of the barn
        barn_x-=55#reduces the x coords of the barn by 55 (where we want the tractor to stop)
        barn_y+=30#reduces the y coords of the barn by 30 (where we want the tractor to stop)
        if trac_x<barn_x:
            vx=1#velocity of x is 1 - we want to increase by 1 becasue we want it to move towards the barn
        if trac_x>barn_x:
            vx=-1#same as before, but if the x coord is larger and we want to make it smaller by 1
        if trac_x==barn_x:
            vx=0#if the x ccord is the same as barn x - x velocity is zero, stopping it from moving in x plane, makes it move only in the y axis if needed
        if trac_y<barn_y:
            vy=1#exactly what we did for x, but with y
        if trac_y>barn_y:
            vy=-1#if y is bigger than 1, we minus one to the current coordinate 
        if trac_y==barn_y:
            vy=0#if the y coord is equal, stays the same and moves in the x axis
        if trac_x==barn_x and trac_y==barn_y:
            unload_cabbages()#if both x and y of the tractor are equal to the x and y of the barn, it will return none and exits the function
            return None
        move_widget(tractor,trac_x+vx,trac_y+vy)#moves the tractor by the velocity we received from the if statements
        time.sleep(0.01)#stops the tractor between each iteration of the loop so we can see the prgress of the tractor better

def unload_cabbages():
    """ Function to display cabbages deposited to the barn on screen for the user to read"""
    time.sleep(5)
    print("csha")

def collect_cabbage(tractor,farm,texture,trac_img):
    """Collects cabbage from farms it comes across function"""
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
    existing_farms[v][4] = "empty"
    main_canvas.tag_raise(tractor)
    go_to_barn(tractor)
    return cabbage_count

def add_sheep (x,y,item):
    '''This adds an image of a sheep to the canvas'''
    s = 0
    
    for s in range(0, len(existing_farms)):
        #If statement makes sure that the sheep does not spawn on a cabbage patch
        if x > existing_farms[s][0] and x < existing_farms[s][1] and y > existing_farms[s][2] and y<existing_farms[s][3]:
            #recur the function, it will keep recuring until the coordinates are not on a cabbage patch.
            add_sheep(randint(50, 1150), randint(50, 650), sheep1)
            return None
            #add a sheep to the canvas once the x and y coordinates do not clash with a cabbage patch
    temp_sheep_widget=main_canvas.create_image(x,y, image = item, anchor = NW)
    existing_sheep_widget.append(temp_sheep_widget)
    existing_sheep.append([x,y])

   
def add_hay (x,y,item):
    """ Add hay images to the canvas at random locations function"""
    s = 0
    for s in range(0, len(existing_farms)):
        ''' This code below will make sure hay bales dont spawn on top of eachother'''
        if x > existing_farms[s][0] and x < existing_farms[s][1] and y > existing_farms[s][2] and y < existing_farms[s][3]:
            add_hay(randint(50, 1150), randint(50, 650), haybail)
            return None
    main_canvas.create_image(x,y,image=item,anchor=NW)
    main_canvas.create_image(x,y,image=item,anchor = NW)
    
def fence(x,y,l,w,item):
    """ Will make fence tileable (used in bottom of page) can be used later for
    animal fencing etc.)"""
    for a in range(x,l+x,10):
        for b in range(y,w+y,10):
            main_canvas.create_image(a,b,image=item,anchor = NW)
            
def farm_button(tractor):
    '''Adds more farms when button is pressed'''
    add_cabbage_field (randint(100, 1100),randint(50,600),(rw * 10), (rh * 10),cabbage_texture,tractor)

def hay_button():
    """Button for connecting the button being pressed by the user to the function to create the hay on the screen"""
    add_hay(randint(50,1150), randint(50, 650),haybail)
    
def go_start_field(tractor, farm_x, farm_y):
    """Function to go to the start of the farm to start cropping the contents of it"""
    move_widget(tractor,farm_x,farm_y)
    
def sheep_button():
    """ Button to connect button being pressed by the user to function to draw the sheep on the screen"""
    add_sheep(randint(50, 1150), randint(50, 650), sheep1)

""" All the imported images are in this section"""
fence_img = PhotoImage(file="textures/fence.gif")#Assigns fence image
side_fence = PhotoImage(file="textures/side_fence.gif") #Assigns fence_long image
tractor_img = PhotoImage(file="textures/tractor_right.gif")
bck_img = PhotoImage(file="textures/background.gif")
barn_img = PhotoImage(file="textures/barn.gif")
dirt_texture = PhotoImage(file="textures/dirt.gif")
cabbage_texture = PhotoImage(file="textures/cabbage.gif")
sheep1=PhotoImage(file='textures/sheep.gif')
haybail = PhotoImage(file="textures/hay_bail.gif")
"""---------------------------------------------------------------------------------------------------------"""


"""All the variables are in this section"""
existing_farms, existing_sheep, existing_sheep_widget = [], [], []   



def main():
    """Main function to make canvas and multiple things in it, also includes multiple variables and imports of images etc."""
    global root,barn, rw,rh
    icon = Image("photo", file="textures/tractor_right.gif")
    root.tk.call('wm','iconphoto',root._w,icon) #Changes the application icon
    global main_canvas, haybail, cabbage_texture
    main_canvas = Canvas(width =1200, height = 720, bg='white')#create canvas
    main_canvas.pack(expand = YES, fill = BOTH)
    x_min = 0 # min and max values used in setting boundaries on the canvas
    y_min= 0  # max values also used in setting starting coordinates for tractor
    x_max=int(main_canvas['width'])
    y_max=int(main_canvas['height'])
    tractor1 = main_canvas.create_image(300,200,image=tractor_img, anchor = NW) #adding tractor to the canvas
    main_canvas.create_image(0,0,image=bck_img,anchor=NW) # Sets background of the window to grass
    barn = main_canvas.create_image(x_max-10,y_min+20,image=barn_img,anchor=NE)
    rh= randint(8,12)
    rw = randint(10,14)
    global existing_farms, sheep1, existing_sheep, existing_sheep_widget # existsing farms is list containing a list for each individual farm. Order of items inside the inner list is: x-coord, y-coord, x2-coord, y2-coord, farm_type
    add_cabbage_field(100,50,(rw*10),(rh*10),cabbage_texture,tractor1)
    add_cabbage_field(300,220,(rw*10),(rh*10),cabbage_texture,tractor1)
    fence(1,((y_max)-10),(x_max),int(10),fence_img)
    fence(1,(y_min)+5,(x_max),int(10),fence_img)
    fence(1,1,(x_min)+5,(y_max),side_fence)
    fence(1195,1,(x_min)+5,(y_max),side_fence)
    button = Button(main_canvas, width=30, text = 'Add Sheep', command = sheep_button, bg='light green')
    button_haybail = Button(main_canvas, width=30, text = "Add Hay Bails", command=hay_button)
    button_farm = Button(main_canvas, width=30, text = 'Add Farm',command=lambda:farm_button(tractor1))
    button.configure(width=10)
    button_haybail.configure(width=10)
    button1= main_canvas.create_window(1,(y_max)-30,anchor=NW,window=button)
    button2 = main_canvas.create_window(130,(y_max)-30,anchor=NW,window=button_haybail)
    button3 = main_canvas.create_window(260,(y_max)-30,anchor=NW,window=button_farm)
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
            global_cabbage_var.set("Barn cabbages: "+str(cabbages_global))
            continue
        if inside_farm(tractor1) == False or existing_farms[v][4] == "empty":
            move_widget(tractor1, x1+vx, y1+vy)

        sheep_movement()
        time.sleep(0.01)
    
    mainloop()
main()

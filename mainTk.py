from tkinter import *
from random import randint
import time

global root
root = Tk()
global barn_img, haybail, cabbage_texture, sheep1, tractor_img, side_fence, fence_img, dirt_texture
""" All the imported images are in this section"""
fence_img = PhotoImage(file="textures/fence.gif")  # Assigns fence image
side_fence = PhotoImage(file="textures/side_fence.gif")  # Assigns fence_long image
tractor_img = PhotoImage(file="textures/tractor_right.gif")
bck_img = PhotoImage(file="textures/background.gif")
barn_img = PhotoImage(file="textures/barn.gif")
dirt_texture = PhotoImage(file="textures/dirt.gif")
cabbage_texture = PhotoImage(file="textures/cabbage.gif")
sheep1 = PhotoImage(file='textures/sheep.gif')
haybail = PhotoImage(file="textures/hay_bail.gif")
"""---------------------------------------------------------------------------------------------------------"""

"""All the variables are in this section"""
global barn, trac_x, barn_x, trac_y, barn_y, tractor, rw, rh, existing_farms, x_max, y_max, vx, vy, x_min, y_min, barn_cabbage_var,tractor_cabbage_var
x_min = 0  # min and max values used in setting boundaries on the canvas
y_min = 0  # max values also used in setting starting coordinates for tractor    
existing_farms,existing_sheep,existing_sheep_widget = [], [], [] # existsing farms is list containing a list for each individual farm. Order of items inside the inner list is: x-coord, y-coord, x2-coord, y2-coord, farm_type
farm_coords = [[20,20,100,120],[20,160,220,160],[20,330,100,180],[20,540,100,80],[20,640,300,60],[140,20,100,50],[140,80,100,60],[140,340,100,210],[140,560,200,60],[260,20,180,190],[260,220,100,80],[370,220,150,80],[260,320,260,220],[350,560,170,140],[540,220,120,120],[680,220,220,120],[740,360,100,180],[540,610,250,90],[850,360,240,80],[850,450,340,80],[1100,150,90,290],[920,150,160,200]]
fenced_area=[[460,0,440,200],[540,360,180,230],[800,550,400,160]]
print(fenced_area[0][0])
vx = -1
vy = -1
rh = randint(8, 12)
rw = randint(10, 14)
barn_cabbage_var = StringVar()
tractor_cabbage_var = StringVar()


def move_widget(item, x, y):
    """ Moves a widget(item) on the main canvas to the new coordinates(x,y)"""
    main_canvas.coords(item, x, y)
    main_canvas.update()


def add_cabbage_field(x, y, l, w, item, tractor):
    """ Top left conner of the farm is at coordinates (x,y)
        Creates a farm with the width of 'w' and length of 'l'
        l and w has to be in multiples of 10 """
    for i in range(x, l + x, 10):
        for k in range(y, w + y, 10):
            main_canvas.create_image(i, k, image=item, anchor=NW)
    existing_farms.append([x, x + l, y, y + w, "grown"])
    main_canvas.tag_raise(tractor)


def fence(x, y, l, w, item):
    """ Will make fence tileable (used in bottom of page) be used later for
    animal fencing etc.)"""
    for a in range(x, l + x):
        for b in range(y, w + y):
            main_canvas.create_image(a, b, image=item, anchor=NW)


def inside_farm(tractor):
    """ Checks if the tractor is inside the farm.
        More specifically it checks if the top left coordinate is inside the area marked by any of the cabbage fields
        on the screen, if they were added using add_cabbage_field function
        Returns a boolean result. True if tractor is inside a farm.
        v is a global variable, signaling which farm the tractor is on, do not reassign else where"""
    status = False
    x, y = main_canvas.coords(tractor)
    global v
    v = 0
    while v < len(existing_farms):
        if x > existing_farms[v][0] and x < existing_farms[v][1] and y > existing_farms[v][2] and y < existing_farms[v][3]:
            return True
        v += 1
    return status


def go_to_barn(tractor):
    """ Function for tractor to go to the barn"""
    vx = 1
    vy = 1
    while True:
        trac_x, trac_y = main_canvas.coords(tractor)
        barn_x, barn_y = main_canvas.coords(barn)
        barn_x -= 55
        barn_y += 30
        if trac_x < barn_x:
            vx = 1
        if trac_x > barn_x:
            vx = -1
        if trac_x == barn_x:
            vx = 0
        if trac_y < barn_y: 
            vy = 1
        if trac_y > barn_y:
            vy = -1
        if trac_y == barn_y:
            vy = 0
        if trac_x == barn_x and trac_y == barn_y:
            unload_cabbages()
            return None
        move_widget(tractor, trac_x + vx, trac_y + vy)
        sheep_movement()
        time.sleep(0.01)


def unload_cabbages():
    """ Function to display cabbages deposited to the barn on screen for the user to read
        Tractor waits a random amount of time to unload the cabbages, before returning to his task"""
    while True:
        if randint(0,20)==1:
            tractor_cabbage_var.set("Tractor cabbages: " +str(0))
            return None
        time.sleep(0.1)


def collect_cabbage(tractor, farm, texture, trac_img):
    """Collects cabbage from farms it comes across function"""
    farm_length = farm[1] - farm[0]
    farm_height = farm[3] - farm[2]
    cabbage_count = 0
    for k in range(0, farm_height, 10):
        for w in range(0, farm_length, 10):
            move_widget(tractor, farm[0] + w, farm[2] + k)
            trac_x, trac_y = main_canvas.coords(tractor)
            main_canvas.create_image(trac_x, trac_y, image=texture, anchor=NW)
            cabbage_count += 1
            tractor_cabbage_var.set("Tractor cabbages: " + str(cabbage_count))
            sheep_movement()
            time.sleep(0.05)
    existing_farms[v][4] = "empty"
    main_canvas.tag_raise(tractor)
    go_to_barn(tractor)
    return cabbage_count


def sheep_movement():
    vx = 1
    vy = 1
    x_min1 = 0  # min and max values used in setting boundaries on the canvas
    y_min1 = 0  # max values also used in setting starting coordinates for tractor
    x_max1 = int(main_canvas['width'])
    y_max1 = int(main_canvas['height'])
    for p in range(0, len(existing_sheep)):
        if randint(0, 100) == 5:
            x1, y1 = main_canvas.coords(existing_sheep_widget[p])
            vx = randint(-10, 10)
            vy = randint(-10, 10)
            move_widget(existing_sheep_widget[p], (x1 + vx), (y1 + vy))
def hit_fenced_area(x,y):
    """ Should detect when the tractor hits the fenced area, however i couldn't get it to work properly so it is not used."""
    global fenced_area_tracker
    fenced_area_tracker = 0
    status = False
    while fenced_area_tracker < len(fenced_area):
        if x > fenced_area[fenced_area_tracker][0] and x <(fenced_area[fenced_area_tracker][0]+fenced_area[fenced_area_tracker][1]) and y > fenced_area[fenced_area_tracker][2] and y < (fenced_area[fenced_area_tracker][2]+fenced_area[fenced_area_tracker][3]):
            print("True")
            return True
        fenced_area_tracker += 1
    return status
         
def add_sheep(item):
    '''This adds an image of a sheep to the canvas'''
    s = 0
    k= randint(0,2)
    x = randint(fenced_area[k][0],fenced_area[k][0]+fenced_area[k][2])
    y = randint(fenced_area[k][1],fenced_area[k][1]+fenced_area[k][3])
    """for s in range(0, len(existing_farms)):
        # If statement makes sure that the sheep does not spawn on a cabbage patch
        if x > existing_farms[s][0] and x < existing_farms[s][1] and y > existing_farms[s][2] and y < existing_farms[s][
            3]:
            # recur the function, it will keep recuring until the coordinates are not on a cabbage patch.
            add_sheep(randint(50, 1150), randint(50, 650), sheep1)
            return None
            # add a sheep to the canvas once the x and y coordinates do not clash with a cabbage patch""" #  No longer needed as sheep will only spawn inside the fenced areas
    temp_sheep_widget = main_canvas.create_image(x, y, image=item, anchor=NW)
    existing_sheep_widget.append(temp_sheep_widget)
    existing_sheep.append([x, y])


def add_hay(x, y, item):
    """ Add hay images to the canvas at random locations function"""
    s = 0
    for s in range(0, len(existing_farms)):
        ''' This code below will make sure hay bales dont spawn on top of eachother'''
        if x > existing_farms[s][0] and x < existing_farms[s][1] and y > existing_farms[s][2] and y < existing_farms[s][3]:
            add_hay(randint(50, 1150), randint(50, 650), haybail)
            return None
    main_canvas.create_image(x, y, image=item, anchor=NW)
    main_canvas.create_image(x, y, image=item, anchor=NW)


def fence(x, y, l, w, item):
    """ Will make fence tileable (used in bottom of page) can be used later for
    animal fencing etc.)"""
    for a in range(x, l + x, 10):
        for b in range(y, w + y, 10):
            main_canvas.create_image(a, b, image=item, anchor=NW)


def farm_button(tractor):
    '''Adds a random farm which was pre-setted inside the farm_coords list when button is pressed'''
    try:
        r = randint(0,len(farm_coords))
        add_cabbage_field(farm_coords[r][0],farm_coords[r][1],farm_coords[r][2],farm_coords[r][3],cabbage_texture,tractor)
        farm_coords.pop(r)
    except IndexError:
        print("Sorry, not enough space for another farm.")


def hay_button():
    """Button for connecting the button being pressed by the user to the function to create the hay on the screen"""
    add_hay(randint(50, 1150), randint(50, 650), haybail)


def go_start_field(tractor, farm_x, farm_y):
    """Function to go to the start of the farm to start cropping the contents of it"""
    move_widget(tractor, farm_x, farm_y)


def sheep_button():
    """ Button to connect button being pressed by the user to function to draw the sheep on the screen"""
    add_sheep(sheep1)


"""Adding things to the canvas(Fences,CabbageFields) at the beginning"""

def add_things_canvas():
    fence(1, (y_max) - 10, (x_max), int(10), fence_img)
    fence(1, (y_min) + 5, (x_max), int(10), fence_img)
    fence(1, 1, (x_min) + 5, (y_max), side_fence)
    fence(1195, 1, (x_min) + 5, (y_max), side_fence)
    # Testing new fence templates
    for i in range(0,len(fenced_area)):
        fence(fenced_area[i][0],fenced_area[i][1],fenced_area[i][2],10,fence_img)
        fence(fenced_area[i][0],fenced_area[i][1]+fenced_area[i][3],fenced_area[i][2],10,fence_img)
        fence(fenced_area[i][0],fenced_area[i][1],10,fenced_area[i][3],side_fence)
        fence(fenced_area[i][0]+fenced_area[i][2],fenced_area[i][1],10,fenced_area[i][3],side_fence)


def main():
    global main_canvas, tractor, x_max, y_max, barn, fence_img
    """Main function to create canvas and a few things in it"""
    main_canvas = Canvas(width=1200, height=720, bg='white')
    x_max = int(main_canvas['width'])
    y_max = int(main_canvas['height'])
    main_canvas.pack(expand=YES, fill=BOTH)
    main_canvas.create_image(0, 0, image=bck_img, anchor=NW)  # Sets background of the window to grass# create canvas
    button = Button(root, width=30, text='Add Sheep', command=sheep_button, bg='light green')
    button_haybail = Button(root, width=30, text="Add Hay Bails", command=hay_button)
    button_farm = Button(root, width=30, text='Add Farm', command=lambda: farm_button(tractor))
    button.configure(width=10)
    button_haybail.configure(width=10)
    button.pack(side=LEFT)
    button_haybail.pack(side=LEFT)
    button_farm.pack(side=LEFT)
    barn = main_canvas.create_image(x_max - 10, y_min + 20, image=barn_img, anchor=NE)
    tractor = main_canvas.create_image(300, 200, image=tractor_img, anchor=NW)  # adding tractor to the canvas
    Label(root, textvariable=tractor_cabbage_var).pack(side=RIGHT)   
    Label(root, textvariable=barn_cabbage_var).pack(side=RIGHT)
    '''Calls upon add_things_function above'''
    add_things_canvas()
    boundaries_detect()
    return


""" Boundaries detection"""
def boundaries_detect():
    global vx, vy
    cabbages_global = 0
    while True:
        x1, y1 = main_canvas.coords(tractor)
        k=hit_fenced_area(x1,y1)
        if (x1 + 20) > x_max and inside_farm(tractor) == False:
            vx = -1
        if (y1 + 25) > y_max and inside_farm(tractor) == False:
            vy = -1
        if (y1) < y_min and inside_farm(tractor) == False:
            vy = 1
        if (x1) < x_min and inside_farm(tractor) == False:
            vx = 1
        if inside_farm(tractor) == True and existing_farms[v][4] == "grown":
            cabbages_global += collect_cabbage(tractor, existing_farms[v], dirt_texture, tractor_img)
            print(cabbages_global)
            barn_cabbage_var.set("Barn cabbages: " + str(cabbages_global))
            continue
        if inside_farm(tractor) == False or existing_farms[v][4] == "empty":
            move_widget(tractor, x1 + vx, y1 + vy)
        sheep_movement()
        time.sleep(0.01)
    return

    mainloop()


main()

from tkinter import *
from random import randint
import time

global root
root = Tk()
global barn_img, haybail, cabbage_texture, sheep1, tractor_img, side_fence, fence_img, dirt_texture, icon
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
icon = Image("photo", file="textures/tractor_right.gif")
"""---------------------------------------------------------------------------------------------------------"""

"""All the variables are in this section"""
global barn, trac_x, barn_x, trac_y, barn_y, tractor, rw, rh, existing_farms, x_max, y_max, vx, vy, x_min, y_min, global_cabbage_var
x_min = 0  # min and max values used in setting boundaries on the canvas
y_min = 0  # max values also used in setting starting coordinates for tractor    global_cabbage_var = StringVar()
existing_farms,existing_sheep,existing_sheep_widget = [], [], [] # existsing farms is list containing a list for each individual farm. Order of items inside the inner list is: x-coord, y-coord, x2-coord, y2-coord, farm_type
vx = -1
vy = -1
rh = randint(8, 12)
rw = randint(10, 14)
global_cabbage_var = StringVar()


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
    print(existing_farms)
    main_canvas.tag_raise(tractor)


def fence(x, y, l, w, item):
    """ Will make fence tileable (used in bottom of page) can be used later for
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
        if x > existing_farms[v][0] and x < existing_farms[v][1] and y > existing_farms[v][2] and y < existing_farms[v][
            3]:
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
        time.sleep(0.00001)


def unload_cabbages():
    """ Function to display cabbages deposited to the barn on screen for the user to read"""
    time.sleep(5)
    print("csha")


def collect_cabbage(tractor, farm, texture, trac_img):
    """Collects cabbage from farms it comes across function"""
    farm_length = farm[1] - farm[0]
    farm_height = farm[3] - farm[2]
    cabbage_count = 0
    local_cab_var = StringVar()
    Label(root, textvariable=local_cab_var).pack()
    for k in range(0, farm_height, 10):
        for w in range(0, farm_length, 10):
            move_widget(tractor, farm[0] + w, farm[2] + k)
            trac_x, trac_y = main_canvas.coords(tractor)
            main_canvas.create_image(trac_x, trac_y, image=texture, anchor=NW)
            cabbage_count += 1
            local_cab_var.set("Tractor cabbages: " + str(cabbage_count))
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
    print(main_canvas.coords(existing_sheep_widget))
    for p in range(0, len(existing_sheep)):
        if randint(0, 100) == 5:
            x1, y1 = main_canvas.coords(existing_sheep_widget[p])
            vx = randint(-10, 10)
            vy = randint(-10, 10)
            move_widget(existing_sheep_widget[p], (x1 + vx), (y1 + vy))


def add_sheep(x, y, item):
    '''This adds an image of a sheep to the canvas'''
    s = 0

    for s in range(0, len(existing_farms)):
        # If statement makes sure that the sheep does not spawn on a cabbage patch
        if x > existing_farms[s][0] and x < existing_farms[s][1] and y > existing_farms[s][2] and y < existing_farms[s][
            3]:
            # recur the function, it will keep recuring until the coordinates are not on a cabbage patch.
            add_sheep(randint(50, 1150), randint(50, 650), sheep1)
            return None
            # add a sheep to the canvas once the x and y coordinates do not clash with a cabbage patch
    temp_sheep_widget = main_canvas.create_image(x, y, image=item, anchor=NW)
    existing_sheep_widget.append(temp_sheep_widget)
    existing_sheep.append([x, y])


def add_hay(x, y, item):
    """ Add hay images to the canvas at random locations function"""
    s = 0
    for s in range(0, len(existing_farms)):
        ''' This code below will make sure hay bales dont spawn on top of eachother'''
        if x > existing_farms[s][0] and x < existing_farms[s][1] and y > existing_farms[s][2] and y < existing_farms[s][
            3]:
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
    '''Adds more farms when button is pressed'''
    add_cabbage_field(randint(100, 1100), randint(50, 600), (rw * 10), (rh * 10), cabbage_texture, tractor)


def hay_button():
    """Button for connecting the button being pressed by the user to the function to create the hay on the screen"""
    add_hay(randint(50, 1150), randint(50, 650), haybail)


def go_start_field(tractor, farm_x, farm_y):
    """Function to go to the start of the farm to start cropping the contents of it"""
    move_widget(tractor, farm_x, farm_y)


def sheep_button():
    """ Button to connect button being pressed by the user to function to draw the sheep on the screen"""
    add_sheep(randint(50, 1150), randint(50, 650), sheep1)


"""Addin things to the scence(Fences,CabbageFields)"""


def add_things_canvas():
    add_cabbage_field(100, 50, (rw * 10), (rh * 10), cabbage_texture, tractor)
    add_cabbage_field(300, 220, (rw * 10), (rh * 10), cabbage_texture, tractor)
    fence(1, (y_max) - 10, (x_max), int(10), fence_img)
    fence(1, (y_min) + 5, (x_max), int(10), fence_img)
    fence(1, 1, (x_min) + 5, (y_max), side_fence)
    fence(1195, 1, (x_min) + 5, (y_max), side_fence)


def main():
    global main_canvas, tractor, x_max, y_max, barn, fence_img
    """Main function to make canvas and multiple things in it, also includes multiple variables and imports of images etc."""
    root.tk.call('wm', 'iconphoto', root._w, icon)  # Changes the application icon
    main_canvas = Canvas(width=1200, height=720, bg='white')
    x_max = int(main_canvas['width'])
    y_max = int(main_canvas['height'])
    main_canvas.pack(expand=YES, fill=BOTH)
    main_canvas.create_image(0, 0, image=bck_img, anchor=NW)  # Sets background of the window to grass# create canvas
    button = Button(main_canvas, width=30, text='Add Sheep', command=sheep_button, bg='light green')
    button_haybail = Button(main_canvas, width=30, text="Add Hay Bails", command=hay_button)
    button_farm = Button(main_canvas, width=30, text='Add Farm', command=lambda: farm_button(tractor))
    button.configure(width=10)
    button_haybail.configure(width=10)
    barn = main_canvas.create_image(x_max - 10, y_min + 20, image=barn_img, anchor=NE)
    button1 = main_canvas.create_window(1, (y_max) - 30, anchor=NW, window=button)
    button2 = main_canvas.create_window(130, (y_max) - 30, anchor=NW, window=button_haybail)
    button3 = main_canvas.create_window(260, (y_max) - 30, anchor=NW, window=button_farm)
    tractor = main_canvas.create_image(300, 200, image=tractor_img, anchor=NW)  # adding tractor to the canvas
    Label(root, textvariable=global_cabbage_var).pack()
    '''Calls upon add_things_function above'''
    add_things_canvas()
    return


""" Boundaries detection"""


def boundaries_detect():
    global vx, vy
    cabbages_global = 0
    while True:
        x1, y1 = main_canvas.coords(tractor)
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
            global_cabbage_var.set("Barn cabbages: " + str(cabbages_global))
            continue
        if inside_farm(tractor) == False or existing_farms[v][4] == "empty":
            move_widget(tractor, x1 + vx, y1 + vy)

        sheep_movement()
        time.sleep(0.01)
    return

    mainloop()


main()
boundaries_detect()

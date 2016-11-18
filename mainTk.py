from tkinter import *
from random import randint
import time
import pyaudio
import wave
def sound_bounce():
    try:           
        chunk = 1024

        f = wave.open("/Users/Max/Documents/CabbagePatch/AI-Farming-Simulator/Audio/bounce.wav","rb")
        p = pyaudio.PyAudio()

        stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                        channels = f.getnchannels(),
                        rate = f.getframerate(),
                        output = True)

        data = f.readframes(chunk)

        while len(data) > 0:
            stream.write(data)
            data = f.readframes(chunk)

            stream.stop_stream()
            stream.close()

            p.terminate()
    except OSError:
            print("Hello")
                
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
    existing_farms_x1.append(x)
    existing_farms_x2.append(x+l)
    existing_farms_y1.append(y)
    existing_farms_y2.append(y+w)
    existing_farms_type.append("grown")
    print(existing_farms_x1,existing_farms_x2,existing_farms_y1,existing_farms_y2, existing_farms_type)
def fence(x,y,l,w,item):
    """ Will make fence tileable (used in bottom of page) can be used later for
    animal fencing etc.)"""
    for a in range(x,l+x,10):
        for b in range(y,w+y,10):
            main_canvas.create_image(a,b,image=item,anchor = NW)
def inside_farm(tractor):
    """ Checks if the tractor is inside the farm.
        More specifcally it checks if the top left coordinate is inside the area marked by any of the cabbage fields 
        on the screen, if they were added using add_cabbage_field function
        Returns a boolean result. True if tractor is inside a farm.
        i is a global variable, sygnaling which farm the tractor is on, do not reassign else where"""
    x,y= main_canvas.coords(tractor)
    global i
    i = 0
    while i < len(existing_farms_x1):
        if x > existing_farms_x1[i] and x< existing_farms_x2[i] and y > existing_farms_y1[i] and y<existing_farms_y2[i]:
            return True
        else:
            status = False
        i+=1
    return status
def collect_cabbage(tractor,farm_x,farm_y, farm_x2, farm_y2,texture,trac_img):
    """Collects cabbage function"""
    farm_length = farm_x2 - farm_x
    farm_height = farm_y2 - farm_y
    cabbage_count = 0
    for k in range(0, farm_height,10):
        for w in range(0,farm_length,10):
            move_widget(tractor,farm_x+w,farm_y+k)
            trac_x,trac_y = main_canvas.coords(tractor)
            main_canvas.create_image(trac_x,trac_y,image=texture, anchor=NW)
            cabbage_count+=1
            print(cabbage_count)
            time.sleep(0.09)
    existing_farms_type[i] = "empty"
    main_canvas.tag_raise(tractor)
    return cabbage_count
def add_sheep (x,y,item):
    '''This adds an image of a sheep to the canvas'''
    main_canvas.create_image(x,y, image=item, anchor = NW,)
def fence(x,y,l,w,item):
    """ Will make fence tileable (used in bottom of page) can be used later for
    animal fencing etc.)"""
    for a in range(x,l+x,10):
        for b in range(y,w+y,10):
            main_canvas.create_image(a,b,image=item,anchor = NW)
def go_start_field(tractor, farm_x, farm_y):
    move_widget(tractor,farm_x,farm_y)
def sheep_button():
    add_sheep(randint(1, 1200), randint(1, 720), sheep1)
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
    bck_img = PhotoImage(file="textures/background.gif")
    main_canvas.create_image(0,0,image=bck_img,anchor=NW) # Sets background of the window to grass
    main_canvas.create_image(0,0,image=bck_img,anchor=NW) # Sets background of the window to grass
    x_min = 0 # min and max values used in setting boundaries on the canvas
    y_min= 0  # max values also used in setting starting coordinates for tractor
    x_max=int(main_canvas['width'])
    y_max=int(main_canvas['height'])
    rh= randint(8,12)
    rw = randint(10,14)
    global existing_farms_x1,existing_farms_x2, existing_farms_y1, existing_farms_y2, existing_farms_type
    dirt_texture = PhotoImage(file="textures/dirt.gif")
    cabbage_texture = PhotoImage(file="textures/cabbage.gif")
    existing_farms_x1,existing_farms_x2, existing_farms_y1, existing_farms_y2, existing_farms_type = [],[],[],[],[]
    add_cabbage_field(100,50,(rw*10),(rh*10),cabbage_texture)
    add_cabbage_field(300,220,(rw*10),(rh*10),cabbage_texture)
    fence(1,((y_max)-10),(x_max),int(10),fence_img)
    fence(1,(y_min)+5,(x_max),int(10),fence_img)
    fence(1,1,(x_min)+5,(y_max),side_fence)
    fence(1195,1,(x_min)+5,(y_max),side_fence)
    global sheep1
    sheep1=PhotoImage(file='textures/sheep.gif')
    button = Button(main_canvas, width=30, text = 'Add Sheep', command = sheep_button, bg='light green')
    button.configure(width=10)
    button1 = main_canvas.create_window(1,(y_max)-30,anchor=NW,window=button)
    print(existing_farms_x1)
    tractor_img = PhotoImage(file="textures/tractor_right.gif")
    tractor1 = main_canvas.create_image(300,200,image=tractor_img, anchor = NW) #adding tractor to the canvas
    vx = -1
    vy = -1
    cabbages_global = 0
    while True:
        x1,y1= main_canvas.coords(tractor1)
        if (x1+20)> x_max and inside_farm(tractor1)==False:
            sound_bounce()
            vx=-1
        if (y1+25)> y_max and inside_farm(tractor1)==False:
            sound_bounce()
            vy=-1
        if (y1)<y_min and inside_farm(tractor1)==False:
            sound_bounce()
            vy = 1
        if (x1)<x_min and inside_farm(tractor1)==False:
            sound_bounce()
            vx=1
        if inside_farm(tractor1) == True and existing_farms_type[i]=="grown":
            cabbages_global+=collect_cabbage(tractor1, existing_farms_x1[i],existing_farms_y1[i],existing_farms_x2[i],existing_farms_y2[i],dirt_texture,tractor_img)
            print(cabbages_global)
            continue
        if inside_farm(tractor1) == False or existing_farms_type[i] == "empty":
            move_widget(tractor1, x1+vx, y1+vy)
        time.sleep(0.01)
    mainloop()
main()


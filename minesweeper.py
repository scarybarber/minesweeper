import tkinter as tk
import random
import tkinter.messagebox as messagebox


# mine counting for 8 adjacent buttons

def mine_count(i,j):
    global mine_position
    count = 0
    adjacent_offsets = [
          (-1,-1,),(-1,0),(-1,1),
          (0,1),        (0,-1),
          (1,-1),(1,0),(1,1)
            ]
    for dx,dy in adjacent_offsets:
        ni,nj = i + dx, j+ dy
        if (ni,nj) in mine_position:
                count += 1
        
    return count


# non-mine buttons counting for 8 adjacent buttons
def is_zero_count(i,j):
    return mine_count(i,j) == 0 



def adjacent_zero_search(i,j):
    adjacent_zero_count = []
    adjacent_offsets = [
          (-1,-1,),(-1,0),(-1,1),
          (0,1),    (0,-1),
          (1,-1),(1,0),(1,1)
    ]
    processed = {(i,j)}

    reveal_number(i,j)

    if is_zero_count(i,j):
        for dx,dy in adjacent_offsets:
            ni,nj = i + dx, j+ dy
            if (ni,nj) not in processed and ni >=0 and nj >=0 and ni < rows and nj < rows:
                adjacent_zero_count.append((ni,nj))  
            
    while len(adjacent_zero_count) != 0:
        ni, nj = adjacent_zero_count [0]
        reveal_number(ni,nj)
        adjacent_zero_count.remove((ni,nj))
        processed.add((ni,nj))    
        if is_zero_count(ni,nj):
            for dx,dy in adjacent_offsets:
                mi,mj = ni + dx, nj+ dy
                if (mi,mj) not in processed and mi >=0 and mj >=0 and mi < rows and mj < rows:
                    adjacent_zero_count.append((mi,mj))
                   

            

# mine or number

def reveal_number(i,j):
    global buttons_checked
    buttons_checked = []
    for i2,j2,bt in buttons:
        if (i2,j2) == (i,j):
            if (i,j) in mine_position:
                canvas.itemconfig(bt, fill = 'white')
                x0, y0, x1, y1 = canvas.coords(bt)
                cx = (x0 + x1) / 2
                cy = (y0 + y1) / 2
                canvas.create_text(cx, cy, text= '💣', font= ("Arial", 14))
                messagebox.showinfo("You Lose!", " BOMB 💥")
                reset_game()
            else:
                canvas.itemconfig(bt, fill = 'white')
                count = mine_count(i,j)
                if count > 0:
                    x0, y0, x1, y1 = canvas.coords(bt)
                    cx = (x0 + x1) / 2
                    cy = (y0 + y1) / 2
                    canvas.create_text(cx, cy, text= str(count), font= ("Arial", 14, "bold"))
            break
        buttons_checked.append((i2,j2,bt))
        check_win()


# bind two functions on same click

def on_left_click(i,j):
    def handler(event):
        if (i,j) in mine_position or mine_count(i,j) != 0:
            reveal_number(i,j)
        else:
            adjacent_zero_search(i,j)
    return handler



# set up a flag

flag_position = set()

def flag(i,j):
    def handle(event):
        for i3,j3,bt in buttons:
            if (i3,j3) == (i,j):
                if (i,j) not in flag_position:
                    flag_position.add((i,j))
                    canvas.itemconfig(bt, fill = 'white')
                    x0, y0, x1, y1 = canvas.coords(bt)
                    cx = (x0 + x1) / 2
                    cy = (y0 + y1) / 2
                    canvas.create_text(cx, cy, text= '🚩', font= ("Arial", 14))
                    check_win()
                else:
                    flag_position.remove((i,j))
                    canvas.itemconfig(bt, fill = 'lightblue')
                    canvas.itemconfig(texts[(i,j)], text='')
                break
    return handle 



# win: when all the buttons are revealed

def check_win():
    if flag_position == mine_position and len(buttons_checked) == 100:
        messagebox.showinfo("You Win!", "🎉 Congratulations!")




# reset game

def reset_game():
    global buttons, mine_position, flag_position, texts
    flag_position = set()
    texts = {}

    canvas.delete("all")
    
    buttons = []
    button_position = [(i,j) for i in range(rows) for j in range(cols)]
    mine_position = set(random.sample(button_position,15))

    for i in range(rows):
        for j in range(cols):
            x0 = gap + j * ( button_size+ gap)
            y0 = gap + i * ( button_size + gap)
            x1 = x0 + button_size
            y1 = y0 + button_size

            bt = canvas.create_rectangle(x0,y0,x1,y1, fill= "lightblue", outline= "black")
            tag = f"cell_{i}_{j}"
            texts[(i,j)] = canvas.create_text((x0+x1)/2, (y0+y1)/2, text= '', font= ("Arial", 14), tags=f"text_{i}_{j}")
            canvas.itemconfig(bt, tags = tag)
            canvas.tag_bind(tag, '<Button-1>', on_left_click(i,j))
            canvas.tag_bind(tag, '<Button-2>', flag(i,j))
            buttons.append((i, j, bt))





## set up the window

window = tk.Tk()
window.geometry('370x420')
window.title("Minesweeper")

# restart button 

restart_btn = tk.Button(window, text="Restart", command=reset_game)
restart_btn.pack(pady= 10)

# create canvas

canvas = tk.Canvas(window, width=350, height=350, bg='lightgrey')
canvas.pack(anchor=tk.CENTER, expand=True)

# button size

button_size = 30
gap = 5
rows = 350 // (button_size+gap)
cols = 350 // (button_size+gap)

buttons = []
button_position = [(i,j) for i in range(rows) for j in range(cols)]

# randomly select 10 buttons as "mines" in the rest of the space

mine_position = set(random.sample(button_position,15))

texts = {}




## interface design

for i in range(rows):
    for j in range(cols):
        x0 = gap + j * ( button_size+ gap)
        y0 = gap + i * ( button_size + gap)
        x1 = x0 + button_size
        y1 = y0 + button_size

        bt = canvas.create_rectangle(x0,y0,x1,y1, fill= "lightblue", outline= "black")
        tag = f"cell_{i}_{j}"
        canvas.itemconfig(bt, tags = tag)

        # every left click on button reveal mine, number or flood reveal

        canvas.tag_bind(tag, '<Button-1>', on_left_click(i,j))

        # every right click on button mark a flag 

        canvas.tag_bind(tag, '<Button-2>', flag(i,j))

        buttons.append((i, j, bt))
        
        # every click on non-mine button reveals all adjacent non-mine buttons

        

window.mainloop()








# from tkinter import *
# root = Tk()
# prompt = '      Press any key      '
# label1 = Label(root, text=prompt, width=len(prompt), bg='yellow')
# label1.pack()
# def key(event):
#     if event.char == event.keysym:
#         msg = 'Normal Key %r' % event.char
#     elif len(event.char) == 1:
#         msg = 'Punctuation Key %r (%r)' % (event.keysym, event.char)
#     else:
#         msg = 'Special Key %r' % event.keysym
#     label1.config(text=msg)
# root.bind_all('<Control-Key-C>', key)
# root.bind_all('<Control-Key-1>', key)
# root.bind_all('<Control-Key-2>', key)
# root.bind_all('<Control-Key-/>', key)
# root.mainloop()
import tkinter as tk

def left_click(event):
    event.widget.configure(bg="green")

def right_click(event):
    event.widget.configure(bg="red")

# root = tk.Tk()
# button = tk.Frame(root, width=20, height=20, background="gray")
# button.pack(padx=20, pady=20)

# # button.bind("<Button-1>", left_click)
# button.bind("<Button-2>", right_click)
# button.bind("<Button-3>", right_click)
# root.bind_all('<Control-Key-C>', left_click)
def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y
    print(lasx, lasy)

# def draw_smth(event):
#     global lasx, lasy
#     canvas.create_line((lasx, lasy, event.x, event.y), 
#                       fill='red', 
#                       width=2)
#     lasx, lasy = event.x, event.y
def quit(event):
    print("you pressed control-forwardslash")
    get_x_and_y(event)
    # root.quit()

root = tk.Tk()
root.bind('<Control-1>', quit)      # forward-slash
# root.bind('<Control-backslash>', quit)  # backslash
root.mainloop()
# root.mainloop()
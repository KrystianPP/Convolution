import cv2
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog


def load_img():
    # loading image from given directory, processing and displaying it
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select image",
                                               filetypes=(("png files", "*.png"),
                                                          ("all files", "*.*")))
    hold = Canvas(root, width=200, height=200)
    hold.place(x=30, y=100)
    img = cv2.imread(root.filename)
    root.shape = np.flip(img.shape[:2])

    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        root.rgb = True
    elif img.ndim == 2:
        root.rgb = False
    else:
        raise TypeError("Wrong type of image")

    img = cv2.resize(img, (200, 200))
    img = ImageTk.PhotoImage(image=Image.fromarray(img))
    root.one = img
    hold.create_image(0, 0, image=img, anchor='nw')


def convolve():
    # convolution of image with given mask and displaying it
    global mask_elem
    if mask_elem is None:
        raise ValueError('Missing elements in mask')
    else:
        new_mask = [float(ele.get()) for ele in mask_elem]
        shape = int(np.sqrt(len(new_mask)))
        kernel = np.array(new_mask).reshape(shape, shape)
    input = np.array(ImageTk.getimage(root.one))
    if root.rgb:
        input = cv2.cvtColor(input, cv2.COLOR_RGBA2RGB)

    img = cv2.filter2D(input, -1, kernel)
    hold2 = Canvas(root, width=200, height=200)
    hold2.place(x=570, y=100)
    img = ImageTk.PhotoImage(image=Image.fromarray(img))
    root.two = img
    hold2.create_image(0, 0, image=img, anchor='nw')


def mask_3():
    # placing rectangle on the area where 5x5 mask were previously
    # then making 3x3 mask where user can type values
    w = Canvas(root, width=220, heigh=200)
    w.place(x=280, y=180)
    w.create_rectangle(0, 0, 500, 500)
    global mask_elem
    mask_elem = []
    row, col = 0, 0
    for i in range(1, 10):
        mask_elem.append(Entry(root, width=5))
        mask_elem[i-1].place(x=340 + row, y=180 + col)
        row += 40
        if i % 3 == 0:
            row = 0
            col += 25


def mask_5():
    # making 5x5 mask where user can type values
    global mask_elem
    mask_elem = []
    row, col = 0, 0
    for i in range(1, 26):
        mask_elem.append(Entry(root, width=5))
        mask_elem[i-1].place(x=300 + row, y=180 + col)
        row += 40
        if i % 5 == 0:
            row = 0
            col += 25


def save():
    # saving image with following numbers in file names
    global num
    if root.rgb:
        img = cv2.cvtColor(np.array(ImageTk.getimage(root.two)), cv2.COLOR_BGR2RGB)
    else:
        img = np.array(ImageTk.getimage(root.two))
    cv2.imwrite(f'Convolved{num}.png', cv2.resize(img, root.shape))
    num += 1


num = 0  # variable used in save function
root = Tk()
var = IntVar()
root.geometry('800x480')

# initializing buttons
b1 = Button(root, text='Wczytaj zdjęcie', command=load_img)
b2 = Button(root, text="Wykonaj konwolucje", command=convolve)
b3 = Button(root, text='Zapisz obraz', command=save)
r1 = Radiobutton(root, text='Maska 3x3', variable=var, value=1, command=mask_3)
r2 = Radiobutton(root, text='Maska 5x5', variable=var, value=2, command=mask_5)

# locating buttons on proper place
b1.place(x=40, y=420)
b2.place(x=330, y=420)
b3.place(x=650, y=420)
r1.place(x=350, y=100)
r2.place(x=350, y=120)

root.mainloop()

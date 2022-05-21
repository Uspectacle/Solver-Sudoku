import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import numpy as np
import pytesseract
import cv2
from PIL import ImageGrab, ImageTk
import pyautogui
from tkinter import *
import PIL.Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def clean(entry, get=True):
    string = entry.get() if get else str(entry)
    digits = [s for s in string if s.isdigit()]
    if len(digits):
        return int(digits[0])
    return 0

def write(entry, text):
    entry.delete(0, END)
    entry.insert(0, f'{text}')
    return

def imageToString(image):
    return pytesseract.image_to_string(cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY), lang ='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

class CaptureWindow():
    def __init__(self):
        self.bgColor = "#404040"
        self.fgColor = "#F0F0F0"
        self.canvasSize = 500
        self.cellSize = 30
        self.originRect = None
        self.endRect = None
        self.build_root()
        self.build_grid()
        self.build_buttons()
        self.build_boxEntry()
        self.build_canvas()

        self.root.mainloop()
        return

    def build_root(self):
        self.root = Tk()
        self.root.title('Capture')
        self.root.geometry("480x720")
        self.root.minsize(650, 720)
        self.root.iconbitmap("pumpkinicon.ico")
        self.root.config(background=self.bgColor)
        return

    def paintCanvas(self):
        self.canvas.create_image(self.canvasSize//2, self.canvasSize//2, image=self.showCap)
        self.canvas.create_line(self.canvasSize//3, 0, self.canvasSize//3, self.canvasSize)
        self.canvas.create_line(2*self.canvasSize//3, 0, 2*self.canvasSize//3, self.canvasSize)
        self.canvas.create_line(0, self.canvasSize//3, self.canvasSize, self.canvasSize//3)
        self.canvas.create_line(0, 2*self.canvasSize//3, self.canvasSize, 2*self.canvasSize//3)
        return

    def capture(self):
        self.cap = ImageGrab.grab()
        showCap = self.cap.resize((self.canvasSize, self.canvasSize))
        self.showCap = ImageTk.PhotoImage(showCap)
        self.paintCanvas()
        self.originRect, self.endRect, self.coordRect = None, None, None
        self.coordBox = (0, 0) + self.cap.size
        write(self.boxEntry, self.coordBox)
        return

    def build_grid(self):
        self.grid = Frame(self.root)
        self.grid.pack()

        self.matrix = np.array([[Entry(self.grid, bg=self.bgColor, fg=self.fgColor, width=3) for colIdx in range(9)] for rowIdx in range(9)])
        for rowIdx in range(9):
            for colIdx in range(9):
                self.matrix[rowIdx, colIdx].grid(row=rowIdx+rowIdx//3, column=colIdx+colIdx//3)
        return
    
    def build_buttons(self):
        self.buttons = Frame(self.root)
        self.buttons.pack( side = BOTTOM )

        self.exitButton = Button(self.buttons, text = 'Exit', fg ='red', command=self.root.destroy, bg=self.bgColor)
        self.exitButton.pack( side = LEFT)
        self.captureButton = Button(self.buttons, text = 'Capture', fg=self.fgColor, command=self.capture, bg=self.bgColor)
        self.captureButton.pack( side = LEFT)
        self.resizeButton = Button(self.buttons, text = 'Resize', fg=self.fgColor, command=self.resize, bg=self.bgColor)
        self.resizeButton.pack( side = LEFT)
        self.matrixButton = Button(self.buttons, text = 'Compute Matrix', fg=self.fgColor, command=self.computeMatrix, bg=self.bgColor)
        self.matrixButton.pack( side = LEFT)
        self.saveButton = Button(self.buttons, text = 'Save', fg=self.fgColor, command=self.save, bg=self.bgColor)
        self.saveButton.pack( side = LEFT)
        return
    
    def build_canvas(self):
        self.canvas = Canvas(self.root, width = self.canvasSize, height = self.canvasSize)      
        self.canvas.pack( side = BOTTOM )
        self.capture()
        self.canvas.bind('<ButtonRelease-1>', self.newOrigine)
        return
    
    def build_boxEntry(self):
        self.boxEntry = Entry(bg = self.bgColor, fg = self.fgColor)
        self.boxEntry.pack( side = BOTTOM )
        self.boxEntry.bind('<Return>', self.updateBox)
        return

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        if 'alpha' in kwargs:
            alpha = int(kwargs.pop('alpha') * 255)
            fill = kwargs.pop('fill')
            fill = self.root.winfo_rgb(fill) + (alpha,)
            rectangle = PIL.Image.new('RGBA', (x2-x1, y2-y1), fill)
            self.canvas.rectangle = ImageTk.PhotoImage(rectangle)
            self.canvas.create_image(x1, y1, image=self.canvas.rectangle, anchor='nw')
        self.canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
        return

    def computeMatrix(self):
        if self.coordRect == None:
            matrixImage = self.cap.crop(self.coordBox)
        else:
            matrixImage = self.cap.crop(self.coordRect)
        matrixImage = matrixImage.resize((self.cellSize*9, self.cellSize*9))
        for rowIdx in range(self.matrix.shape[0]):
            for colIdx in range(self.matrix.shape[0]):
                box = np.array([colIdx, rowIdx, colIdx+1, rowIdx+1]) * self.cellSize
                digit = clean(imageToString(matrixImage.crop(box)), get = False)
                string = str(digit) if digit else ''
                write(self.matrix[rowIdx, colIdx], string)
        return

    def newOrigine(self, event):
        self.paintCanvas()
        if self.originRect != None:
            self.endRect = self.originRect
        self.originRect = event.x, event.y
        self.paint()
        x, y = self.originRect
        self.canvas.create_oval(x-2, y-2, x+2, y+2, fill='red', outline='red')
        return

    def paint(self):
        if self.endRect == None:
            return
        x1, y1 = self.originRect
        x2, y2 = self.endRect
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        self.create_rectangle(x1, y1, x2, y2, fill='blue', outline='blue', alpha=0.2)
        bx1, by1, bx2, by2 = self.coordBox
        x1 = bx1 + (bx2 - bx1) * x1 / self.canvasSize
        x2 = bx1 + (bx2 - bx1) * x2 / self.canvasSize
        y1 = by1 + (by2 - by1) * y1 / self.canvasSize
        y2 = by1 + (by2 - by1) * y2 / self.canvasSize
        self.coordRect = (int(x1), int(y1), int(x2), int(y2))
        return

    def updateBox(self, event):
        text = self.boxEntry.get()
        print(text)
        text = text.replace("(", "")
        text = text.replace(")", "")
        text = text.replace(" ", "")
        print(text)
        text = text.split(',')
        print(text)
        text = [coord.split('.')[0] for coord in text]
        print(text)
        text = [int(coord) for coord in text if coord.isdigit()]
        if len(text) != 4:
            print(f'ERROR, self.boxEntry.get(): {self.boxEntry.get()} and coords: {text}')
            return
        x1, y1, x2, y2 = text
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        xmax, ymax = self.cap.size
        x1 = min(xmax, max(0, x1))
        x2 = min(xmax, max(0, x2))
        y1 = min(ymax, max(0, y1))
        y2 = min(ymax, max(0, y2))
        self.coordRect = (x1, y1, x2, y2)
        self.resize()
        return

    def resize(self):
        if self.coordRect == None:
            return
        self.coordBox = self.coordRect
        write(self.boxEntry, self.coordBox)
        showCap = self.cap.crop(self.coordBox)
        showCap = showCap.resize((self.canvasSize, self.canvasSize))
        self.showCap = ImageTk.PhotoImage(showCap)
        self.paintCanvas()
        self.originRect, self.endRect, self.coordRect = None, None, None
        return

    def save(self):
        f = np.vectorize(clean)
        np.save(f"savedSudoku\\{time.time()}.npy", f(self.matrix))
        return

if __name__ == "__main__":
    CaptureWindow()

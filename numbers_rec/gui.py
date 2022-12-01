from tkinter import *
import tkinter as tk
from PIL import ImageGrab, Image, ImageEnhance
import pytesseract


def predict_digit(image):
    enhancer = ImageEnhance.Contrast(image)
    img = enhancer.enhance(2)

    thresh = 200
    fn = lambda x: 255 if x > thresh else 0
    res = img.convert('L').point(fn, mode='1')
    res.save("bw.png", "png")
    text = pytesseract.image_to_string(res, lang='eng', config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    return text


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.x = self.y = 0

        # Создание элементов
        self.canvas = tk.Canvas(self, width=300, height=300, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Думаю..", font=("Helvetica", 48))
        self.classify_btn = tk.Button(self, text="Распознать", command=self.classify_handwriting)
        self.button_clear = tk.Button(self, text="Очистить", command=self.clear_all)

        # Сетка окна
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.classify_btn.grid(row=1, column=1, pady=2, padx=2)
        self.button_clear.grid(row=1, column=0, pady=2)

        self.mouse_pressed = False

        self.canvas.bind("<B1-Motion>", func=self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, outline='black', fill='black')

    def get_pic_from_canvas(self, widget):
        x = self.winfo_rootx() + widget.winfo_x()
        y = self.winfo_rooty() + widget.winfo_y() + 50
        x1 = x + widget.winfo_width() + 320
        y1 = y + widget.winfo_height() + 320
        return ImageGrab.grab().crop((x, y, x1, y1))

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()
        img = self.get_pic_from_canvas(self.canvas)
        img.save("img.png", "png")
        prediction = predict_digit(img)
        self.label.configure(text=str(prediction) + "Наверное")


app = App()
mainloop()

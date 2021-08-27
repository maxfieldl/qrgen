import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
from PIL import Image, ImageTk
import qrcode
import os
import sys
import webbrowser


class QrCodeGenerator(tk.Tk):
    """Main class for the GUI"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    """Start page of the GUI"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="QR Code Generator",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = ttk.Button(self, text="Generate QR Code",
                             command=lambda: controller.show_frame("PageOne"))
        button2 = ttk.Button(self, text="About",
                             command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()


class PageOne(tk.Frame):
    """Page to generate QR Code"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Generate QR Code",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        self.url = tk.StringVar()
        self.url.set("Enter URL")
        self.url_entry = tk.Entry(self, textvariable=self.url, width=50)
        self.url_entry.pack()
        self.url_entry.bind("<Button-1>", self.clear_widget)
        self.url_entry.bind("<Return>", self.generate_qr)
        self.url_entry.focus()
        self.qr_img = tk.Label(self)
        self.qr_img.pack()
        button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def clear_widget(self, event):
        """Clear the content of the entry widget"""
        if self.url_entry == self.url_entry.focus_get() and self.url_entry.get() == "Enter URL":
            self.url_entry.delete(0, "end")

    def generate_qr(self, event):
        """Generate QR Code"""
        if self.url_entry.get() == "Enter URL":
            self.url_entry.delete(0, "end")
        url = self.url_entry.get()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qr.png")
        self.qr_img.img = ImageTk.PhotoImage(Image.open("qr.png"))
        self.qr_img.config(image=self.qr_img.img)


class PageTwo(tk.Frame):
    """Page to show about information"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="About", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack()
        link = tk.Label(self, text="Github", fg="blue", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", self.open_github)

    def open_github(self, event):
        """Open the github link"""
        webbrowser.open_new(r"https://github.com/maxfieldl/qrgen")


if __name__ == "__main__":
    app = QrCodeGenerator()
    app.mainloop()

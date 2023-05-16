import tkinter as tk
from tkinter import filedialog
import qrcode
from PIL import Image, ImageTk


class QRCodeGeneratorGUI:
    """
    GUI for a QR Code Generator\n
    Author: Pedro Henrique Gonçalves Pires\n
    Date: 15/05/2023\n
    """
    def __init__(self):
        # Variables
        self.qr_code_image: Image = None
        self.qr_code_image_to_display: ImageTk.PhotoImage = None
        self.logo_image: Image = None

        # Fonts
        label_font = ('Roboto', 14, 'bold')
        desc_font = ('Roboto', 10, 'bold')
        input_font = ('Roboto', 12)
        button_font = ('Roboto', 12)
        bg_color = '#3F3F3F'
        input_bg_color = '#7A7A7A'
        input_fg_color = 'white'
        button_bg_color = '#008000'
        remove_button_bg_color = '#FF0000'

        window_width = 800
        window_height = 875

        # Create the window
        self.master = tk.Tk()
        self.master.protocol("WM_DELETE_WINDOW", self.quit_me)
        self.master.title("QR Code Generator")
        self.master.iconphoto(False, tk.PhotoImage(file="app_logo.png"))
        self.master.geometry(f'{window_width}x{window_height}')
        self.master.config(bg=bg_color)

        # Create the url entry
        self.url_frame = tk.Frame(self.master, bg=bg_color)
        self.url_frame.pack(pady=10)
        self.url_label = tk.Label(self.url_frame, text="Enter Data:", font=label_font, bg=bg_color, fg=input_fg_color)
        self.url_label.pack(pady=10)
        self.url_entry = tk.Text(self.url_frame, width=25, height=1, font=input_font, bg=input_bg_color,
                                 fg=input_fg_color, borderwidth=0)
        self.url_entry.pack(side=tk.LEFT)
        self.url_scrollbar = tk.Scrollbar(self.url_frame, orient=tk.VERTICAL, command=self.url_entry.yview,
                                          bg=input_bg_color)
        self.url_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.url_entry.config(yscrollcommand=self.url_scrollbar.set)

        # Bind the "<KeyRelease>" event to the url entry widget
        self.url_entry.bind("<KeyRelease>", self.resize_url_entry)

        # Create the load image button
        self.load_image_frame = tk.Frame(self.master, bg=bg_color)
        self.load_image_frame.pack(pady=10)
        self.load_image_button = tk.Button(self.load_image_frame, text="Load Image", font=button_font, command=self.load_image,
                                           relief=tk.FLAT, bg=button_bg_color, fg=input_fg_color)
        self.load_image_button.pack(side=tk.LEFT)
        self.load_image_name = tk.Label(self.load_image_frame, text="No image loaded", font=desc_font, bg=input_bg_color,
                                        fg=input_fg_color, wraplength=int(window_width*0.67))
        self.load_image_name.pack(side=tk.LEFT, padx=10)
        self.load_image_remove = tk.Button(self.load_image_frame, text="X", font=button_font, command=self.remove_image,
                                           relief=tk.FLAT, bg=remove_button_bg_color, fg=input_fg_color)
        self.load_image_remove.pack(side=tk.RIGHT)

        # Create the generate button
        self.generate_button = tk.Button(self.master, text="Generate QR Code", font=button_font,
                                         command=self.generate_qr_code, relief=tk.FLAT, bg=button_bg_color,
                                         fg=input_fg_color)
        self.generate_button.pack(pady=10)

        # Create the canvas that displays the QR Code
        self.qr_code_canvas = tk.Canvas(self.master, width=500, height=500, bg=input_bg_color, highlightbackground=button_bg_color)
        self.qr_code_canvas.pack(pady=20)

        # Create the save button
        self.save_button = tk.Button(self.master, text="Save QR Code", font=button_font, command=self.save_qr_code,
                                     relief=tk.FLAT, bg=button_bg_color, fg=input_fg_color)
        self.save_button.pack(pady=10)

    def resize_url_entry(self, event):
        """
        Resize the url entry widget according to the size of the text
        """
        minimun_width = 25
        maximun_width = 75
        minimun_height = 1
        maximun_height = 5

        url_size: int = len(self.url_entry.get("1.0", tk.END))
        if url_size <= minimun_width:
            self.url_entry.config(width=minimun_width, height=minimun_height)
            return
        if url_size <= maximun_width:
            self.url_entry.config(width=url_size, height=minimun_height)
            return

        qt_lines = (url_size // 75) + 1
        self.url_entry.config(width=maximun_width, height=qt_lines if (qt_lines <= maximun_height) else maximun_height)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.logo_image = Image.open(file_path).convert("RGBA")
            self.load_image_name.config(text=file_path)

    def remove_image(self):
        self.logo_image = None
        self.load_image_name.config(text="Image removed")

    def generate_qr_code(self):
        """
        Generate the QR Code and display it in the canvas
        """
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=1)  # Create a QR Code object

        data = self.url_entry.get("1.0", tk.END)  # Get the data from the entry
        qr.add_data(data)  # Add the data to the QR Code object
        qr.make()  # Generate the QR Code
        qr_code = qr.make_image(fill_color="black", back_color="white")  # Generate the QR Code image

        self.qr_code_image: Image = ImageTk.getimage(ImageTk.PhotoImage(qr_code))  # Create the QR Code Image

        # If an image has been loaded, paste it into the center of the new image
        if self.logo_image:
            # Resize the image to fit inside the QR Code
            self.logo_image = QRCodeGeneratorGUI.resize_image(self.logo_image,
                                                              self.qr_code_image.width*0.4,
                                                              self.qr_code_image.height*0.4)
            # Calculate the x and y coordinates of the center of the new image
            x = (self.qr_code_image.width - self.logo_image.width) // 2
            y = (self.qr_code_image.height - self.logo_image.height) // 2
            # Paste the logo image into the QR Code image
            self.qr_code_image.paste(self.logo_image, (x, y, x + self.logo_image.width, y + self.logo_image.height), mask=self.logo_image)

        # Create a PhotoImage object from the QR Code image
        self.qr_code_image_to_display = ImageTk.PhotoImage(QRCodeGeneratorGUI.resize_image(self.qr_code_image,
                                                                                           self.qr_code_canvas.winfo_width() - 30,
                                                                                           self.qr_code_canvas.winfo_height() - 30))

        # Calculate the x and y coordinates of the center of the canvas
        x = (self.qr_code_canvas.winfo_width() - self.qr_code_image_to_display.width()) / 2
        y = (self.qr_code_canvas.winfo_height() - self.qr_code_image_to_display.height()) / 2

        # Create the QR Code image in the canvas
        self.qr_code_canvas.create_image(x, y, anchor="nw", image=self.qr_code_image_to_display)

    def save_qr_code(self):
        """
        Save the QR Code image
        """
        if self.qr_code_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG Image', '*.png')])
            if file_path:
                # If the QR Code image is a PhotoImage object, convert it to a PIL Image object
                self.qr_code_image.save(file_path)

    def run_app(self):
        self.master.mainloop()

    def quit_me(self):
        self.master.quit()
        self.master.destroy()

    @staticmethod
    def resize_image(image, max_width, max_height):
        """
        Resize an image to fit inside a maximum width and height
        :param image:
        :param max_width:
        :param max_height:
        :return:
        """
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        return image.resize(new_size)


if __name__ == '__main__':
    """
    Run the QRCodeGeneratorGUI class
    """
    qr_code_generator_gui = QRCodeGeneratorGUI()
    qr_code_generator_gui.run_app()

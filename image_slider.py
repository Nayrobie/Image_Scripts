import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

class ImageSliderApp:
    def __init__(self, image_pair):
        self.root = tk.Tk()
        self.root.title("Image Comparison")
        self.image_pair = image_pair
        self.slider_value = 50

        self.load_images()
        self.create_widgets()
        self.update_image()

    def load_images(self):
        self.image1 = self.download_image(self.image_pair[0])
        self.image2 = self.download_image(self.image_pair[1])

        # Resize the second image to match the size of the first image
        if self.image1.size != self.image2.size:
            self.image2 = self.image2.resize(self.image1.size)
    def download_image(self, url):
        response = requests.get(url)
        image_data = BytesIO(response.content)
        return Image.open(image_data)

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=max(self.image1.width, self.image2.width),
                                height=self.image1.height, highlightthickness=0)
        self.canvas.pack()

        self.slider = tk.Scale(self.root, from_=0, to=100, orient=tk.VERTICAL, command=self.on_slider_move)
        self.slider.set(self.slider_value)
        self.slider.pack(side=tk.RIGHT, fill=tk.Y)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(side=tk.BOTTOM)

    def on_slider_move(self, value):
        try:
            self.slider_value = int(value)
            self.update_image()
        except ValueError:
            pass
    def update_image(self):
        blended_image = Image.blend(self.image1, self.image2, self.slider_value / 100)
        self.tk_image = ImageTk.PhotoImage(blended_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    # Pre-made image duos for comparison (use: https://www.aconvert.com/fr/image/ and don't resize images)
    image_pairs = [
        # peach & blue humanoid
        ("https://s4.aconvert.com/convert/p3r68-cdx67/avorh-swumf.jpg",
         "https://s4.aconvert.com/convert/p3r68-cdx67/ap9jc-qe653.jpg"),
        # it does one after the other
        ("https://s4.aconvert.com/convert/p3r68-cdx67/avorh-swumf.jpg",
         "https://s4.aconvert.com/convert/p3r68-cdx67/ap9jc-qe653.jpg")
    ]

    for pair in image_pairs:
        app = ImageSliderApp(pair)
        app.run()
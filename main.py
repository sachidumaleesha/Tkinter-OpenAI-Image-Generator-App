import os
import openai
import tkinter
import requests, io
import customtkinter as ctk
from PIL import Image, ImageTk

def generate():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # print(openai.api_key)

    user_prompt = prompt_entry.get()
    user_prompt += "in style of " + style_dropdown.get()

    response = openai.images.generate(
    model="dall-e-2",
    prompt=user_prompt,
    size="512x512",
    quality="standard",
    n=int(number_slider.get()),
    )

    image_urls = []
    for i in range(len(response.data)):
        image_urls.append(response.data[i].url)

    images = []
    for url in image_urls:
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
        photo_image = ImageTk.PhotoImage(image)
        images.append(photo_image)

    def update_image(index=0):
        canvas.image = images[index]
        canvas.create_image(0, 0, image=images[index], anchor="nw")
        index = (index + 1) % len(images)
        canvas.after(1000, update_image, index)
    
    update_image()

root = ctk.CTk()
root.title("AI Image Generator")

ctk.set_appearance_mode("System")

input_frame = ctk.CTkFrame(root)
input_frame.pack(side="left", expand=True, padx=20, pady=20)

# Row 1
prompt_label = ctk.CTkLabel(input_frame, text="Prompt:")
prompt_label.grid(row=0, column=0, padx=10, pady=10)

prompt_entry = ctk.CTkEntry(input_frame, height=15)
prompt_entry.grid(row=0, column=1, padx=10, pady=10)

# Row 2
style_label = ctk.CTkLabel(input_frame, text="Style:")
style_label.grid(row=1, column=0, padx=10, pady=10)

style_dropdown = ctk.CTkComboBox(input_frame, values=["Realistic", "Cartoonish", "Abstract", "3D Illustration"])
style_dropdown.grid(row=1, column=1, padx=10, pady=10)

# Row 3
number_label = ctk.CTkLabel(input_frame, text="Number of Images:")
number_label.grid(row=2, column=0, padx=10, pady=10)

number_slider = ctk.CTkSlider(input_frame, from_=1, to=5, number_of_steps=4)
number_slider.grid(row=2, column=1, padx=10, pady=10)

# Row 4
generate_button = ctk.CTkButton(input_frame, text="Generate", command=generate)
generate_button.grid(row=3, column=0, columnspan=2, sticky= "news", padx=10, pady=10)

canvas = tkinter.Canvas(root, width=512, height=512)
canvas.pack(side="left")

root.mainloop()
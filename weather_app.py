import tkinter as tk
from PIL import Image, ImageTk
import requests
import os

API_KEY = "67fffaca3eb2909f473ad68ca96ca8fd"

root = tk.Tk()
root.title("Weather App")
root.geometry("600x500")

def format_response(weather):
    try:
        city = weather["name"]
        condition = weather["weather"][0]["description"]
        temp = weather["main"]["temp"]
        final_str = f"City: {city}\nCondition: {condition}\nTemperature: {temp}°F"
    except Exception as e:
        final_str = "There was a problem retrieving that information"
    return final_str

def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"APPID": API_KEY, "q": city, "units": "imperial"}

    response = requests.get(url, params=params)
    weather = response.json()

    
    if weather.get("cod") != 200:
        result["text"] = "City not found or invalid response"
        return

    icon_name = weather["weather"][0]["icon"]
    result["text"] = format_response(weather)
    open_image(icon_name)


def open_image(icon):
    try:
        size = int(frame_two.winfo_height() * 0.25)
        img_path = f"./img/{icon}.png"

        if not os.path.exists(img_path):
            icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"
            img_data = requests.get(icon_url).content
            with open(img_path, 'wb') as handler:
                handler.write(img_data)

        img = Image.open(img_path).resize((size, size), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        weather_icon.delete("all")
        weather_icon.create_image(0, 0, anchor="nw", image=photo)
        weather_icon.image = photo
    except Exception as e:
        print("Error loading image:", e)

bg_img = Image.open('./bg.png').resize((600, 500), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_img)
bg_lbl = tk.Label(root, image=bg_photo)
bg_lbl.place(x=0, y=0, width=600, height=500)


heading_title = tk.Label(bg_lbl, text="Check Weather", font=("arial", 15, "bold"), bg="skyblue", fg="red")
heading_title.place(x=80, y=5)

frame_one = tk.Frame(bg_lbl, bg="cyan", bd=5)
frame_one.place(x=80, y=40, width=450, height=50)

txt_box = tk.Entry(frame_one, font=("times new roman", 25), width=17)
txt_box.grid(row=0, column=0, sticky="W")

btn = tk.Button(frame_one, text="Get Weather", fg="green", font=("times new roman", 16, "bold"),
                command=lambda: get_weather(txt_box.get()))
btn.grid(row=0, column=1, padx=10)

frame_two = tk.Frame(bg_lbl, bg="skyblue", bd=5)
frame_two.place(x=80, y=100, width=450, height=300)

result = tk.Label(frame_two, text="", font=("arial", 15, "italic"), bg="white", justify="left", anchor="nw")
result.place(x=0, y=0, relwidth=1, relheight=1)

weather_icon = tk.Canvas(result, bg="white", bd=0, highlightthickness=0)
weather_icon.place(relx=0.75, rely=0, relwidth=1, relheight=0.5)

root.mainloop()

from tkinter import *
import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk
from datetime import *
import requests
from PIL import Image, ImageTk
from button import RoundedButton
import io

root = Tk()
root.title("Weather App")
root.geometry("830x615+360+120") #830x615+360+120, 1920x1080
root.configure(bg="#D8D6D6", border=1)
root.resizable(True, True)

# Tạo đối tượng Notebook để chứa các tab
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)


# Tạo tab 1
tab1 = ttk.Frame(notebook)
notebook.add(tab1)

# Tạo tab 2
tab2 = ttk.Frame(notebook)
notebook.add(tab2)
style = ttk.Style()
style.configure("TFrame", background="#D8D6D6")

def onEnter():
    update_weather_data(getCity())

def onEsc():
    root.destroy()
city = 0
textField = 0

def getCity():
    city = textField.get().lower().title() ## ha noi -> Ha Noi 
    return city

def get_icon_image(icon_code, w, h):
    url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    response = requests.get(url)
    img = Image.open(io.BytesIO(response.content))
    # img = Image.open(image_path)
    img = img.resize((w, h), Image.LANCZOS) 
    return ImageTk.PhotoImage(img)

# Đổi thứ sang tiếng Việt
weekday_in_vietnamese = {
            'Monday': 'Th 2',
            'Tuesday': 'Th 3',
            'Wednesday': 'Th 4',
            'Thursday': 'Th 5',
            'Friday': 'Th 6',
            'Saturday': 'Th 7',
            'Sunday': 'CN '
        }

def get_weather_time(data):
    
    if (1):
        dt = data['dt']  # Thời gian UNIX
        timezone_offset = data['timezone']  # Độ lệch múi giờ tính bằng giây
        local_time = datetime.fromtimestamp(dt, timezone.utc) + timedelta(seconds=timezone_offset)       
        # Định dạng giờ
        formatted_hours = f"{local_time.hour}h"      
        # Định dạng ngày tháng
        formatted_date = local_time.strftime("%A, %d/%m/%Y")      
        # Thay thế thứ bằng tiếng Việt
        for english, vietnamese in weekday_in_vietnamese.items():
            formatted_date = formatted_date.replace(english, vietnamese)
        return f"{formatted_hours} {formatted_date}"

def getTempMax(data, dataCurent):
    current_date = data['list'][0]['dt_txt'][0:10]
    timezone = int(data['city']['timezone'])/3600
    max_temp = dataCurent['main']['temp']
            # Iterate through the forecast data
    for item in data['list']:
        forecast_datetime = item['dt_txt'][0:10]
        h =  int(item['dt_txt'][11:13]) 
          # Check if we're still on the same day
        if forecast_datetime == current_date and (h + timezone < 25):
                    temp = item['main']['temp']
                    if temp > max_temp:
                        max_temp = temp
        else: return max_temp

def getTempMin(data, dataCurent):
    current_date = data['list'][0]['dt_txt'][0:10]
    max_temp = dataCurent['main']['temp']
    timezone = int(data['city']['timezone'])/3600
            # Iterate through the forecast data
    for item in data['list']:
        h =  int(item['dt_txt'][11:13])
        forecast_datetime = item['dt_txt'][0:10]   
          # Check if we're still on the same day
        if forecast_datetime == current_date and (h + timezone < 25):
                    temp = item['main']['temp']
                    if temp < max_temp:
                        max_temp = temp
        else: return max_temp


def update_weather_data(city):
    API_KEY = "3aa069c12609852ef55a78bd94930820"
    current_weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&lang=vi&appid={API_KEY}&units=metric"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&lang=vi&appid={API_KEY}&units=metric"

    current_response = requests.get(current_weather_url)
    forecast_response = requests.get(forecast_url)

    if current_response.status_code == 200 and forecast_response.status_code == 200:
        longLat.config(text="")
        current_data = current_response.json()
        forecast_data = forecast_response.json()
        # topbox
        fourthIntro.config(text=f"Thời tiết {current_data['name']} ")
        fourthIntro2.config(text=f"{get_weather_time(current_data)}")
        # First box
        firstDayImage = current_data['weather'][0]['icon']
        photo1 = get_icon_image(firstDayImage, 150, 150)
        firstImage.config(image=photo1)
        firstImage.image = photo1

        day1TempAve.config(text=f"{round(current_data['main']['temp'])}°")
        firstLine_temp.config(text=f"{round(current_data['main']['feels_like'])}°")
        # day1Temp.config(text=f"Ngày {round(tempDay)}° / Đêm {round(tempNight)}°")

        # Second box
        # The 'summary' field is not available in the new API, so we'll use the description
        secondSummary.config(text=current_data['weather'][0]['description'])
        noti_Icon.place(x= 10, y=1)

        # Third box
        # We'll use the forecast data to get temperatures for different times of the day
        temperature_list = []
        for forecast in forecast_data['list'][:4]:  # First 4 entries for the next 12 hours
            temp = round(forecast['main']['temp'])
            # time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
            time = datetime.fromtimestamp(forecast['dt'], timezone.utc) + timedelta(seconds=current_data['timezone'])
            time = f"{time.hour}h00"
            icon = forecast['weather'][0]['icon']
            temperature_list.append((time, temp, icon))

        thirdFrame1_time.config(text=temperature_list[0][0])
        thirdFrame1_temp.config(text=f"{temperature_list[0][1]}°")

        thirdFrame2_time.config(text=temperature_list[1][0])
        thirdFrame2_temp.config(text=f"{temperature_list[1][1]}°")

        thirdFrame3_time.config(text=temperature_list[2][0])
        thirdFrame3_temp.config(text=f"{temperature_list[2][1]}°")

        thirdFrame4_time.config(text=temperature_list[3][0])
        thirdFrame4_temp.config(text=f"{temperature_list[3][1]}°")

        # Update icons based on temperature
        for i, (time, temp, icon) in enumerate(temperature_list):           
            photo = get_icon_image(icon, 100, 100)
            globals()[f"thirdFrame{i+1}_icon"].config(image=photo)
            globals()[f"thirdFrame{i+1}_icon"].image = photo

        # Fourth box
        # firstLine.config(text="  Cảm nhận")

        fourthphoto_1 = PhotoImage(file = f"assets/main/icon/iconFeelLike/iconTemperatureHigh.png")
        fourthphoto_1 = fourthphoto_1.subsample(20, 20)
        secondLine_icon.config(image=fourthphoto_1)
        secondLine_icon.image = fourthphoto_1

        fourthphoto_2 = PhotoImage(file = f"assets/main/icon/iconFeelLike/iconTemperatureLow.png")
        fourthphoto_2 = fourthphoto_2.subsample(20, 20)
        thirdLine_icon.config(image=fourthphoto_2)
        thirdLine_icon.image = fourthphoto_2

        fourthphoto_3 = PhotoImage(file = f"assets/main/icon/iconFeelLike/iconhumidity.png")
        fourthphoto_3 = fourthphoto_3.subsample(20, 20)
        fourthLine_icon.config(image=fourthphoto_3)
        fourthLine_icon.image = fourthphoto_3

        fourthphoto_4 = PhotoImage(file = f"assets/main/icon/iconFeelLike/iconpressure.png")
        fourthphoto_4 = fourthphoto_4.subsample(90, 90)
        fifthLine_icon.config(image=fourthphoto_4)
        fifthLine_icon.image = fourthphoto_4

        fourthphoto_5 = PhotoImage(file = f"assets/main/icon/iconFeelLike/iconWind.png")
        fourthphoto_5 = fourthphoto_5.subsample(30, 30)
        sixthLine_icon.config(image=fourthphoto_5)
        sixthLine_icon.image = fourthphoto_5
        secondLine.config(text="Cao nhất")
        secondLine_temp.config(text=f"{round(getTempMax(forecast_data, current_data))}°")

        thirdLine.config(text="Thấp nhất")
        thirdLine_temp.config(text=f"{round(getTempMin(forecast_data, current_data))}°")

        fourthLine.config(text="Độ ẩm")
        fourthLine_temp.config(text=f"{round(current_data['main']['humidity'])}%")

        fifthLine.config(text="Áp suất")
        fifthLine_temp.config(text=f"{round(current_data['main']['pressure'])} hPa")
        
        sixthLine.config(text="Tốc độ gió")
        sixthLine_temp.config(text=f"{round(current_data['wind']['speed'])} m/s")

        fourthphoto_7 = PhotoImage(file = f"assets/main/icon/iconFeelLike/iconCloud.png")
        fourthphoto_7 = fourthphoto_7.subsample(30, 30)
        seventhLine_icon.config(image=fourthphoto_7)
        seventhLine_icon.image = fourthphoto_7
        seventhLine.config(text="Mây che")
        seventhLine_temp.config(text=f"{round(current_data['clouds']['all'])}%")

        # Tab 2
        # First box
        firstline_box1.config(text=f"Thời tiết 4 ngày tiếp theo - {current_data['name']}, {current_data['sys']['country']}")
        # firstline_box2.config(text=f"")
        # For the 5-day forecast, we'll use the forecast data
        i = 0
        j = 0
        while (True):
            if(j > 39) or i > 3:
                break
            item = forecast_data['list'][j]
            j+=1
            h =  int(item['dt_txt'][11:13])
            timeZone = int(current_data['timezone'])/3600

            if(21 < timeZone+h  and  timeZone+h < 25 ):
                #set temp max min
                list = forecast_data['list'][i*8:i*8+8]
                max = -100
                min = 100
                for day in list:
                    if(day['main']['temp'] > max):
                        max =  day['main']['temp']
                    if(day['main']['temp'] < min):
                        min =  day['main']['temp']
                    h =  int(day['dt_txt'][11:13]) 
                    if(9 < h+timeZone and h+timeZone < 13):
                        icon = get_icon_image(day['weather'][0]['icon'], 100, 100)
                        globals()[f"{[ 'third', 'fourth', 'fifth', 'sixth'][i]}Image_icon"].config(image=icon)
                        globals()[f"{['third', 'fourth', 'fifth', 'sixth'][i]}Image_icon"].image = icon
                        globals()[f"{[ 'third', 'fourth', 'fifth', 'sixth'][i]}line_box1"].config(text=weekday_in_vietnamese[datetime.fromtimestamp(day['dt']).strftime("%A")])
                        globals()[f"{['third', 'fourth', 'fifth', 'sixth'][i]}Image_des"].config(text=day['weather'][0]['description'].title())
                        globals()[f"{['third', 'fourth', 'fifth', 'sixth'][i]}Image_hmdNum"].config(text=f"{round(day['main']['humidity'])}%")
                globals()[f"{[ 'third', 'fourth', 'fifth', 'sixth'][i]}line_box2"].config(text=f"{round(max)}° / {round(min)}°")
                i = i+1
    else:
        longLat.config(text="Không tìm thấy địa điểm")
        print("Error fetching weather data")

def switch_tab(tab_index):
    notebook.select(tab_index)

top_box = Frame(tab1, width=830, height=140, bg="#77baf3")
# top_box.pack(side=TOP)
top_box.place(x = 0, y = 0)


# Search box
# def setSearchBox():
Search_image = PhotoImage(file="assets/images/Rounded Rectangle 3.png")
myImage = Label(tab1, image=Search_image, bg="#77baf3")
myImage.place(x = 320, y = 25)

weat_image = PhotoImage(file="assets/main/icon/iconWeather/iconPartlySunny.png")
weat_image = weat_image.subsample(10, 10)
weatherImage = Label(tab1, image=weat_image, background="#203243")
weatherImage.place(x = 350, y = 27)

textField  = tk.Entry(tab1, justify='center',width=15, font=('poppins',25,'bold'),bg="#203243",border=0, fg="white")
textField.place(x = 400, y = 35)
textField.focus()

Search_icon = PhotoImage(file="assets/main/back/Layer 6.png")
# update_weather_data(city)
myImage_icon = Button(tab1, image=Search_icon, borderwidth=0, cursor="hand2", bg="#203243", command= lambda: update_weather_data(getCity()), activebackground="#203243")
myImage_icon.place(x = 690, y = 30)


## Time zone
timeZone = Label(tab1, font=("Arial", 20, 'bold'), fg="black", bg="#77baf3")
timeZone.place(x = 30, y = 20)

longLat = Label(tab1, font=("Arial", 30), fg="black", bg="#77baf3")
longLat.place(x = 330, y = 90)


## Today Weather

box_1 = RoundedButton(tab1, 450, 130, 20, 2, 'white', '#D8D6D6')
box_1.place(x = 50, y = 155)

box_2 = RoundedButton(tab1, 450, 60, 20, 2, 'white', '#D8D6D6')
box_2.place(x = 50, y = 297)

box_3 = RoundedButton(tab1, 450, 180, 20, 2, 'white', '#D8D6D6')
box_3.place(x = 50, y = 370)

box_4 = RoundedButton(tab1, 240, 300, 20, 2, 'white', '#D8D6D6')
box_4.place(x = 540, y = 155)



box5_image = PhotoImage(file="assets/images/test2.png")
box5_image = box5_image.subsample(10, 10)
box_5 = Button(tab1, image=box5_image, borderwidth=0, cursor="hand2", bg="#D8D6D6", command=lambda: switch_tab(1), activebackground="#D8D6D6")
box_5.place(x = 700, y = 470)


## First box

firstFrame = Frame(tab1, width=400, height=120, bg="white")
firstFrame.place(x = 75, y = 160)

firstImage = Label(firstFrame, bg="white")
firstImage.place(x = 1, y = -10)

firstDes = Label(firstFrame, bg="white", fg="black", font="arial 15 bold")
firstDes.place(x = 5, y = 80)

day1TempAve = Label(firstFrame, bg="white", fg="black", font="arial 50 bold")
day1TempAve.place(x = 250, y = 1)

day1Temp = Label(firstFrame, bg="white", fg="black", font="arial 20 bold")
day1Temp.place(x = 140, y = 80)
firstLine_temp = Label(firstFrame, bg="white", fg="black", font="arial 13 bold")
firstLine_temp.place(x = 280, y = 80)


## Second box

secondFrame = Frame(tab1, width=400, height=50, bg = 'white')
secondFrame.place(x = 75, y = 302)

notiImage = PhotoImage(file="assets/main/icon/otherIcons/notification.png")
notiImage = notiImage.subsample(15, 15)
noti_Icon = Label(secondFrame, image=notiImage, bg="white")

secondSummary = Label(secondFrame, bg="white", fg="black", font="arial 12 bold")
secondSummary.place(x = 60, y = 10)


## Third box

thirdFrame_1 = Frame(tab1, width=80, height=160, bg="white")
thirdFrame_1.place(x = 60, y = 380)

thirdFrame1_icon = Label(thirdFrame_1, bg="white")
thirdFrame1_icon.place(x = -10, y = 70)

thirdFrame1_time = Label(thirdFrame_1, bg="white",  fg="black", font="arial 13 bold")
thirdFrame1_time.place(x = 15, y = 10)

thirdFrame1_temp = Label(thirdFrame_1, bg="white", fg="black", font="arial 30 bold")
thirdFrame1_temp.place(x = 10, y = 45)

canvas_1 = Canvas(tab1, width=20, height=150, bg="white")
canvas_1.config(highlightbackground="white")
canvas_1.place(x = 145, y = 380)


thirdFrame_2 = Frame(tab1, width=90, height=160, bg="white")
thirdFrame_2.place(x = 175, y = 380)

thirdFrame2_icon = Label(thirdFrame_2, bg="white")
thirdFrame2_icon.place(x = -10, y = 70)

thirdFrame2_time = Label(thirdFrame_2, bg="white",  fg="black", font="arial 13 bold")
thirdFrame2_time.place(x = 15, y = 10)

canvas_2 = Canvas(tab1, width=20, height=150, bg="white")
canvas_2.config(highlightbackground="white")
canvas_2.place(x = 263, y = 380)

thirdFrame2_temp = Label(thirdFrame_2, bg="white", fg="black", font="arial 30 bold")
thirdFrame2_temp.place(x = 20, y = 45)


thirdFrame_3 = Frame(tab1, width=80, height=160, bg="white")
thirdFrame_3.place(x = 293, y = 380)

thirdFrame3_time = Label(thirdFrame_3, bg="white",  fg="black", font="arial 13 bold")
thirdFrame3_time.place(x = 15, y = 10)
thirdFrame3_icon = Label(thirdFrame_3, bg="white")
thirdFrame3_icon.place(x = -10, y = 70)
thirdFrame3_temp = Label(thirdFrame_3, bg="white", fg="black", font="arial 30 bold")
thirdFrame3_temp.place(x = 15, y = 45)

canvas_3 = Canvas(tab1, width=20, height=150, bg="white")
canvas_3.config(highlightbackground="white")
canvas_3.place(x = 380, y = 380)

thirdFrame_4 = Frame(tab1, width=80, height=160, bg="white")
thirdFrame_4.place(x = 400, y = 380)
thirdFrame4_icon = Label(thirdFrame_4, bg="white")
thirdFrame4_icon.place(x = -10, y = 70)
thirdFrame4_time = Label(thirdFrame_4, bg="white",  fg="black", font="arial 13 bold")
thirdFrame4_time.place(x = 15, y = 10)

thirdFrame4_temp = Label(thirdFrame_4, bg="white", fg="black", font="arial 30 bold")
thirdFrame4_temp.place(x = 15, y = 45)

canvas_1.create_line(10, 10, 10, 150, width=2, fill="#D8D6D6")
canvas_2.create_line(10, 10, 10, 150, width=2, fill="#D8D6D6")
canvas_3.create_line(10, 10, 10, 150, width=2, fill="#D8D6D6")

# top
fourthIntro = Label(tab1, bg="#77BAF3", fg="black", font="arial 15 bold")
fourthIntro.place(x = 10, y = 15)
fourthIntro2 = Label(tab1, bg="#77BAF3", fg="black", font="arial 15 bold")
fourthIntro2.place(x = 10, y = 50)
## Fourth Box

canvas2_1 = Canvas(tab1, width=220, height=20, bg="white")
canvas2_1.config(highlightbackground="white")
canvas2_1.place(x = 550, y = 210)
canvas2_1.create_line(10, 10, 220, 10, width=2, fill="#D8D6D6")

fourthFrame_2 = Frame(tab1, width=220, height=40, bg="white")
fourthFrame_2.place(x = 550, y = 225)

secondLine_icon = Label(fourthFrame_2, bg="white")
secondLine_icon.place(x = 5, y = 1)

secondLine = Label(fourthFrame_2, bg="white", fg="black", font="arial 13 bold")
secondLine.place(x = 35, y = 2)

secondLine_temp = Label(fourthFrame_2, bg="white", fg="black", font="arial 13 bold")
secondLine_temp.place(x = 170, y = 5)

canvas2_2 = Canvas(tab1, width=220, height=20, bg="white")
canvas2_2.config(highlightbackground="white")
canvas2_2.place(x = 550, y = 250)

canvas2_2.create_line(10, 10, 220, 10, width=2, fill="#D8D6D6")

fourthFrame_3 = Frame(tab1, width=220, height=40, bg="white")
fourthFrame_3.place(x = 550, y = 265)

thirdLine_icon = Label(fourthFrame_3, bg="white")
thirdLine_icon.place(x = 5, y = 1)

thirdLine = Label(fourthFrame_3, bg="white", fg="black", font="arial 13 bold")
thirdLine.place(x = 35, y = 2)

thirdLine_temp = Label(fourthFrame_3, bg="white", fg="black", font="arial 13 bold")
thirdLine_temp.place(x = 170, y = 5)

canvas2_3 = Canvas(tab1, width=220, height=20, bg="white")
canvas2_3.config(highlightbackground="white")
canvas2_3.place(x = 550, y = 290)

canvas2_3.create_line(10, 10, 220, 10, width=2, fill="#D8D6D6")

fourthFrame_4 = Frame(tab1, width=220, height=40, bg="white")
fourthFrame_4.place(x = 550, y = 305)

fourthLine_icon = Label(fourthFrame_4, bg="white")
fourthLine_icon.place(x = 5, y = 1)

fourthLine = Label(fourthFrame_4, bg="white", fg="black", font="arial 13 bold")
fourthLine.place(x = 35, y = 2)

fourthLine_temp = Label(fourthFrame_4, bg="white", fg="black", font="arial 13 bold")
fourthLine_temp.place(x = 170, y = 5)

canvas2_4 = Canvas(tab1, width=220, height=20, bg="white")
canvas2_4.config(highlightbackground="white")
canvas2_4.place(x = 550, y = 330)

canvas2_4.create_line(10, 10, 220, 10, width=2, fill="#D8D6D6")

fourthFrame_5 = Frame(tab1, width=220, height=40, bg="white")
fourthFrame_5.place(x = 550, y = 345)

fifthLine_icon = Label(fourthFrame_5, bg="white")
fifthLine_icon.place(x = 5, y = 1)

fifthLine = Label(fourthFrame_5, bg="white", fg="black", font="arial 13 bold")
fifthLine.place(x = 35, y = 2)

fifthLine_temp = Label(fourthFrame_5, bg="white", fg="black", font="arial 13 bold")
fifthLine_temp.place(x = 145, y = 5)

canvas2_5 = Canvas(tab1, width=220, height=20, bg="white")
canvas2_5.config(highlightbackground="white")
canvas2_5.place(x = 550, y = 370)

canvas2_5.create_line(10, 10, 220, 10, width=2, fill="#D8D6D6")

fourthFrame_6 = Frame(tab1, width=220, height=40, bg="white")
fourthFrame_6.place(x = 550, y = 385)

sixthLine_icon = Label(fourthFrame_6, bg="white")
sixthLine_icon.place(x = 5, y = 1)

sixthLine = Label(fourthFrame_6, bg="white", fg="black", font="arial 13 bold")
sixthLine.place(x = 35, y = 2)

sixthLine_temp = Label(fourthFrame_6, bg="white", fg="black", font="arial 13 bold")
sixthLine_temp.place(x = 160, y = 5)

canvas2_6 = Canvas(tab1, width=220, height=20, bg="white")
canvas2_6.config(highlightbackground="white")
canvas2_6.place(x = 550, y = 410)

canvas2_6.create_line(10, 10, 220, 10, width=2, fill="#D8D6D6")

fourthFrame_7 = Frame(tab1, width=220, height=40, bg="white")
fourthFrame_7.place(x = 550, y = 175)

seventhLine_icon = Label(fourthFrame_7, bg="white")
seventhLine_icon.place(x = -2, y = 1)

seventhLine = Label(fourthFrame_7, bg="white", fg="black", font="arial 13 bold")
seventhLine.place(x = 35, y = 10)

seventhLine_temp = Label(fourthFrame_7, bg="white", fg="black", font="arial 13 bold")
seventhLine_temp.place(x = 160, y = 10)


## Tab 2

# First line
firstFrame_tab2 = Frame(tab2, width=830, height=60, bg="#D8D6D6")
firstFrame_tab2.place(x = 1, y = 1)
firstline_arrow = PhotoImage(file="assets/main/icon/otherIcons/back_arrow.png")
firstline_arrow = firstline_arrow.subsample(2, 2)
firstline_icon = Button(tab2, image=firstline_arrow,borderwidth=0, cursor="hand2", bg="#D8D6D6", command=lambda: switch_tab(0), activebackground="#D8D6D6")
firstline_icon.place(x = 1, y = 1)

firstline_box1 = Label(firstFrame_tab2, bg="#D8D6D6", fg="black", font="arial 25 bold")
firstline_box1.place(x = 55, y = 10)

firstline_box2 = Label(firstFrame_tab2, bg="#D8D6D6", fg="black", font="arial 25 bold")
firstline_box2.place(x = 320, y = 10)
# Second line
humidityIcon = PhotoImage(file = f"assets/main/icon/iconFeelLike/iconhumidity.png")
humidityIcon = humidityIcon.subsample(20, 20)

secondFrame_tab2 = Frame(tab2, width=830, height=60, bg="#D8D6D6")
secondFrame_tab2.place(x = 10, y = 65)

secondline_box1 = Label(secondFrame_tab2, bg="#D8D6D6", fg="black", font="arial 20 bold")
secondline_box1.place(x = 45, y = 15)

secondline_box2 = Label(secondFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
secondline_box2.place(x = 150, y = 18)

secondImage_icon = Label(secondFrame_tab2, bg="#D8D6D6")
secondImage_icon.place(x = 250, y = -20)

secondImage_des = Label(secondFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
secondImage_des.place(x = 350, y = 15)

secondImage_hmdIcon = Label(secondFrame_tab2, bg="#D8D6D6")
secondImage_hmdIcon.place(x = 650, y = 15)

secondImage_hmdNum = Label(secondFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
secondImage_hmdNum.place(x = 680, y = 15)

canvasTab2_2 = Canvas(tab2, width=800, height=20, bg="#D8D6D6")
canvasTab2_2.config(highlightbackground="#D8D6D6")
canvasTab2_2.place(x = 10, y = 125)

canvasTab2_2.create_line(50, 10, 750, 10, width=2, fill="black")


# Third line

thirdFrame_tab2 = Frame(tab2, width=830, height=60, bg="#D8D6D6")
thirdFrame_tab2.place(x = 10, y = 140)

thirdline_box1 = Label(thirdFrame_tab2, bg="#D8D6D6", fg="black", font="arial 20 bold")
thirdline_box1.place(x = 45, y = 15)

thirdline_box2 = Label(thirdFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
thirdline_box2.place(x = 150, y = 18)

thirdImage_icon = Label(thirdFrame_tab2, bg="#D8D6D6")
thirdImage_icon.place(x = 250, y = -20)

thirdImage_des = Label(thirdFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
thirdImage_des.place(x = 350, y = 15)

thirdImage_hmdIcon = Label(thirdFrame_tab2, bg="#D8D6D6")
thirdImage_hmdIcon.place(x = 650, y = 15)
thirdImage_hmdIcon.config(image=humidityIcon)
thirdImage_hmdIcon.image = humidityIcon

thirdImage_hmdNum = Label(thirdFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
thirdImage_hmdNum.place(x = 680, y = 15)

canvasTab2_3 = Canvas(tab2, width=800, height=20, bg="#D8D6D6")
canvasTab2_3.config(highlightbackground="#D8D6D6")
canvasTab2_3.place(x = 10, y = 200)

canvasTab2_3.create_line(50, 10, 750, 10, width=2, fill="black")

# Fourth line
fourthFrame_tab2 = Frame(tab2, width=830, height=60, bg="#D8D6D6")
fourthFrame_tab2.place(x = 10, y = 215)

fourthline_box1 = Label(fourthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 20 bold")
fourthline_box1.place(x = 45, y = 15)

fourthline_box2 = Label(fourthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
fourthline_box2.place(x = 150, y = 18)

fourthImage_icon = Label(fourthFrame_tab2, bg="#D8D6D6")
fourthImage_icon.place(x = 250, y = -20)

fourthImage_des = Label(fourthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
fourthImage_des.place(x = 350, y = 15)

fourthImage_hmdIcon = Label(fourthFrame_tab2, bg="#D8D6D6")
fourthImage_hmdIcon.place(x = 650, y = 15)
fourthImage_hmdIcon.config(image=humidityIcon)
fourthImage_hmdIcon.image = humidityIcon

fourthImage_hmdNum = Label(fourthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
fourthImage_hmdNum.place(x = 680, y = 15)

canvasTab2_4 = Canvas(tab2, width=800, height=20, bg="#D8D6D6")
canvasTab2_4.config(highlightbackground="#D8D6D6")
canvasTab2_4.place(x = 10, y = 275)

canvasTab2_4.create_line(50, 10, 750, 10, width=2, fill="black")

# Fifth line
fifthFrame_tab2 = Frame(tab2, width=830, height=60, bg="#D8D6D6")
fifthFrame_tab2.place(x = 10, y = 290)

fifthline_box1 = Label(fifthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 20 bold")
fifthline_box1.place(x = 45, y = 15)

fifthline_box2 = Label(fifthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
fifthline_box2.place(x = 150, y = 18)

fifthImage_icon = Label(fifthFrame_tab2, bg="#D8D6D6")
fifthImage_icon.place(x = 250, y = -20)

fifthImage_des = Label(fifthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
fifthImage_des.place(x = 350, y = 15)

fifthImage_hmdIcon = Label(fifthFrame_tab2, bg="#D8D6D6")
fifthImage_hmdIcon.place(x = 650, y = 15)
fifthImage_hmdIcon.config(image=humidityIcon)
fifthImage_hmdIcon.image = humidityIcon

fifthImage_hmdNum = Label(fifthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
fifthImage_hmdNum.place(x = 680, y = 15)

canvasTab2_5 = Canvas(tab2, width=800, height=20, bg="#D8D6D6")
canvasTab2_5.config(highlightbackground="#D8D6D6")
canvasTab2_5.place(x = 10, y = 350)

canvasTab2_5.create_line(50, 10, 750, 10, width=2, fill="black")
# Sixth line
sixthFrame_tab2 = Frame(tab2, width=830, height=60, bg="#D8D6D6")
sixthFrame_tab2.place(x = 10, y = 365)

sixthline_box1 = Label(sixthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 20 bold")
sixthline_box1.place(x = 45, y = 15)

sixthline_box2 = Label(sixthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
sixthline_box2.place(x = 150, y = 18)

sixthImage_icon = Label(sixthFrame_tab2, bg="#D8D6D6")
sixthImage_icon.place(x = 250, y = -20)

sixthImage_des = Label(sixthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
sixthImage_des.place(x = 350, y = 15)

sixthImage_hmdIcon = Label(sixthFrame_tab2, bg="#D8D6D6")
sixthImage_hmdIcon.place(x = 650, y = 15)
sixthImage_hmdIcon.config(image=humidityIcon)
sixthImage_hmdIcon.image = humidityIcon

sixthImage_hmdNum = Label(sixthFrame_tab2, bg="#D8D6D6", fg="black", font="arial 17 bold")
sixthImage_hmdNum.place(x = 680, y = 15)

canvasTab2_6 = Canvas(tab2, width=800, height=20, bg="#D8D6D6")
canvasTab2_6.config(highlightbackground="#D8D6D6")
canvasTab2_6.place(x = 10, y = 425)

canvasTab2_6.create_line(50, 10, 750, 10, width=2, fill="black")

update_weather_data("hà đông")
root.bind("<Escape>", lambda event=None: onEsc())
root.bind("<Return>", lambda event=None: onEnter())
root.mainloop()

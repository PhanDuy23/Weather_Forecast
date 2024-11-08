# DỰ ÁN PYTHON
## 1. Thông Tin Nhóm

**Tên Dự Án:** [WEATHER-FORECAST]

<!-- **Link Dự Án:** [[GitHub Link](https://github.com/Yamaaaaaaaa/Group5_BTCK_PGC-Endless_Way.git)](#) -->

**Thành Viên Nhóm:**
- [Phan Văn Duy]
- [Trần Đức Dũng]

## 2. Giới Thiệu Dự Án

**MÔ TẢ:** **[WEATHER-FORECAST]** là destop app dùng để xem dự báo thời tiết nhiều thành phố, tỉnh thành, quốc gia trên thế giới, dự báo thời tiết trong ngày và trong 4 ngày tới.


## 3. Công nghệ
- **Tkinter**: là thư viện tiêu chuẩn của Python để xây dựng giao diện đồ họa người dùng (GUI).
- **Requests**: là thư viện phổ biến để thực hiện các yêu cầu HTTP, như GET, POST, PUT, DELETE.
- **PIL**: là thư viện mạnh mẽ để xử lý và thao tác với ảnh.
- **IO**: là thư viện tiêu chuẩn trong Python để xử lý các hoạt động I/O (input/output) với các đối tượng tệp.
## 4. Dữ liệu
- **API**
  - [Thời tiết hiện tại](https://api.openweathermap.org/data/2.5/weather?q=Hanoi&lang=vi&appid=3aa069c12609852ef55a78bd94930820&units=metric)
  - [Thời tiết các ngày tới](https://api.openweathermap.org/data/2.5/forecasr?q=Hanoi&lang=vi&appid=3aa069c12609852ef55a78bd94930820&units=metric)
  - [Icon thời tiết](http://openweathermap.org/img/wn/{icon_code}@2x.png)

## 5. Cấu trúc dự án

```
- assets 
  - images
  - main
    - back
    - icon
      - iconFeelLike
      - iconWeather
      - otherIcons
- src
  - button.py
  - weatherForecast.py
```

Diễn giải:
- **assets:** Chứa các tài nguyên như hình ảnh, icon
- **button.py:** file định nghĩa button
- **weatherForecast.py** file chính 
## 6. Ảnh Demo

![page1](demoApp/page1.png)

![page2](demoApp/page2.png)

- Cần cài các thư viện để chạy: 
  - pip install pytz 
  - pip install geopy
  - pip install timezonefinder
  - pip install requests 
  - pip install pillow
  

# ISS Watcher App
This Python application sends you an email if the ISS is nearby your location at night.

## How it works
This project fetches data from two APIs. One of them is the [Sunrise & Sunset API](https://sunrise-sunset.org/api), which tells the user when the sun rises or sets based on their current location. The other API used is the [ISS Location API](http://open-notify.org/Open-Notify-API/ISS-Location-Now/), which provides the latitude and longitude of the ISS. If the ISS is within a 100 km range of the user's location and it is nighttime (between sunset and sunrise), the user receives an email notification.

## How to use this app

### Step 1: Clone this app
Use the terminal:
git clone https://github.com/Akos24/iss-watcher-app.git

### Step 2: Modify the CSV files:
The coords.csv contains data about the user's location and timezone. In the second row you should provide data about the latitude, longitude, and timezone of the location you want to investigate.

Example for correct input:<br/>
Lat,Lng,Timezone<br/>
47.438161,19.098913,Europe/Budapest

The user_data.csv contains data about the email address where you get the notification, and the email address from where you send the notification. You should also provide an app password which python can use to send emails with your email address. You can set up this password in the Google App passwords option.

Example for correct input:<br/>
NameTo,EmailTo,EmailFrom,PasswordFrom<br/>
John Doe,johndoe@gmail.com,adamsmith@gmail.com,abcd efhg ijkl mnop

### Step 3: Change directory to the cloned directory
cd "iss-watcher-app"

### Step 4: Run the app
python3 main.py

You might want to run the app in the background for a while. The app checks the ISS location every minute. This makes the app faster and limits API request rate. If you run this app in the byckground at nighttime you might get a few emails about the ISS location.

## How to contribute
If you spot some bugs in this app, or you want to make some adjustments feel free to make pull requests. Every contribution is welcome :)

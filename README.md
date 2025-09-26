### Weather App

The Weather App is meant to present weather data of wind, pressure and temperature
of a given data set via an URL link in the last 48 hours. The base URL is meant for>
presenting data in the last 48 hours for all Slovenian cities.

### Build

To build the app the user needs to install the reqired packages as so:

pip install -r requirements.txt

Should you need any additional packages it is reccommended to create
your own virtual environment and install them there.

### Run

To run the program simply type in the terminal:

python3 main.py

### Further development

For future development the plan is to fix/add the following things:

- reading values from the Pressure [hPa] column that are presented in mmHg (with a *)
- adjusting reading the active link for the data
- adding test.py
- expanding the data_collection directory by reading from XML,JSON and other files
- expanding the gui directory with other possible GUI libraries (PyQt6, Tkinter, Kivy, etc)



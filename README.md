# Smart Campus network and IoT web applications Project

This is a school group project for the course **EIE2903/IC2141 Internet and Multimedia Product Development** at The Hong Kong Polytechnic University (PolyU), developed by Group 8 in year 1 summer (2025).

The main objective of this project is developing a Smart Campus network and IoT web applications.

## What it does

- Home page with navigation links to admin login, log page, dashboard, Time-Event-Data page, and Data Analysis page
- Top and bottom navigation bars on the site
- Time-Event-Data page lets users choose a venue/location and time range to view events and optional environmental records
- Data analysis page filters abnormal records and shows time since each record was created

## My contribution

- Built the Time-Event-Data and Data Analysis page and its form logic
- Created a dynamic venue selection field from the database
- Implemented the query logic to extract matching event and environmental records
- Used `django.utils.timesince` to show how recent records are
- Worked on the web design and Raspberry Pi / IoT status tag interaction

> Privacy note: student ID and my groupmate's name are redacted in the report for privacy reasons.

## Requirements

- Python 3
- Django

## Run

1. Go to `01-Home/workspace/IC2140/Smart_Campus/mysite`
2. Run:
   ```bash
   python manage.py runserver
   ```
3. Open the app in a browser at `http://127.0.0.1:8000/`

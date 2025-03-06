---
title: "Module 10 Challenge"
---

# Overview

This challenge use SQLAlchemy ORM queries, Pandas, and Matplotlib to complete analysis of climate data in the Honolulu, Hawaii area.

# Repo Contents
1. SurfsUp folder
    a. Resources folder - contains SQLite database, "hawaii.sqlite" comprised of two tables:
        - measurement - id, station, date, prcp, tobs
        - station - id, station, name, latitude, longitude, elevation
    b. climate_starter.ipynb - Jupyter notebook containing the climate analysis described in more detail below
    c. app.py - a Flask API based on the climate analysis
2. README.md

# Part One: Analysis
### Precipitation Analysis

Below is a bar graph showing the last twelve months of precipitation data:
![alt text](Images/image.png)

Below are the summary statistics for the precipitation data during the same time period:
![alt text](Images/image-1.png)

### Station Analysis

Activity across the 9 stations was analyzed, and the following is noted:
- The most-active station was: USC00519281
- The minimum, maximum and average temps were [(54.0, 85.0, 71.66378066378067)]

Below is a histogram of the last 12 months of temperature data for the most-active station:
![alt text](Images/image-2.png)

# Part Two: Climate App

A Flask API based on the above analysis with the following routes:

1. precipitation - provides a dictionary of the precipitation by station and date for the latest 12 months
2. stations - provides a list of stations
3. tobs - provides a dictionary of temperature observations for the most-active station for the latest 12 months
4. start - calculates `TMIN`, `TAVG`, and `TMAX` for all the dates greater than or equal to the start date input by the user
5. start_end - calculates `TMIN`, `TAVG`, and `TMAX` for all the dates greater than or equal to the start date and less than or equal to the end date input by the user

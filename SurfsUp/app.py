# Import the dependencies.
import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta as td

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify, request


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)   



#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<b>Available Routes:</b><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<b>Search using dates between 2016-08-23 and 2017-08-23:</b><br/>"        
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start_end/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of last 12 months of precipitation data"""

    # Calculate the date one year from the last date in data set.
    max_dt = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_dt = max_dt[0]
    d1=dt.strptime(end_dt, "%Y-%m-%d")
    start_dt = d1 - td(days=366)

    # Retrieve the last 12 months of precipitation data by station
    precip_data = session.query(Station.name, Measurement.date, Measurement.prcp).\
    filter(Measurement.station == Station.station).\
    filter(Measurement.date >= start_dt).\
    filter(Measurement.date <= end_dt).\
    order_by(Station.name, Measurement.date).all()

    # Close the session
    session.close()

    # Create a dictionary from the row data and append to a list of all_precip
    all_precip = []
    for name, date, prcp in precip_data:
        measurement_dict = {}
        measurement_dict["name"] = name
        measurement_dict["date"] = date
        measurement_dict["precipitation"] = prcp
        all_precip.append(measurement_dict)

    return jsonify(all_precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station, Station.name).\
        order_by(Station.name).all()

    # Close the session
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all temp observations for the most-active station"""
    # Identify the most-active station
    most_active_station = session.query(Measurement.station, Station.name, func.count(Measurement.date)).\
        filter(Measurement.station == Station.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.date).desc()).first()
    
    # Identify the date range for the most recent 12 months
    max_dt = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    end_dt = max_dt[0]
    d1=dt.strptime(end_dt, "%Y-%m-%d")
    start_dt = d1 - td(days=366)

    # Query the database to obtain the tobs from the last 12 months for the most-active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station[0]).\
        filter(Measurement.date >= start_dt).\
        filter(Measurement.date <= end_dt).all()

    # Close the session
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(f"Temperatures for 12 months ending {end_dt} for station {most_active_station[1]}:", all_tobs)


@app.route("/api/v1.0/start/<start>")
def start(start=None):
    # Create our session (link) from Python to the DB
    session = Session(engine) 

    """Return the min, max, and average temperatures calculated from the given start date (YYYY-MM-DD) to the end of the dataset"""
    # Set the start date from user input
    start_dt = (start)

    # Query the database to obtain temperature information from the given start date to the end of the dataset
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_dt).all()

    # Close the session
    session.close()
    
    # Convert list of tuples into normal list
    all_start = list(np.ravel(results))
        
    return jsonify(f"Temperatures between {start} and 2017-08-23: TMin={all_start[0]}, TMax={all_start[1]}, TAvg={all_start[2]}")


@app.route("/api/v1.0/start_end/<start>/<end>")
def start_end(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine) 
 
    # Set the dates for the date range based on user input
    start_dt = (start)
    end_dt = (end)

    """Return the min, max, and average temperatures calculated from the given start date and end date"""
    # Query the database to obtain the temperature information for requested date range 
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_dt).\
    filter(Measurement.date <= end_dt).all()

    # Close the session
    session.close()

    # Convert list of tuples into normal list
    all_end = list(np.ravel(results))

    return jsonify(f"Temperatures for the period {start} to {end}: TMin={all_end[0]}, TMax={all_end[1]}, TAvg={all_end[2]}")


if __name__ == '__main__':
    app.run(debug=True)
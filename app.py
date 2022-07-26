import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station 
print('cols',Measurement.__table__.columns.keys())

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



@app.route("/")
def Homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/measurement</br>"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
        f"/api/v1.0/tobs"
    )


# retrieve data from database
# Measuremnet = engine.execute("SELECT date, prcp  FROM measurement;")

        



@app.route("/api/v1.0/precipitation")
def precipitation():
        # Create our session (link) from Python to the DB

    prev_year = dt.date(2017,4,5) - dt.timedelta(days=365)
    session = Session(engine)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    session.close()
    # Query all measurement


    measurement_dict = {date: prcp for date, prcp in precipitation}
    #results = session.query(Measurement.date, Measurement.prcp).all()
    print(measurement_dict)

    return jsonify(measurement_dict)


        

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all measurement
    results = session.query(Measurement.staions).all()
    session.close()

    return jsonify(results)


@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    tobs_most_active_station = session.query(Measurement.date, Measurement.tobs ).\
    filter(Measurement.date > '2016-08-23').\
    filter(Measurement.station == 'USC00519281').all()
    session.close()


    return jsonify(tobs_most_active_station)



@app.route('/api/v1.0/<start_date>/<end_date>')
def start_end(start_date, end_date):
    
    
    session = Session(engine)
    query_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    session.close()
    temps = list(np.ravel(query_data))

    return jsonify(temps)
if __name__ == '__main__':
    app.run(debug=True)
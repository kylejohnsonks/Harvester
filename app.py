
# Import dependencies
from flask import Flask, render_template, redirect, session, jsonify
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import func, cast
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

from config import db_password

# Create a new Flask instance
app = Flask(__name__,template_folder='Templates')

# add the code to create the connection to the PostgreSQL database
db_string = f"postgresql://postgres:{db_password}@127.0.0.1:5432/Harvester"
engine = create_engine(db_string)

#create classes for tables
Base = automap_base()
Base.prepare(engine, reflect=True)
sr=Base.classes.solution_readings 

# Define root
@app.route('/')
def index():
    return render_template("index.html")

#measurements button
@app.route('/measurements')
def readings_page():
    return render_template("measurements.html")


#add solution reading function
@app.route('/measurements/solution/<ph>/<tds>/<volume>')
def add_solution_reading(ph,tds,volume):

    

    
    #with session, add record to sr table
    with Session(engine) as session:
        reading=sr(ph=ph,tds=tds,volume=volume,read_date=func.current_date())
        session.begin()
        try:
            session.add(reading)
        except:
            session.rollback()
            raise
        else:
            session.commit()
    # result = str('Successfully added measurement')
    result=(f"Successfully added measurement to solution readings: <br> pH={ph} <br> TDS={tds} <br> Volume={volume}")
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

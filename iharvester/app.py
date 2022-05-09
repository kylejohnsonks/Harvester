
# Import dependencies
from unittest import result
import datetime
from datetime import date
from flask import Flask, render_template, redirect, session, jsonify
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, func, cast, select, Table, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

from config import db_password

# Create a new Flask instance
app = Flask(__name__,template_folder='templates')

# add the code to create the connection to the PostgreSQL database
db_string = f"postgresql://rxlnazlfqdjqhm:{db_password}@ec2-52-200-215-149.compute-1.amazonaws.com:5432/dddgnv1vi3caf7"
engine = create_engine(db_string)


# Get table metadata
metadata_obj=MetaData()
sr_meta=Table("solution_readings",metadata_obj,autoload_with=engine)
sl_meta=Table("seed_lots",metadata_obj,autoload_with=engine)
s_meta=Table("seedlings",metadata_obj,autoload_with=engine)
plants_meta=Table("plants",metadata_obj,autoload_with=engine)
pt_meta=Table("plant_types",metadata_obj,autoload_with=engine)
pm_meta=Table("plant_measurements",metadata_obj,autoload_with=engine)

#create classes for tables
Base = automap_base()
Base.prepare(engine, reflect=True)
sr=Base.classes.solution_readings
sl=Base.classes.seed_lots
s=Base.classes.seedlings
plants=Base.classes.plants
pt=Base.classes.plant_types
pm=Base.classes.plant_measurements

# Define root
@app.route('/')
def index():
    return render_template("index.html")

# Route for solution chart
@app.route('/solutionchart')
def solution_chart():
    stmt=select(sr_meta).where(sr_meta.c.read_date > func.CURRENT_DATE()-30)
    ph=[]
    tds=[]
    volume=[]
    dates=[]
    with Session(engine) as session:
        for row in session.execute(stmt):
            dates.append(row[4].strftime("%Y-%m-%d"))
            ph.append(float(row[1]))
            tds.append(int(row[2]))
            volume.append(float(row[3]))

    #test data
    # xvals=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
   
    #combine data into dict
    all_data={'dates':dates,'ph':ph,'tds':tds,'volume':volume}

    # return dict
    return jsonify(all_data)

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

#Add plant type function


#Add seed lot function
@app.route('/measurements/seedlot/<vendor>/<order_date>/<quantity>/<price>/<product_url>/<plant_type_id>')
def add_seed_lot(vendor,order_date,quantity,price,product_url,plant_type_id):
    with Session(engine) as session:
        seedlot=sl(
            vendor=vendor,order_date=order_date,quantity=quantity,
            price=price,product_url=product_url,
            plant_type_id=plant_type_id
        )
        session.begin()
        try:
            session.add(seedlot)
        except:
            session.rollback()
            raise
        else:
            session.commit()

        for item in session.execute(select(func.max(sl.id))):
            sl_id=item[0]

    result=(f"Successfully added seed lot: {sl_id}")
    return jsonify(result)

#Add seedling function

#Add plant function

#Add plant measurement function



if __name__ == "__main__":
    app.run(debug=True)

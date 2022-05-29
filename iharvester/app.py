
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
host='ec2-3-234-131-8.compute-1.amazonaws.com'
db_name='d2o18jsmguf1st'
username='msiswhpqugztpy'
db_string = f"postgresql://{username}:{db_password}@{host}/{db_name}"
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

#measurements button
@app.route('/measurements')
def measurements_page():
    return render_template("measurements.html")

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
   
    #combine data into dict
    all_data={'dates':dates,'ph':ph,'tds':tds,'volume':volume}

    # return dict
    return jsonify(all_data)

@app.route('/dropdowns')
#get New seed lot drop down values
def dropdowns():
    pt_types=[]
    sl_ids=[]
    # s_update_ids=[]
    s_ids=[]
    plant_ids=[]
    stmt=select(pt_meta.c.type).distinct().order_by(pt_meta.c.type)
    with Session(engine) as session:
        for row in session.execute(stmt):
            pt_types.append(row[0])
    
    #new seedling, seed lot IDs
    stmt=select(sl_meta.c.id).order_by(sl_meta.c.id)
    with Session(engine) as session:
        for row in session.execute(stmt):
            sl_ids.append(row[0])

    # #Update seedling, seedling IDs
    stmt=select(s_meta.c.id).where(s_meta.c.germinated== None).order_by(s_meta.c.id)
    with Session(engine) as session:
        for row in session.execute(stmt):
            s_update_ids.append(row[0])

    # #New plant, seedling ID
    stmt=select(s_meta.c.id).where(s_meta.c.germinated=='true').order_by(s_meta.c.id)
    with Session(engine) as session:
        for row in session.execute(stmt):
            s_ids.append(row[0])

    #plant Measurement, plant ID
    stmt=select(plants_meta.c.id).order_by(plants_meta.c.id)
    with Session(engine) as session:
        for row in session.execute(stmt):
            plant_ids.append(row[0])

    dropdowns={'pt_types':pt_types,'sl_ids':sl_ids,'s_ids':s_ids,'plant_ids':plant_ids}
    return (jsonify(dropdowns))

#create list of varieties for given plant type
@app.route('/dropdowns/<plant_variety>')
def dropdown_plant_variety(plant_variety):
    dropdown_plant_variety=[]
    stmt=select(pt_meta.c.variety).where(pt_meta.c.type==plant_variety).order_by(pt_meta.c.type)
    with Session(engine) as session:
        for row in session.execute(stmt):
            dropdown_plant_variety.append(row[0])

    return (jsonify(dropdown_plant_variety))

#MEASUREMENT FUNCTIONS
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
@app.route('/measurements/seedlingadd/<seed_lot_id>')
def add_seedling(seed_lot_id):
    with Session(engine) as session:
        add_seedling=s(start_date=func.current_date(), seed_lot_id=seed_lot_id)
        session.begin()
        try:
            session.add(add_seedling)
        except:
            session.rollback()
        else:
            session.commit()
        for item in session.execute(select(func.max(s.id))):
            s_id=item[0]
    result=(f"Successfully added seedling: {s_id}")
    return jsonify(result)

#Update Seedling Function



#Add plant function

#Add plant measurement function


if __name__ == "__main__":
    app.run(debug=True)

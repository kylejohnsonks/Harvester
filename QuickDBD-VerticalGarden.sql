-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/L8C75k
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- Table documentation comment 1 (try the PDF/RTF export)

CREATE TABLE "solution_readings" (
    "reading_id" serial   NOT NULL,
    "ph" numeric   NOT NULL,
    -- Total dissolved solids (TDS) is measured as a volume of water with the unit milligrams per liter (mg/L), otherwise known as parts per million (ppm).
    "tds" numeric   NOT NULL,
    -- i.e. the amount of water in the tank in gallons
    "volume" numeric   NOT NULL,
    "read_date" date   NOT NULL,
    CONSTRAINT "pk_solution_readings" PRIMARY KEY (
        "reading_id"
     )
);

CREATE TABLE "plant_types" (
    "plant_type_id" serial   NOT NULL,
    "name" varchar   NOT NULL,
    "description" varchar   NOT NULL,
    "notes" varchar   NOT NULL,
    "planting_instructions" varchar   NOT NULL,
    CONSTRAINT "pk_plant_types" PRIMARY KEY (
        "plant_type_id"
     )
);

CREATE TABLE "seed_lots" (
    "seed_lot_id" serial   NOT NULL,
    "vendor" varchar   NOT NULL,
    "order_date" date   NOT NULL,
    "quantity" int   NOT NULL,
    "price" money   NOT NULL,
    "product_url" varchar   NOT NULL,
    "plant_type_id" int   NOT NULL,
    CONSTRAINT "pk_seed_lots" PRIMARY KEY (
        "seed_lot_id"
     )
);

CREATE TABLE "plants" (
    "plant_id" serial   NOT NULL,
    "start_date" date   NOT NULL,
    "seed_lot_id" int   NOT NULL,
    "plant_type_id" int   NOT NULL,
    "location" int   NOT NULL,
    "germination_date" date   NOT NULL,
    "germination_faliure" boolean   NOT NULL,
    "transfer_date" date   NOT NULL,
    CONSTRAINT "pk_plants" PRIMARY KEY (
        "plant_id"
     )
);

CREATE TABLE "plant_measurements" (
    "plant_measurement_id" serial   NOT NULL,
    "plant_id" int   NOT NULL,
    "size_x" numeric   NOT NULL,
    "size_y" numeric   NOT NULL,
    "size_z" numeric   NOT NULL,
    "leaf_count" int   NOT NULL,
    "measurement_date" date   NOT NULL,
    "harvest_volume" numeric   NOT NULL,
    CONSTRAINT "pk_plant_measurements" PRIMARY KEY (
        "plant_measurement_id"
     )
);

ALTER TABLE "seed_lots" ADD CONSTRAINT "fk_seed_lots_plant_type_id" FOREIGN KEY("plant_type_id")
REFERENCES "plant_types" ("plant_type_id");

ALTER TABLE "plants" ADD CONSTRAINT "fk_plants_seed_lot_id" FOREIGN KEY("seed_lot_id")
REFERENCES "seed_lots" ("seed_lot_id");

ALTER TABLE "plants" ADD CONSTRAINT "fk_plants_plant_type_id" FOREIGN KEY("plant_type_id")
REFERENCES "plant_types" ("plant_type_id");

ALTER TABLE "plant_measurements" ADD CONSTRAINT "fk_plant_measurements_plant_id" FOREIGN KEY("plant_id")
REFERENCES "plants" ("plant_id");


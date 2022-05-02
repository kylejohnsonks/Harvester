-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/L8C75k
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- Table documentation comment 1 (try the PDF/RTF export)

CREATE TABLE "solution_readings" (
    "id" integer   NOT NULL,
    "ph" numeric   NOT NULL,
    -- Total dissolved solids (TDS) is measured as a volume of water with the unit milligrams per liter (mg/L), otherwise known as parts per million (ppm).
    "tds" numeric   NOT NULL,
    -- i.e. the amount of water in the tank in gallons
    "volume" numeric   NOT NULL,
    "read_date" date   NOT NULL,
    CONSTRAINT "pk_solution_readings" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "plant_types" (
    "id" integer   NOT NULL,
    "type" varchar   NOT NULL,
    "variety" varchar   NOT NULL,
    "description" varchar   NULL,
    "notes" varchar   NULL,
    "planting_instructions" varchar   NULL,
    "ph" varchar NULL
    "tds" varchar NULL
    CONSTRAINT "pk_plant_types" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "seed_lots" (
    "id" integer   NOT NULL,
    "vendor" varchar   NULL,
    "order_date" date   NULL,
    "quantity" int   NULL,
    "price" money   NULL,
    "product_url" varchar   NULL,
    "plant_type_id" int   NOT NULL,
    CONSTRAINT "pk_seed_lots" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "plants" (
    "id" integer   NOT NULL,
    "location" int   NOT NULL,
    "transfer_date" date   NULL,
    "removal_date" date   NULL,
    "seedling_id" int   NOT NULL,
    CONSTRAINT "pk_plants" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "plant_measurements" (
    "id" integer   NOT NULL,
    "size_x" numeric   NOT NULL,
    "size_y" numeric   NOT NULL,
    "size_z" numeric   NOT NULL,
    "leaf_count" int   NULL,
    "measurement_date" date   NOT NULL,
    "harvest_volume" numeric   NULL,
    "plant_id" int   NOT NULL,
    CONSTRAINT "pk_plant_measurements" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "seedlings" (
    "id" integer   NOT NULL,
    "start_date" date   NOT NULL,
    "germination_date" date   NULL,
    "germination_faliure" boolean   NULL,
    "seed_lot_id" int   NOT NULL,
    CONSTRAINT "pk_seedlings" PRIMARY KEY (
        "id"
     )
);

ALTER TABLE "seed_lots" ADD CONSTRAINT "fk_seed_lots_plant_type_id" FOREIGN KEY("plant_type_id")
REFERENCES "plant_types" ("id");

ALTER TABLE "plants" ADD CONSTRAINT "fk_plants_seedling_id" FOREIGN KEY("seedling_id")
REFERENCES "seedlings" ("id");

ALTER TABLE "plant_measurements" ADD CONSTRAINT "fk_plant_measurements_plant_id" FOREIGN KEY("plant_id")
REFERENCES "plants" ("id");

ALTER TABLE "seedlings" ADD CONSTRAINT "fk_seedlings_seed_lot_id" FOREIGN KEY("seed_lot_id")
REFERENCES "seed_lots" ("id");


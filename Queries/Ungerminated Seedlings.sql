SELECT Count(pt.variety), pt.type, pt.variety
FROM seedlings as s
JOIN seed_lots as sl ON s.seed_lot_id=sl.id
JOIN plant_types as pt ON sl.plant_type_id=pt.id
WHERE s.germinated IS NULL
GROUP BY pt.type, pt.variety;
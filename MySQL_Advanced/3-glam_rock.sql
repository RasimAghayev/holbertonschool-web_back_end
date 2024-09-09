-- Search bands with style Glam rock
-- Calculate duration based on the current year if split is NULL
SELECT band_name, 
       IFNULL(split, YEAR(CURDATE())) - IFNULL(formed, 0) AS lifespan
FROM metal_bands 
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;

USE holberton;

-- Creating the result table
CREATE TEMPORARY TABLE glam_rock_bands AS
SELECT band_name, 
       (YEAR(split) - YEAR(formed)) AS lifespan
FROM metal_bands
WHERE main_style = 'Glam rock';

-- Selecting and ranking the bands by lifespan
SELECT band_name, 
       lifespan
FROM glam_rock_bands
ORDER BY lifespan DESC;

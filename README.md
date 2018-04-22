# idw02
Two options
1.- Fill voids from data stored in an Access DB with voids. The results are written en plain text files. hen, you can import this files to the DB.
2.- Interpolate values in points without data. Data are stored in the DB above.

We use the inverse distance wheigthed to interpolate precipitacion, temperature etc. data.
We use a variant of Shepards method https://en.wikipedia.org/wiki/Inverse_distance_weighting
We use the nearest data point in each quadrant nearest to a point without data, so we have a maximun of 4 points to do the interpolation

# idw02
Script to interpolate precipitacion, temperature etc. data using idw method
1.- Fill voids from data stored in an Access DB with voids. The results are written in plain text files. hen, you can import this files to the DB.
2.- Interpolate values in scatter points without data. Results are written in plain text files.

We use the inverse distance wheigthed to interpolate precipitacion, temperature etc. data.
We use a variant of Shepards method https://en.wikipedia.org/wiki/Inverse_distance_weighting
We use the nearest data point in each quadrant nearest to a point without data, so we have a maximun of 4 points to do the interpolation, one in each quadrant

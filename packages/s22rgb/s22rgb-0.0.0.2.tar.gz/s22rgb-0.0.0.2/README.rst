s22rgb mean sentinel 2 to rgb image.

The technical route is as follows:

1. Obtain the ZIP file list

2. The for loop runs iteratively and decompresses a single ZIP

3. Obtain the list of files in JP2 format, which corresponds to TIFF files of other remote sensing satellites

4.GDAL reads jp2 file, numpy calculates linear transformation, here using 2% linear transformation

5. Recombine it into a three-band matrix and save it as a common JPG format through OpencV

contact：ytkz11@163.com
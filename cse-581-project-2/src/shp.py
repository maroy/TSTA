import shapefile;

#with open("..\\data\\tl_2014_us_county.shp", "rb") as f:
sf = shapefile.Reader("..\\data\\tl_2014_us_county\\tl_2014_us_county")

shapesRecords = sf.shapeRecords()

result = {}

our_county_names = ["Lapeer", "Livingston", "Macomb", "Oakland", "St. Clair", "Wayne"]
for i in range(0, len(shapesRecords)):
    sr = shapesRecords[i]
    if sr.record[0] == '26' and sr.record[4] in our_county_names:
        result[sr.record[4]] = sr.shape.bbox

print result
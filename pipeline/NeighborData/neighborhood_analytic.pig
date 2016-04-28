record = LOAD 'zillow' as (address:chararray,longtitude:float,latitude:float,nearestLaundry:float,laundryNum:int,nearestSupermarkets:float,superMarketsNum:int,nearestTrainStation:float,trainStationNum:int);

record_grouped = group record ALL;
lng_max = foreach record_grouped generate 'max_longtitude',MAX(record.longtitude);
lat_max = foreach record_grouped generate 'max_latitude',MIN(record.latitude);

record_no_laundry = filter record by $4 == 0;
record_no_laundry_count = group record_no_laundry ALL;
no_laudry_count = foreach record_no_laundry_count generate 'no_laundry_count',COUNT($1);

record_no_supermarkets = filter record by $6 == 0;
record_no_supermarkets_count = group record_no_supermarkets ALL;
no_supermarkets_count = foreach record_no_supermarkets_count generate 'no_supermarkets_count',COUNT($1);

record_no_subway = filter record by $8 == 0;
record_no_subway_count = group record_no_subway ALL;
no_subway_count = foreach record_no_subway_count generate 'no_subway_count',COUNT($1);

final = union no_laudry_count,no_supermarkets_count,no_subway_count,lng_max,lat_max;
store final into 'analytic';
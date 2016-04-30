neighbor = LOAD 'neighborData' USING PigStorage('\t') AS (zpid:chararray,address:chararray,longtitude:float,latitude:float,nearestLaundry:float,laundryNum:int,nearestSupermarkets:float,superMarketsNum:int,nearestTrainStation:float,trainStationNum:int);

zillow = LOAD 'toJoinNeighbor' USING PigStorage('\t') AS (zpid:chararray, address:chararray, zipcode, beds, baths, size:int, price:int, months:int, lot:float, built:int);

house = join neighbor by zpid, zillow by zpid;

sorted_house = foreach house generate neighbor::zpid,zillow::zipcode,zillow::city,neighbor::longtitude,neighbor::latitude,neighbor::nearestLaundry,neighbor::laundryNum,neighbor::nearestSupermarkets,neighbor::superMarketsNum,neighbor::nearestTrainStation,neighbor::trainStationNum,zillow::beds,zillow::baths,zillow::size,zillow::sold,zillow::sale,zillow::rent,zillow::lot,zillow::transaction,zillow::built,zillow::parking;

STORE sorted_house INTO 'all_about_house'

complaints = LOAD 'complaintData' USING PigStorage('\t') AS (eid,time1,time2,cause,detail,city,zipcode,address,longtitde,latitude);

all_about_house = join complaints by zipcode, sorted_house by zipcode;

house_info = foreach all_about_house generate sorted_house::neighbor::zpid,sorted_house::zillow::zipcode,sorted_house::zillow::city,sorted_house::neighbor::longtitude,sorted_house::neighbor::latitude,sorted_house::neighbor::nearestLaundry,sorted_house::neighbor::laundryNum,sorted_house::neighbor::nearestSupermarkets,sorted_house::neighbor::superMarketsNum,sorted_house::neighbor::nearestTrainStation,sorted_house::neighbor::trainStationNum,sorted_house::zillow::beds,sorted_house::zillow::baths,sorted_house::zillow::size,sorted_house::zillow::sold,sorted_house::zillow::sale,sorted_house::zillow::rent,sorted_house::zillow::lot,sorted_house::zillow::transaction,sorted_house::zillow::built,sorted_house::zillow::parking,complaints::cause,complaints::city,complaints::longtitde,complaints::latitude;

STORE house_info INTO 'toModel';

/*

STORE all_about_house INTO 'all_about_house_test';

neighbor::zpid,
neighbor::address,
neighbor::longtitude,
neighbor::latitude,
neighbor::nearestLaundry,
neighbor::laundryNum,
neighbor::nearestSupermarkets,
neighbor::superMarketsNum,
neighbor::nearestTrainStation,
neighbor::trainStationNum,
zillow::zpid,
zillow::address,
zillow::street_address,
zillow::city,
zillow::state,
zillow::zipcode,
zillow::beds,
zillow::baths,
zillow::size,
zillow::sold,
zillow::sale,
zillow::rent,
zillow::lot,
zillow::transaction,
zillow::built,
zillow::parking

complaints::eid,
complaints::time1,
complaints::time2,
complaints::cause,
complaints::detail,
complaints::city,
complaints::zipcode,
complaints::address,
complaints::longtitde,
complaints::latitude,
sorted_house::neighbor::zpid,
sorted_house::zillow::zipcode,
sorted_house::zillow::city,
sorted_house::neighbor::longtitude,
sorted_house::neighbor::latitude,
sorted_house::neighbor::nearestLaundry,
sorted_house::neighbor::laundryNum,
sorted_house::neighbor::nearestSupermarkets,
sorted_house::neighbor::superMarketsNum,
sorted_house::neighbor::nearestTrainStation,
sorted_house::neighbor::trainStationNum,
sorted_house::zillow::beds,
sorted_house::zillow::baths,
sorted_house::zillow::size,
sorted_house::zillow::sold,
sorted_house::zillow::sale,
sorted_house::zillow::rent,
sorted_house::zillow::lot,
sorted_house::zillow::transaction,
sorted_house::zillow::built,
sorted_house::zillow::parking


sorted_house::neighbor::zpid,sorted_house::zillow::zipcode,sorted_house::zillow::city,sorted_house::neighbor::longtitude,sorted_house::neighbor::latitude,sorted_house::neighbor::nearestLaundry,sorted_house::neighbor::laundryNum,sorted_house::neighbor::nearestSupermarkets,sorted_house::neighbor::superMarketsNum,sorted_house::neighbor::nearestTrainStation,sorted_house::neighbor::trainStationNum,sorted_house::zillow::beds,sorted_house::zillow::baths,sorted_house::zillow::size,sorted_house::zillow::sold,sorted_house::zillow::sale,sorted_house::zillow::rent,sorted_house::zillow::lot,sorted_house::zillow::transaction,sorted_house::zillow::built,sorted_house::zillow::parkingcomplaints::cause,complaints::city,complaints::longtitde,complaints::latitude


zpid
address 
street
city
state
zipcode
beds
baths
space
sold
sale
rent
lot
soldDate
builtDate
parking
*/

data = LOAD 'zillowInputs.txt' USING PigStorage('\t') AS (zpid, address, street_address, city, state, zipcode, beds, baths, size:int, sold:int, sale:int, rent, lot, transaction, built, parking);
/*DUMP data;*/
usable = FILTER data BY sold != -1 OR sale != -1;
/*DUMP usable;*/
cleaned_state = FILTER usable BY state == 'NY';
/*cleaned_state_city = FILTER cleaned_state BY city == 'New York' OR city == 'Brooklyn' OR city == 'Bronx' OR city == 'Queens';*/
grouped_city = GROUP cleaned_state BY city;
distribution_city = FOREACH grouped_city GENERATE group, COUNT($1);
DUMP distribution_city;
for_sale = FILTER cleaned_state BY sale != -1 AND size != -1;
current_price_per_sqft = FOREACH for_sale GENERATE city, sale/size;
/*DUMP current_price_per_sqft;*/
grouped_city_for_sale = GROUP current_price_per_sqft BY city;
/*DUMP grouped_city_for_sale;*/
current_average_price_per_sqft_for_city = FOREACH grouped_city_for_sale GENERATE group, AVG($1.$1);
DUMP current_average_price_per_sqft_for_city;
has_sold_and_built_and_size = FILTER cleaned_state BY built != 'unknown' AND sold != -1 AND size != -1;
previous_price_per_sqft = FOREACH has_sold_and_built_and_size GENERATE built, sold/size;
/*DUMP has_sold_and_built;*/
grouped_year_has_sold = GROUP previous_price_per_sqft BY built;
/*DUMP grouped_year_has_sold;*/
previous_average_price_per_sqft_for_built_year = FOREACH grouped_year_has_sold GENERATE group, AVG($1.$1);
DUMP previous_average_price_per_sqft_for_built_year;  
 
/*STORE usable INTO 'report';*/   

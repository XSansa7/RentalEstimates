data = LOAD 'output_jxs' USING PigStorage('\t') AS (zpid, address, street_address, city, state, zipcode, beds, baths, size, prev_price, curr_price, rent, lot_size, transaction, built_time, parking_size);
/*DUMP data;*/
usable = FILTER data BY curr_price != 'unknown' OR transaction != 'unknown';
/*DUMP usable;*/
/*STORE usable INTO 'myreport';*/
clean_state = FILTER usable BY state == 'NY';
/*STORE clean_state INTO 'myreport2';*/
clean_state_city = FILTER clean_state BY city == 'Manhattan' OR city == 'Brooklyn' OR city == 'Bronx';
/*STORE clean_state_city INTO 'myreport3';*/
basic = FILTER clean_state_city BY beds != '-- beds' AND beds != 'Studio' AND baths != '-- baths' AND size != 'unknown' AND size != '-- sqft';
/*STORE basic INTO 'myreport4';*/
advanced = FILTER basic BY built_time != 'unknown' AND lot_size != 'unknown';
STORE advanced INTO 'myreport16';
grouped_by_parking = GROUP advanced BY parking_size;
types = FOREACH grouped_by_parking GENERATE group, COUNT($1);
/*STORE types INTO 'myreport13';*/
/*grouped_city = GROUP cleaned_state BY city;*/
/*distribution_city = FOREACH grouped_city GENERATE group, COUNT($1);*/
/*DUMP distribution_city;*/
/*for_sale = FILTER cleaned_state BY sale != -1 AND size != -1;*/
/*current_price_per_sqft = FOREACH for_sale GENERATE city, sale/size;*/
/*DUMP current_price_per_sqft;*/
/*grouped_city_for_sale = GROUP current_price_per_sqft BY city;*/
/*DUMP grouped_city_for_sale;*/
/*current_average_price_per_sqft_for_city = FOREACH grouped_city_for_sale GENERATE group, AVG($1.$1);*/
/*DUMP current_average_price_per_sqft_for_city;*/
/*has_sold_and_built_and_size = FILTER cleaned_state BY built != 'unknown' AND sold != -1 AND size != -1;*/
/*previous_price_per_sqft = FOREACH has_sold_and_built_and_size GENERATE built, sold/size;*/
/*DUMP has_sold_and_built;*/
/*grouped_year_has_sold = GROUP previous_price_per_sqft BY built;*/
/*DUMP grouped_year_has_sold;*/
/*previous_average_price_per_sqft_for_built_year = FOREACH grouped_year_has_sold GENERATE group, AVG($1.$1);*/
/*DUMP previous_average_price_per_sqft_for_built_year;*/  
 
/*STORE usable INTO 'report';*/   

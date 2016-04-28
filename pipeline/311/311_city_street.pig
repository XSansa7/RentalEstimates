record = LOAD 'newrows' USING PigStorage('\t');
delete_null = FILTER record BY $16 != '' AND $10 !='' AND $5 != '';
choose_target = FILTER delete_null BY $16 == 'BROOKLYN' OR $16 == 'BRONX' OR $16 == 'NEW YORK' OR $16 == 'STATEN ISLAND' OR $16 == 'JAMAICA' OR $16 == 'FLUSHING' OR $16 == 'ASTORIA' OR $16 == 'RIDGEWOOD' OR $16 == 'CORONA' OR $16 == 'FAR ROCKAWAY';
raw= FOREACH choose_target GENERATE $16,$10;
distinct_raw= DISTINCT raw;
results = ORDER distinct_raw BY $0;
STORE results INTO 'city_street';
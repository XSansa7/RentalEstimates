record = LOAD 'newrows' USING PigStorage('\t');
delete_null = FILTER record BY $16 != '' AND $10 !='' AND $5 !='';
get_target = FILTER delete_null BY $16 == 'BROOKLYN' OR $16 == 'BRONX' OR $16 == 'NEW YORK' OR $16 == 'STATEN ISLAND' OR $16 == 'JAMAICA' OR $16 == 'FLUSHING' OR $16 == 'ASTORIA' OR $16 == 'RIDGEWOOD' OR $16 == 'CORONA' OR $16 == 'FAR ROCKAWAY';
raw = FOREACH get_target GENERATE UPPER($5);
complain_group = GROUP raw BY $0;
complain_count = FOREACH complain_group GENERATE $0, COUNT($0);
results = ORDER complain_count BY $1 DESC;
STORE results INTO 'complain_type_order';
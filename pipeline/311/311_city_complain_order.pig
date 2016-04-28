record = LOAD 'newrows' USING PigStorage('\t');
delete_null = FILTER record BY $16 != '' AND $10 !='';
raw= FOREACH delete_null GENERATE UPPER($16),$5;
complain_group = GROUP raw BY $0;
complain_count = FOREACH complain_group GENERATE $0, COUNT($1);
results = ORDER complain_count BY $1 DESC;
STORE results INTO 'city_complain_order';
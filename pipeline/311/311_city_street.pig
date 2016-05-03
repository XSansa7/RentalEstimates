record = LOAD 'newrows' USING PigStorage('\t');
delete_null = FILTER record BY $16 != '' AND $10 !='';
raw= FOREACH delete_null GENERATE $16,$10;
distinct_raw= DISTINCT raw;
results = ORDER distinct_raw BY $0;
STORE results INTO 'newrows_result';
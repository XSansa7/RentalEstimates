record = LOAD 'newrows' USING PigStorage('\t');
delete_null = FILTER record BY $16 != '' AND $10 !='' AND $5 !='' AND $50 !='' AND $51!='';
get_target = FILTER delete_null BY $16 == 'BROOKLYN' OR $16 == 'BRONX' OR $16 == 'NEW YORK';
raw = FOREACH get_target GENERATE $0,$1,$2,$5,$6,UPPER($16),$8,$10,$50,$51;
results = ORDER raw BY $5;
STORE results INTO 'clean_data_three_city';
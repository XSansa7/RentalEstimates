addressFile = open('city_street','r')
out1 = open('city_st_clean_shx','w')
out2 = open('city_st_clean_jxs','w')
out3 = open('city_st_clean_gjq','w')
targets = ['Woodside','WOODHAVEN','SPRINGFIELD GARDENS','Rego Park','OZONE PARK','MASPETH','MIDDLE VILLAGE','MANHATTAN','BRONX','QUEENS','Brooklyn','Bellerose','CENTRAL PARK','COLLEGE POINT','COLUMBUS','CORONA','ELMHURST','ELMONT','ENGLEWOOD','FLUSHING','FOREST HILLS','Far Rockaway','Fresh Meadows','HOWARD BEACH','JAMAICA','KEW GARDENS','LITTLE NECK','Long Island City','ROSEDALE','Richmond Hill','SPRINGFIELD GARDENS']
for i in range(len(targets)):
  targets[i] = targets[i].lower()
out = out1
count = 0
for address in addressFile.readlines():
  address.strip()
  terms = address.split('\t')
  city = terms[0].lower()
  if city == 'new york':
    city = 'manhattan'
  street = terms[1]
  if count == 8000:
      out = out2
  if count == 16000:
      out = out3
  if city in targets:
    out.write(city+" "+street)
    count += 1
    

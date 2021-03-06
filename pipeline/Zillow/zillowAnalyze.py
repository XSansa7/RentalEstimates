zillow = sc.textFile("toJoinNeighbor").distinct()
zipcode = zillow.map(lambda l: [l.split("\t")[2]]+[float(l.split("\t")[6])/float(l.split("\t")[5])])
grouped = zipcode.groupByKey().mapValues(list)
price_by_zip = grouped.map(lambda l:[l[0]]+[sum(map(lambda k:float(k),l[1]))/len(l[1])])
price_by_zip_ordered = price_by_zip.takeOrdered(price_by_zip.count(),key=lambda x:x[1])
print price_by_zip_ordered

years = zillow.map(lambda l: [l.split("\t")[-1]]+[float(l.split("\t")[6])/float(l.split("\t")[5])])
years_grouped = years.groupByKey().mapValues(list)
price_by_year = years_grouped.map(lambda l:[l[0]]+[sum(map(lambda k:float(k),l[1]))/len(l[1])])
price_by_year_ordered = price_by_year.takeOrdered(price_by_year.count(),key=lambda x:x[1])
print price_by_year_ordered
neighbor = sc.textFile("neighborData").distinct().map(lambda l:(l.split("\t")[0],l.split("\t")[1:])).filter(lambda l:len(l[1])==9)
n = neighbor.map(lambda l:[l[0]]+l[1])
laundry_average = n.map(lambda l:float(l[4])).sum()/n.count()
supermarket_average = n.map(lambda l:float(l[6])).sum()/n.count()
subway_average = n.map(lambda l:float(l[8])).sum()/n.count()
count = n.count()
max_laundry = n.map(lambda l:float(l[4])).max()
min_laundry = n.map(lambda l:float(l[4])).min()
average_laundry = n.map(lambda l:float(l[4])).sum()/count

max_super = n.map(lambda l:float(l[6])).max()
min_super = n.map(lambda l:float(l[6])).min()
average_super = n.map(lambda l:float(l[6])).sum()/count

max_subway = n.map(lambda l:float(l[8])).max()
min_subway = n.map(lambda l:float(l[8])).min()
average_subway = n.map(lambda l:float(l[8])).sum()/count

import math
#from pyspark.mllib.regression import LinearRegressionWithSGD, LabeledPoint

def rad(value):
    return (math.pi/180)*value


def distance(lat1,lng1,lat2,lng2):
    radlat1=rad(lat1)
    radlat2=rad(lat2)
    a=radlat1-radlat2
    b=rad(lng1)-rad(lng2)
    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    earth_radius=6378.137
    s=s*earth_radius
    if s<0:
        return -s
    else:
        return s


## join datasets
neighbor = sc.textFile("neighborData").distinct().map(lambda l:(l.split("\t")[0],l.split("\t")[1:])).filter(lambda l:len(l[1])==9)
zillow = sc.textFile("toJoinNeighbor").distinct().map(lambda l:(l.split("\t")[0],l.split("\t")[1:]))
complaints = sc.textFile("complaintData").map(lambda l:(l.split("\t")[6],[l.split("\t")[3]]+[l.split("\t")[5]]+l.split("\t")[-2:]))
house = neighbor.join(zillow).map(lambda l:[l[0]]+l[1][0]+l[1][1][1:]).map(lambda l:(l[10],l[0:10]+l[11:]))
complaints_part = complaints.sample(False,0.05,81)
all_about_house = complaints_part.join(house).map(lambda l:l[1][1]+l[1][0])
# all_about_house = sc.textFile("all_about_house_list")
# 
# all_about_house = sc.textFile("/user/hs3048/house_complaints") # entries with complaints
# house_detail = sc.textFile("/user/hs3048/neighborJoined") # house infomation without complaints
# all_about_house_list = all_about_house.map(lambda t: t.split('\t'))
valid_entries = all_about_house.filter(lambda l: l[2] != "" and l[3] != "" and l[-2] != "" and l[-1] != "" and distance(float(l[2]),float(l[3]),float(l[-2]),float(l[-1])) <= 0.5)
valid_entries = valid_entries.map(lambda e:(e[0],e))
grouped = valid_entries.groupByKey().mapValues(list)
z = grouped.map(lambda l:(l[0],map(lambda k:k[17],l[1])))
s = z.map(lambda p: (p[0],str(sum(map(lambda l: 1 if l==u'heating' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'noise' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'plumbing' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'general construction' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'paint/plaster' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'blocked driveway' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'street condition' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'illegal parking' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'water condition' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'electric' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'rodent' else 0,p[1]))),str(sum(map(lambda l: 1 if l==u'other' else 0,p[1]))))).map(lambda l:(l[0],l[1:]))

house_detail = house.map(lambda t:(t[1][0],[t[1][0]]+[t[0]]+t[1][1:]))

final_data = house_detail.join(s)
final_data = final_data.map(lambda l:[l[0]]+l[1][0][:]+list(l[1][1]))
final_data = final_data.map(lambda l:"\t".join(l))
final_data.saveAsTextFile("final_data")
# build model
# features = final_data.map(lambda line:{'feature':line.split("\t")[:-1],'result':line.split("\t")[-1]})
# points = features.map(lambda pair:LabeledPoint(pair['result'],pair['feature']))
# model = LinearRegressionWithSGD.train(point,iterations=100,intercept=True,step=0.0000001)
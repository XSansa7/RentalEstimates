from pyspark.mllib.regression import LinearRegressionWithSGD, LabeledPoint

dataFile = sc.textFile("x28.txt")
features = alldata.map(lambda line:{'feature':line.split("\t")[:-1],'result':line.split("\t")[-1]})
points = features.map(lambda pair:LabeledPoint(pair['result'],pair['feature']))
model = LinearRegressionWithSGD.train(point,iterations=100,intercept=True,step=0.0000001)

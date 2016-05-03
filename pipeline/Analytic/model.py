from pyspark.mllib.tree import GradientBoostedTrees, GradientBoostedTreesModel
from pyspark.mllib.regression import LinearRegressionWithSGD, LabeledPoint
from pyspark.mllib.feature import Normalizer
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.util import MLUtils
from pyspark.mllib.regression import IsotonicRegression, IsotonicRegressionModel
from pyspark.mllib.evaluation import RegressionMetrics
from pyspark import SparkContext
from pyspark.mllib.feature import StandardScaler

sc = SparkContext()
dataFile = sc.textFile("final_data")
dataFile_select = dataFile.map(lambda line:line.split("\t")[6:])
dataFile_to_float = dataFile_select.map(lambda line:map(lambda w:float(w),line))
# consider all aspects
to_model = dataFile_to_float.map(lambda l:{'feature':l[:8]+[l[8]/2000]+l[10:12]+l[13:],'result':l[9]})

# consider only internal facts
#to_model = dataFile_to_float.map(lambda l:{'feature':l[6:8]+[l[8]/2000]+l[10:12],'result':l[9]})

# consider partial other factors
#to_model = dataFile_to_float.map(lambda l:{'feature':l[:7]+[l[8]/2000],'result':l[9]})

points = to_model.map(lambda pair:LabeledPoint(pair['result'],pair['feature']))
#(trainingData, testData) = points.randomSplit([0.8, 0.2])
# normalize
labels = points.map(lambda x:x.label)
features = points.map(lambda x:x.features)
#normalizer = Normalizer()
#normData = labels.zip(normalizer.transform(features)).map(lambda x:LabeledPoint(x[0],x[1]))
scaler = StandardScaler().fit(features)
scaData = labels.zip(scaler.transform(features))
(trainingData_l, testData_l) = scaData.randomSplit([0.8, 0.2])
trainingData = trainingData_l.map(lambda l:LabeledPoint(l[0],l[1]))
testData = testData_l.map(lambda l:LabeledPoint(l[0],l[1]))
#model = LinearRegressionWithSGD.train(trainingData,iterations=1000,intercept=True,initialWeights=[1000]*7+[3000]+[2000],step=0.001)
#model = LinearRegressionWithSGD.train(trainingData,iterations=100000,intercept=True,regType='l2',step=0.0004)
#model = LinearRegressionWithSGD.train(trainingData,iterations=1000,intercept=True,regType='l1',step=0.01)
#model = LinearRegressionWithSGD.train(trainingData,iterations=10,intercept=True,regType='l1',step=0.00031)
#model = LinearRegressionWithSGD.train(trainingData,iterations=10000,intercept=True,regType='l1',step=0.0025)

# with all factors
# to_model = dataFile_to_float.map(lambda l:{'feature':l[:8]+[l[8]/2000]+l[10:12]+l[13:],'result':l[9]}) r^2=0.31569051647475987
model = LinearRegressionWithSGD.train(trainingData,iterations=1000,intercept=True,regType='l1',step=0.375)


# without complaints
# to_model = dataFile_to_float.map(lambda l:{'feature':l[:7]+[l[8]/2000],'result':l[9]}) r^2:0.15743232037132104
# model = LinearRegressionWithSGD.train(trainingData,iterations=10000,intercept=True,regType='l1',step=0.746)

# only internal factors
# to_model = dataFile_to_float.map(lambda l:{'feature':l[6:8]+[l[8]/2000]+l[10:12],'result':l[9]}) r^2:0.10478991443409424
# model = LinearRegressionWithSGD.train(trainingData,iterations=3000,intercept=True,regType='l1',step=1.14)


#model = GradientBoostedTrees.trainRegressor(trainingData,categoricalFeaturesInfo={}, numIterations=100)
#model = RandomForest.trainRegressor(trainingData, categoricalFeaturesInfo={},numTrees=10, featureSubsetStrategy="auto",impurity='variance', maxDepth=30, maxBins=32)

#predictions = model.predict(testData.map(lambda x: x.features))
#labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
valuesAndPreds = testData.map(lambda p: (float(model.predict(p.features)), p.label))
metrics = RegressionMetrics(valuesAndPreds)
metrics.r2
testMSE = labelsAndPredictions.map(lambda (v, p): (v - p) * (v - p)).sum()/float(testData.count())
print metrics.r2


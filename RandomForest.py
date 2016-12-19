
###pyspark --packages com.databricks:spark-csv_2.10:1.2.0

from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler

df=sqlContext.read.load('/Users/ruixuanzhang/Desktop/voice.csv',format='com.databricks.spark.csv',header='true',inferSchema='true')
labelIndexer = StringIndexer(inputCol="label", outputCol="indexedLabel").fit(df)
#labelIndexer = StringIndexer(inputCol="_c28",outputCol="indexedLabel").fit(df)

#####Try to use different features here
#assembler=VectorAssembler(inputCols=["_c1","_c2","_c3","_c4","_c5","_c6","_c7","_c8","_c9","_c10","_c11","_c12","_c13","_c14","_c15","_c16","_c17","_c18","_c19","_c20","_c21","_c22","_c23","_c24","_c25"],outputCol="features")
#assembler=VectorAssembler(inputCols=["meanfreq","sd","median","Q25","Q75","IQR","skew","kurt","sfm","mode","centroid","meanfun","minfun","maxfun","meandom","mindom","maxdom","dfrange","modindx"],outputCol="features")
#assembler=VectorAssembler(inputCols=["meanfreq","sd","median","Q25","Q75","IQR","sfm","mode","centroid","meanfun","maxfun","meandom","maxdom","dfrange","modindx"],outputCol="features")
#assembler=VectorAssembler(inputCols=["meanfreq","sd","median","Q25","Q75","minfun","sfm","mode","centroid","meanfun","maxfun","meandom","maxdom","dfrange","modindx"],outputCol="features")
#single test
#assembler=VectorAssembler(inputCols=["meanfreq","sd","median","Q25","Q75","IQR","skew","kurt","sfm","mode","centroid","meanfun","minfun","maxfun","meandom","mindom","maxdom","dfrange"],outputCol="features")
#assembler=VectorAssembler(inputCols=["_c1","_c2","_c3","_c4","_c5","_c6","_c7","_c8","_c9","_c10","_c11","_c12","_c13","_c14","_c15","_c16","_c17","_c18","_c19","_c20","_c21","_c22","_c23","_c24","_c25"],outputCol="features")
#assembler=VectorAssembler(inputCols=["IQR","kurt","sfm","centroid","meanfun","meandom","mindom","maxdom","dfrange","modindx"],outputCol="features")
assembler=VectorAssembler(inputCols=["meanfreq","sd","median","Q25","Q75","IQR","skew","kurt","sfm","mode","centroid","meanfun","minfun","maxfun","meandom","mindom","maxdom","dfrange","modindx"],outputCol="features")
assembled=assembler.transform(df)
featureIndexer=VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=30).fit(assembled)
(trainingData,testData)=assembled.randomSplit([0.75,0.25])
rf=RandomForestClassifier(labelCol="indexedLabel",featuresCol="indexedFeatures",numTrees=50)
pipeline = Pipeline(stages=[labelIndexer,featureIndexer,rf])
model = pipeline.fit(trainingData)
predictions = model.transform(testData)
predictions.select("prediction","indexedLabel","features").show(5)
evaluator = MulticlassClassificationEvaluator( labelCol = "indexedLabel", predictionCol= "prediction", metricName = "accuracy" )
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g" % (1.0 - accuracy))

rfModel = model.stages[2]


####0.29

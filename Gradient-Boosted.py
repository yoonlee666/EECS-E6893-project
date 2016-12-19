### start with this sentence
###pyspark --packages com.databricks:spark-csv_2.10:1.2.0

from pyspark.ml import Pipeline
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.feature import StringIndexer, VectorIndexer
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

df=sqlContext.read.load('/Users/ruixuanzhang/Documents/FISEMESTER/BDA/BDA_PROJECT/Sound/data.csv',format='com.databricks.spark.csv',header='false',inferSchema='true')
labelIndexer = StringIndexer(inputCol="_c27",outputCol="indexedLabel").fit(df)
assembler=VectorAssembler(inputCols=["_c1","_c2","_c3","_c4","_c5","_c6","_c7","_c8","_c9","_c10","_c11","_c12","_c13","_c14","_c15","_c16","_c17","_c18","_c19","_c20","_c21","_c22","_c23","_c24","_c25","_c26"],outputCol="features")
assembled=assembler.transform(df)

featureIndexer=VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=30).fit(assembled)
(trainingData,testData)=assembled.randomSplit([0.8,0.2])
gbt = GBTClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", maxIter=10)

pipeline = Pipeline(stages=[labelIndexer, featureIndexer,gbt])
model = pipeline.fit(trainingData) # warn exists
predictions = model.transform(testData)
predictions.select("prediction","indexedLabel","features").show(5)
evaluator = MulticlassClassificationEvaluator(labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g" % (1.0 - accuracy))

#!/bin/bash
#
if [ "$1" = "--help" ] || [ "$1" = "--?" ]; then
  echo "This script runs Bayes classifiers and SGD over voice.csv in project Genger Recognition by Voice..."
  exit
fi
SCRIPT_PATH=${0%/*}
if [ "$0" != "$SCRIPT_PATH" ] && [ "$SCRIPT_PATH" != "" ]; then
  cd $SCRIPT_PATH
fi

START_PATH=$MAHOUT_HOME/project
export MAHOUT_LOCAL='true'

algorithm=( clean-up naivebayes-MapReduce sgd naivebayes-Spark  )
if [ -n "$1" ]; then
  choice=$1
else
  echo "Please select a number to choose the corresponding task to run"
  echo "1. ${algorithm[0]}-- cleans up the work area in $WORK_DIR"     #clean up
  echo "2. ${algorithm[1]}"                                            #naivebayes-MapReduce
  echo "3. ${algorithm[2]}"                                            #sgd
  echo "4. ${algorithm[3]}"                                            #naivebayes-Spark
  read -p "Enter your choice : " choice
fi

echo "ok. You chose $choice and we'll use ${algorithm[$choice-1]}"
alg=${algorithm[$choice-1]}

#set -e
if  ( [ "x$alg" == "xnaivebayes-MapReduce" ] ); then
  if [ -e $MAHOUT_HOME/mahout_voice ]; then
    echo "please do clean up first :)"
    exit 1
  else
    echo "creating work directory at ${WORK_DIR}"
    mkdir -p $MAHOUT_HOME/mahout_voice
    export WORK_DIR=$MAHOUT_HOME/mahout_voice
    cd ${WORK_DIR}
    echo "downloading zip file..."
    wget https://github.com/yoonlee666/EECS-E6893-project/raw/master/voice.csv.zip
    echo "extracting zip file..."
    unzip voice.csv.zip voice.csv
    echo "splitting data from csv file..."
    mkdir voice-all
    mkdir all
    mkdir voice-all/male
    mkdir voice-all/female
    python $START_PATH/split_NB.py
    rm -rf all
    echo "Creating sequence files from voice data"
    $MAHOUT_HOME/bin/mahout seqdirectory -i ${WORK_DIR}/voice-all -o ${WORK_DIR}/voice-seq -ow
    echo "Converting sequence files to vectors"
    $MAHOUT_HOME/bin/mahout seq2sparse -i ${WORK_DIR}/voice-seq -o ${WORK_DIR}/voice-vectors  -ow -lnorm -seq  -wt tfidf
    echo "Creating training and holdout set with a random 80-20 split of the generated vector dataset"
    $MAHOUT_HOME/bin/mahout split -i ${WORK_DIR}/voice-vectors/tfidf-vectors --trainingOutput ${WORK_DIR}/voice-train-vectors \
    --testOutput ${WORK_DIR}/voice-test-vectors --randomSelectionPct 10 --overwrite --sequenceFiles -xm sequential
    echo "Training Naive Bayes model"
    $MAHOUT_HOME/bin/mahout trainnb -i ${WORK_DIR}/voice-train-vectors -o ${WORK_DIR}/model -li ${WORK_DIR}/labelindex -ow $c
    echo "Self testing on training set"
    $MAHOUT_HOME/bin/mahout testnb -i ${WORK_DIR}/voice-train-vectors -m ${WORK_DIR}/model -l ${WORK_DIR}/labelindex -ow -o ${WORK_DIR}/voice-testing $c
    echo "Testing on holdout set"
    $MAHOUT_HOME/bin/mahout testnb -i ${WORK_DIR}/voice-test-vectors -m ${WORK_DIR}/model -l ${WORK_DIR}/labelindex -ow -o ${WORK_DIR}/voice-testing $c
  fi

elif [ "x$alg" == "xsgd" ]; then
  if [ -e $MAHOUT_HOME/mahout_voice ]; then
    echo "please do clean up first :)"
    exit 1
  else
    echo "creating work directory at ${WORK_DIR}"
    mkdir -p $MAHOUT_HOME/mahout_voice
    export WORK_DIR=$MAHOUT_HOME/mahout_voice
    cd ${WORK_DIR}
    echo "downloading zip file..."
    wget https://github.com/yoonlee666/EECS-E6893-project/raw/master/voice.csv.zip
    echo "extracting zip file..."
    unzip voice.csv.zip voice.csv
    echo "splitting data from csv file..."
    mkdir voice-all && mkdir voice-all/voice-train && mkdir voice-all/voice-train/male && mkdir voice-all/voice-train/female
    mkdir voice-all/voice-test && mkdir voice-all/voice-test/male && mkdir voice-all/voice-test/female
    python $START_PATH/split_sgd.py
    echo "Training on ${WORK_DIR}/voice-all/voice-train/"
    $MAHOUT_HOME/bin/mahout org.apache.mahout.classifier.sgd.TrainNewsGroups ${WORK_DIR}/voice-all/voice-train/
    echo "Testing on ${WORK_DIR}/voice-all/voice-test/ with model: /tmp/news-group.model"
    $MAHOUT_HOME/bin/mahout org.apache.mahout.classifier.sgd.TestNewsGroups --input ${WORK_DIR}/voice-all/voice-train/ --model ${WORK_DIR}/model

  fi

elif [ "x$alg" == "xclean-up" ]; then
  rm -rf $WORK_DIR
  rm -rf /tmp/news-group.model
fi

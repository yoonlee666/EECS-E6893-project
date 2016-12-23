#!/bin/bash
# Run Naive Bayes in Mahout
if [ "$1" = "--help" ] || [ "$1" = "--?" ]; then
  echo "This script runs Bayes classifiers over voice.csv in project Genger Recognition by Voice..."
  exit
fi
SCRIPT_PATH=${0%/*}
if [ "$0" != "$SCRIPT_PATH" ] && [ "$SCRIPT_PATH" != "" ]; then
  cd $SCRIPT_PATH
fi

START_PATH=$MAHOUT_HOME/project
export MAHOUT_LOCAL='true'

algorithm=( clean-up naivebayes-MapReduce  )
if [ -n "$1" ]; then
  choice=$1
else
  echo "Please select a number to choose the corresponding task to run"
  echo "1. ${algorithm[0]}-- cleans up the work area in $WORK_DIR"     #clean up
  echo "2. ${algorithm[1]}"                                            #naivebayes-MapReduce
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
#    $MAHOUT_HOME/bin/mahout seq2sparse -i ${WORK_DIR}/voice-seq -o ${WORK_DIR}/voice-vectors -lnorm -nv  -wt tfidf
    $MAHOUT_HOME/bin/mahout seq2sparse -i ${WORK_DIR}/voice-seq -o ${WORK_DIR}/voice-vectors -lnorm -nv
    echo "Creating training and holdout set with a random 80-20 split of the generated vector dataset"
    $MAHOUT_HOME/bin/mahout split -i ${WORK_DIR}/voice-vectors/tf-vectors --trainingOutput ${WORK_DIR}/voice-train-vectors \
    --testOutput ${WORK_DIR}/voice-test-vectors --randomSelectionPct 40 --overwrite --sequenceFiles -xm sequential
    echo "Training Naive Bayes model"
    $MAHOUT_HOME/bin/mahout trainnb -i ${WORK_DIR}/voice-train-vectors -o ${WORK_DIR}/model -li ${WORK_DIR}/labelindex -ow $c
    echo "Self testing on training set"
    $MAHOUT_HOME/bin/mahout testnb -i ${WORK_DIR}/voice-train-vectors -m ${WORK_DIR}/model -l ${WORK_DIR}/labelindex -ow -o ${WORK_DIR}/voice-testing $c
    echo "Testing on holdout set"
    $MAHOUT_HOME/bin/mahout testnb -i ${WORK_DIR}/voice-test-vectors -m ${WORK_DIR}/model -l ${WORK_DIR}/labelindex -ow -o ${WORK_DIR}/voice-testing $c
  fi

elif [ "x$alg" == "xclean-up" ]; then
  rm -rf $WORK_DIR
  rm -rf /tmp/news-group.model
fi

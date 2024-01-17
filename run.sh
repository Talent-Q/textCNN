#!/bin/bash

echo "Start..."

cd /home/talentq/workstation/project/textCNN
source ../../venv/textCNN/bin/activate

log_dir="./log"
time=$(date "+/%Y%m%d_%H%M%S.log")
log_path=$log_dir$time

nohup python w0_TextCNN6-20_30_40\(2_lr\).py > $log_path 2>&1 &

echo ""
sleep 1
ps -ef | grep "w0_TextCNN6"
#!/bin/bash

# 回显当前时间
echo "Start..."
time=$(date "+%Y-%m-%d %H:%M:%S")
echo -e "Time: $time\n"

# 激活虚拟环境
cd /home/talentq/workstation/project/textCNN
source ../../venv/textCNN/bin/activate

# 后台执行
echo -e "\n\n" >> './detect_log/nohup_err.log'
nohup python w0_TextCNN6-20_30_40\(2_lr\).py > /dev/null 2>>'./detect_log/nohup_err.log' &

# 查看进程
sleep 1
ps -ef | grep -v grep | grep -E "UID|w0_TextCNN6"

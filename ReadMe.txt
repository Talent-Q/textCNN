安装环境：
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


运行程序：
./run.sh


查看显卡：
watch -n 2 nvidia-smi


每日操作：
git pull
git add .
git commit -m ""
git push

 
# 解决显卡一直被 /usr/bin/nvidia/update 占用
ps -ef | grep /usr/bin/nvidia/update
sudo readlink -f /proc/<pid>/exe
sudo chmod -x /dev/shm/.cache/javra

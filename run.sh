# coding=utf-8

######  欢迎使用脚本任务，首先让我们熟悉脚本任务的一些使用规则  ######
# 脚本任务支持两种运行方式

# 1.shell 脚本. 在 run.sh 中编写项目运行时所需的命令，并在启动命令框中填写 bash run.sh <参数1> <参数2>使脚本任务正常运行.

# 2.python 指令. 在 run.py 编写运行所需的代码，并在启动命令框中填写 python run.py <参数1> <参数2> 使脚本任务正常运行.

#注：run.sh、run.py 可使用自己的文件替代。

###数据集文件目录
# datasets_prefix = '/root/paddlejob/workspace/train_data/datasets/'

# 数据集文件具体路径请在编辑项目状态下通过左侧导航「数据集」中文件路径拷贝按钮获取
# train_datasets =  '通过路径拷贝获取真实数据集文件路径 '

# 输出文件目录. 任务完成后平台会自动把该目录所有文件压缩为tar.gz包，用户可以通过「下载输出」可以将输出信息下载到本地.
# output_dir = "/root/paddlejob/workspace/output"

# 日志记录. 任务会自动记录环境初始化日志、任务执行日志、错误日志、执行脚本中所有标准输出和标准出错流(例如print()),用户可以在「提交」任务后,通过「查看日志」追踪日志信息.
#pip install opencv-contrib-python -i https://pypi.douban.com/simple/
#pip install wechaty==0.7dev17 -i https://pypi.douban.com/simple/
pip install wechaty==0.8 -i https://pypi.douban.com/simple/
pip install moviepy
pip install paddlenlp

# 设置环境变量
export WECHATY_PUPPET_SERVICE_TOKEN="puppet_padlocal_2your_id7"
WECHATY_PUPPET_SERVICE_TOKEN=kevinsun

# 运行python文件
python run_bot.py
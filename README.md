DICT
====

**怎么安装**

- 下载 dict.py 到电脑里

>curl -s https://raw.githubusercontent.com/YeXiaoRain/DICT/master/DICT.py > yourpath/dict.py

- 编辑 ~/.bashrc

>sudo vim ~/.bashrc`

- 在末尾加上

>alias youdao='python yourpath/dict.py'

- 使用：

>youdao word or sentence

- 也可以直接使用：

>curl -s https://raw.githubusercontent.com/YeXiaoRain/DICT/master/DICT.py | python - word or sentence

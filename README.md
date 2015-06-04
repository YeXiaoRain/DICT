DICT
====

**怎么安装**

- 下载 dict.py 到电脑里

```Bash
curl -o dict.py https://raw.githubusercontent.com/YeXiaoRain/DICT/master/DICT.py 
```

- 编辑 ~/.bashrc

```Bash
sudo vim ~/.bashrc
```

- 在末尾加上

```Bash
alias youdao='python yourpath/dict.py'
```

- 使用：

```Bash
youdao word or sentence
```

- 也可以直接使用：

```Bash
curl -s https://raw.githubusercontent.com/YeXiaoRain/DICT/master/DICT.py | python - word or sentence
```


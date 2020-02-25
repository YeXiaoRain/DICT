DICT
====

**怎么安装**

- 下载 dict.py 到电脑里

```Bash
curl -o dict.py https://raw.githubusercontent.com/YeXiaoRain/DICT/python2/DICT.py 
```

- 编辑 ~/.bashrc

```Bash
sudo vim ~/.bashrc
```

- 在末尾加上

```Bash
alias youdao='python2 <yourpath>/dict.py'
```

- 使用：

```Bash
youdao word or sentence
```

- 也可以直接使用：

```Bash
curl -s https://raw.githubusercontent.com/YeXiaoRain/DICT/python2/DICT.py | python2 - word or sentence
```


- 其它翻译项目(如nodejs分支):

|repo|source|comment|modified|
|---|---|---|---|
|[command-line-tool/dictionary](https://github.com/command-line-tool/dictionary)|youdaoapi|不支持句子|youdaodict|
|[syaning/dict-en-zh](https://github.com/syaning/dict-en-zh)|youdao网页/shanbayapi|shanbay源比较垃圾|-|
|[Toybreak/cliDict](https://github.com/Toybreak/cliDict)|bing|没有中->英 不支持句子|bingdict|
|[justinleoye/tuzki-dict](https://github.com/justinleoye/tuzki-dict)||chrome插件|-|


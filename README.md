DICT
====

**怎么安装**

- 下载 dict.py 到电脑里

```Bash
curl -o dict.py https://raw.githubusercontent.com/YeXiaoRain/DICT/python3/DICT.py 
```

- 编辑 ~/.bashrc

```Bash
sudo vim ~/.bashrc
```

- 在末尾加上

```Bash
alias y='python3 <yourpath>/DICT.py'
```

- 使用：

```Bash
y word or sentence
```

- 也可以直接执行脚本进行交互式翻译：

`y`


- 也可以直接使用：

```Bash
curl -s https://raw.githubusercontent.com/YeXiaoRain/DICT/python3/DICT.py | python3 - word or sentence
```

# 启用OpenapiYoudao

去`https://ai.youdao.com/`创建应用

复制`_config.ini`为`config.ini`并配置你的`APP_ID`和`APP_SECRET`

如果没有配置则不会调用`OpenapiYoudao`

# 其它翻译项目(如nodejs分支):

|repo|source|comment|modified|
|---|---|---|---|
|[command-line-tool/dictionary](https://github.com/command-line-tool/dictionary)|youdaoapi|不支持句子|youdaodict|
|[syaning/dict-en-zh](https://github.com/syaning/dict-en-zh)|youdao网页/shanbayapi|shanbay源比较垃圾|-|
|[Toybreak/cliDict](https://github.com/Toybreak/cliDict)|bing|没有中->英 不支持句子|bingdict|
|[justinleoye/tuzki-dict](https://github.com/justinleoye/tuzki-dict)||chrome插件|-|


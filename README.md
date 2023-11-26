# DICT

## Install

```bash
apt install python3 python3-pip git
git clone https://github.com/YeXiaoRain/DICT.git -b python3
pip install --user requirememnts.txt

# edit ~/.bashrc
alias y='python3 <your path>/DICT.py'
# or
alias g='python3 <your path>/googletranslator.py'
```

## Usage

```bash
y 你好
y word or sentence
g google 翻译可能需要proxy
```

## Enable OpenapiYoudao

去`https://ai.youdao.com/`创建应用

复制`_config.ini`为`config.ini`并配置你的`APP_ID`和`APP_SECRET`

如果没有配置则不会调用`OpenapiYoudao`

## Deps

- ~~<http://fanyi.youdao.com>~~
- yodao.com
- <https://openapi.youdao.com/api>
- googletrans

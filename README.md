# RentalEstimates

Apr 3, 2016

##什么也没干

==
Apr 6. 2016

##可以一起来用google API抓链接啦

先用google帐号在这里注册一个projcet https://console.developers.google.com/apis/, 启用custom search api，把google api的key记下来。

然后在这里 https://cse.google.com/cse/all 创建一个自定义搜索引擎，获取搜索引擎ID

把你们刚刚申请的对应的Google API key和Custom Search Engine ID填进keyFile里以后就可以跑了（左边API key，右边cse ID，中间用tab隔开）。

用的代码是`searchForLinks.py`，每天跑一次这个脚本就行。


# pycase
## python写的一些脚本
- demo-mm.py
微信公众号webview测试脚本demo
- checkfile文件夹
对比文章相似度
主要思路：利用jieba获取分词---去的每天文章top1000热度的分词---合并这
两篇文章1000个分词---去重---计算每篇文章top1000在合并后分词中的频率---获得
词频向量---根据词频向量算出相似度
- dinner.py
随机数决定谁去拿饭卡
- kill-5037.py   
windows下kill占用5037端口的进程
- mobile.py   
随机生成手机号和身份证号
- photo.py  
图片相似度对比
- jira_count.py  
统计jira数据
- str_to_json文件夹
用于将fiddler中复制出来的参数，转化为dict
- change文件夹  
部署替换文件相关脚本
- realease文件夹  
统计build相关脚本，并生成报告，格式如下：  
![image](https://github.com/NJ-zero/pycase/raw/master/realease/summary.png)
![image](https://github.com/NJ-zero/pycase/raw/master/realease/detail.png)

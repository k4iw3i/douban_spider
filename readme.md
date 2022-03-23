# 豆瓣电影爬虫
## 简介:
本项目旨在从[豆瓣电影分类页面](https://movie.douban.com/tag/#/)抓取电影列表并进一步抓取详细信息。
### 附加功能：
作为参数附加[火星影视本月上映列表](https://huo720.com/calendar/thismonth/)爬虫并获取豆瓣详情。

## 安装环境:
1. 更新apt
```shell
sudo apt update
```
2. 安装pip
```shell
sudo apt install python3-pip
```
3. 安装环境
```shell
cd [项目根目录]
pip3 install -r requirements.txt
```
## 配置爬虫
配置密码:
[密码文件](src/secrets_config.py)  
配置样例
```python
proxy_key = '1234567'
username = 'test@douban.com'
password = 'password123456'
```

配置爬虫:
[配置文件](src/spider_config.py)
```python
tags = ['电影', '电视剧']
genres = ['全部类型', '剧情','喜剧','动作','爱情','科幻','动画','悬疑','惊悚','恐怖','犯罪','同性','音乐','歌舞','传记','历史','战争','西部','奇幻','冒险','灾难','武侠','情色'] 
sort = ['U', 'R'] #U ->"近期热门", R -> "最新上映"
#前三项可根据需要减项
huoxing_max_page = 10 #爬取火星影视页数,参数为0将不爬取火星影视
douban_max_item_per_search = 100 #每个tag/genre/sort下爬取影视数量,应是20的倍数
concurrent_requests = 16 #同时请求页面书
download_delay = 0 #请求之间空隙秒数
```
最后四项直接影响爬虫运行时长，经测试：默认选项情况下爬虫大概需要40分钟左右完成
如果爬虫过程中出现403等错误代码，应当酌情减少concurrent_requests, 增加download_delay


## 运行爬虫:
```shell
cd [项目根目录]
scrapy crawl douban_spider
```
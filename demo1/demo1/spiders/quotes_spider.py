import scrapy
import json
import re

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    #urls = 'https://www.loldk.com/fm/f/a/adetail-3'
    start_urls = [
        'https://www.loldk.com/fm/f/a/adetail-3.html',
        'https://www.loldk.com/fm/f/a/adetail-6-1.html'
    ]
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://www.evehicle.cn',
        'Referer': 'http://www.evehicle.cn/wp-content/themes/newsite/html/emap.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    for i in range(136):
         start_urls.append('https://www.loldk.com/fm/f/a/adetail-3-'+str(i)+'.html')
    for i in range(125):
        start_urls.append('https://www.loldk.com/fm/f/a/adetail-6-'+str(i)+'.html')

    def parse(self, response):
        links = []
        for link in response.css('div.article-img.fl a::attr(href)').getall():
            next_page = response.urljoin(link)
            filename = r'./log1.txt'
            with open(filename, 'a+',encoding='utf-8') as f:
                f.write(next_page+'\n')
            yield scrapy.Request(next_page, headers=self.headers, callback=self.parse_subpage)

    def parse_subpage(self, response, **kwargs):
        title = response.css('h2.detail-title::text').get()
        date = response.css('p.detail-date::text').get()
        conts = response.css('div.detail-cont').getall()
        url = response.url
        content = ''
        for cont in conts:
            pattern = re.compile(r'\s|\n|<.*?>', re.S)
            # 将匹配到的内容用空替换，即去除匹配的内容，只留下文本
            content = pattern.sub('', cont)
            print(content)
        filename = r'./logs.txt'
        with open(filename, 'a+',encoding='utf-8') as f:
            f.write(json.dumps({'title':title,'date':date,'url':url,'content':content},ensure_ascii=False))
            f.write('\n')
        yield {
            'title':title,
            'url':url,
            'date':date,
            'content':content
        }
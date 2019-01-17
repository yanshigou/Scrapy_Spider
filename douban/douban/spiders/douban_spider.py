# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名
    name = 'douban_spider'
    # 域名
    allowed_domains = ['movie.douban.com']
    # 入口url, 扔到调度器里面去
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        # 解析循环条目
        movie_list = response.xpath('//*[@id="content"]/div/div[1]/ol[@class="grid_view"]/li')

        for i in movie_list:
            douban_item = DoubanItem()
            # 详细xpath 进行数据解析
            douban_item['serial_number'] = i.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            content = i.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            for c in content:
                a = ''.join(c.split())
                douban_item['introduce'] = a
            douban_item['star'] = i.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = i.xpath(".//span[@class='inq']/text()").extract_first()
            douban_item['src'] = i.xpath(".//div[@class='info']/div[@class='hd']/a/@href").extract_first()
            # print(douban_item)
            # yield到piplines中去处理数据
            yield douban_item
        # 解析下一页的路径
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        # print(next_link)
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250"+next_link, callback=self.parse)

# -*- coding: utf-8 -*-
import scrapy
from datetime import timedelta, date
from news.items import ArticleItem
from scrapy.loader import ItemLoader

class TheguardianarticlesspiderSpider(scrapy.Spider):
    name = 'TheguardianArticlesSpider'
    allowed_domains = ['theguardian.com']
    start_urls = []
    start_url = "https://www.theguardian.com/world/{}/{}/{}/all"
    
    def __init__(self, from_date=date.today(), to_date=date.today(), *args, **kwargs):
        super(TheguardianarticlesspiderSpider, self).__init__(*args, **kwargs)
        self.from_date = date.fromisoformat(from_date)
        self.to_date = date.fromisoformat(to_date)
        for n in range(int ((self.to_date - self.from_date).days)):
            dt = self.from_date + timedelta(n)
            self.start_urls.append(self.start_url.format(dt.strftime("%Y"), dt.strftime("%b"), dt.strftime("%d")))
        
    def parse(self, response):
        art_links = response.css('a[href^="https"].u-faux-block-link__overlay::attr(href)').extract()
        for link in art_links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.fetch_article
            )
    
    def fetch_article(self, response):
        #date = response.meta.get('date', '')
        #dt = response.meta.get('date', '')
        #dt = response.css('p.content__dateline time.content__dateline-wpd::attr(datetime)').extract()
        item_loader = ItemLoader(item=ArticleItem(), response=response)
        
        item_loader.add_value('url', response.url)
        item_loader.add_css('headline', 'h1.content__headline::text')
        item_loader.add_css('authors', 'a[rel^="author"] span::text')
        item_loader.add_css('authors', 'div.meta__contact-wrap p.byline::text')
        item_loader.add_css('text', 'div.content__article-body p *::text')
        item_loader.add_css('date', 'p.content__dateline time.content__dateline-wpd::attr(datetime)')

        yield item_loader.load_item()
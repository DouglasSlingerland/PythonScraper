#This is a Groupon site scraper utilizing scrapy to prune relevant business data listed and exported into a CSV sheet
#To use this scraper, open a shell to the directory it's located in and execute
# scrapy runspider scraper.py -s USER_AGENT="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0" -o out.csv
import scrapy
from scrapy.crawler import CrawlerProcess
class BusinessItem(scrapy.Item):
    Name = scrapy.Field()
    Address = scrapy.Field()
    City = scrapy.Field()
    Phone = scrapy.Field()
    Website = scrapy.Field()
    GrouponUrl = scrapy.Field()

class GrouponSpider(scrapy.Spider):
    name = 'grouponspider'
    start_urls = ['#GrouponStartLinkhere',
                

]
    
    def parse(self, response):
        for url in response.css('figure.card-ui > a::attr("href")').extract():
            BusinessIdentifier = url.split('/')[4]
            newUrl = "https://www.groupon.com/deals/merchant_locations_proxy/"+BusinessIdentifier+".json"
            item = BusinessItem()
            
            request = scrapy.Request(url, callback=self.get_website)
            request.meta['item'] = item
            yield request
            request = scrapy.Request(newUrl, callback=self.get_bussinessinfo)
            request.meta['item'] = item
            yield request
            item['GrouponUrl'] = url
            yield item

    def get_bussinessinfo(self, response):      
        for css in response.css('html').extract():
            item = response.meta['item']
            item['Name'] = response.css('span').extract()[1][6:-7]
            item['Address'] = response.css('p').extract()[2][3:-4]
            item['City'] = response.css('p').extract()[3][3:-4]
            item['Phone'] = response.css('p').extract()[-1][3:-4]                         
            return [item]
            
    def get_website(self, response):
        item = response.meta['item']
        item['Website'] = response.css('a.merchant-website::attr("href")').extract()
        return [item]

import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    #allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://baijiahao.baidu.com/s?id=1613535141662246752&wfr=spider&for=pc",
        "https://baijiahao.baidu.com/s?id=1600539020444755658&wfr=spider&for=pc"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
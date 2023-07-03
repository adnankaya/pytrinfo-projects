import scrapy

class OrumcekadamSpider(scrapy.Spider):
    name = 'OrumcekAdam'
    allowed_domains = ['toscrape.com']
    # 'random' sub_domainini yerleştirdik
    # start_urls = ['http://quotes.toscrape.com/random'] 
    start_urls = ['http://quotes.toscrape.com'] 

    def parse(self, response):
        for quote in response.css('div.quote'):
            m_dict = {
                'author_name' : quote.css('small.author::text').extract_first(),
                'text' : quote.css('span.text::text').extract_first(),
                'tags' : quote.css('a.tag::text').extract(), # tag'ler çok olabilir.
            }
            yield m_dict
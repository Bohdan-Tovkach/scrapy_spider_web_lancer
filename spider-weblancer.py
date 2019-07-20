import scrapy # our scrapy library
import re # regular expression 

# to retrieve data in .json or .csv scrapy crawl my_spider -o [filename].[extension] 
class QuotesSpider(scrapy.Spider):

    name = "weblancer"
    start_urls = [
        'https://www.weblancer.net/jobs/',
    ]

    def parse(self, response):
        # use xpath to get data from div=row 
        my_query = response.xpath("//div[@class='cols_table']/div[@class='row']")
        for my_dict in my_query:
            yield {
                'title': my_dict.xpath("div[@class='col-sm-10']/h2[@class='title']\
                    /a/text()").extract(),

                'category': my_dict.xpath("div[@class='col-sm-8 text-muted dot_divided']\
                    /span/a[@class='text-muted']/text()").extract(),

                'price': my_dict.xpath("div[@class='col-sm-2 text-sm-right']\
                    /div[@class='float-right float-sm-none title amount indent-xs-b0']/text()").extract(),

                # use regular expression to get all data (order) in sequence \d\w (digital+/word+) 
                'order': re.findall(r"\d+.\w+", str(my_dict.xpath("div[@class='col-sm-2 text-sm-right']\
                    /div[@class='float-left float-sm-none text_field']/text()").extract())), 
            }   
            # use slice that our spider go to proper sequence (1,2,3..., x)
            next_page = response.xpath("//div[@class='col text-center']/a/@href")[-2] 
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

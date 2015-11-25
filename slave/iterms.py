from scrapy.item import Item, Field

class CrawlerIterm(Item):
    title = Field()
    content = Field()
    link = Field()
    desc = Field()
    original_url = Field()
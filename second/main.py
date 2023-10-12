import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuoteItem(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorsQuotesPipeline:
    authors = []
    quotes = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            self.authors.append(
                {
                    "fullname": adapter["fullname"],
                    "born_date": adapter["born_date"],
                    "born_location": adapter["born_location"],
                    "description": adapter["description"],
                }
            )
        if "quote" in adapter.keys():
            self.quotes.append(
                {
                    "tags": adapter["tags"],
                    "author": adapter["author"],
                    "quote": adapter["quote"],
                }
            )

    def close_spider(self, spider):
        with open("second/json/authors.json", "w", encoding="utf-8") as fh:
            json.dump(self.authors, fh, ensure_ascii=False, indent=4)

        with open("second/json/quotes.json", "w", encoding="utf-8") as fh:
            json.dump(self.quotes, fh, ensure_ascii=False, indent=4)


class AuthorsQuotesSpider(scrapy.Spider):
    name = "authors_and_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES": {AuthorsQuotesPipeline: 300}}

    def parse(self, response, *args):
        for block in response.xpath("//div[@class='quote']"):
            tags_raw = block.xpath("div[@class='tags']/a/text()").extract()
            tags = []
            for tag in tags_raw:
                tags.append(tag.strip())
            author = block.xpath("span/small/text()").get().strip()
            quote = block.xpath("span[@class='text']/text()").get().strip()
            yield QuoteItem(tags=tags, author=author, quote=quote)
            yield response.follow(
                url=self.start_urls[0] + block.xpath("span/a/@href").get(),
                callback=self.nested_parse_author,
            )
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def nested_parse_author(self, response, *args):
        author = response.xpath("//div[@class='author-details']")
        fullname = author.xpath("h3[@class='author-title']/text()").get().strip()
        born_date = (
            author.xpath("p/span[@class='author-born-date']/text()").get().strip()
        )
        born_location = (
            author.xpath("p/span[@class='author-born-location']/text()").get().strip()
        )
        description = (
            author.xpath("div[@class='author-description']/text()").get().strip()
        )
        yield AuthorItem(
            fullname=fullname,
            born_date=born_date,
            born_location=born_location,
            description=description,
        )


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(AuthorsQuotesSpider)
    process.start()
    print("Done")

import scrapy

from scrapy.loader import ItemLoader

from ..items import ApobankdeItem
from itemloaders.processors import TakeFirst


class ApobankdeSpider(scrapy.Spider):
	name = 'apobankde'
	start_urls = ['https://newsroom.apobank.de/tags?page=1&namespace=pressreleases']

	def parse(self, response):
		tag_links = response.xpath('//a/@href').getall()
		yield from response.follow_all(tag_links, self.parse_tags)

	def parse_tags(self, response):
		post_links = response.xpath('//a[@title]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="panel__text"]//text()[normalize-space() and not(ancestor::a)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="type__date"]//time/text()').get()

		item = ItemLoader(item=ApobankdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

import scrapy
from ..items import ConfspiderItem

class ConferencespiderSpider(scrapy.Spider):
	name = 'conferenceSpider'
	page = 2
	start_urls = ['https://www.worldconferencealerts.com/Interdisciplinary-Conference.php']
	def parse(self, response):
		items = ConfspiderItem()
		divisions = response.css('.table')
		for div in divisions:
			name = div.css('.conflist span:nth-child(1)::text').extract()
			location = div.css('span.div_venue::text').extract()
			organizer = div.css('.organized-by a:nth-child(1)::text').extract()
			topic = div.css('strong+ a::text').extract()
			date = div.css('div.date-as-calendar').xpath('@content').extract()
			conflink = div.css('a.conflist').xpath('@href').extract()

			items['name'] = name
			items['location'] = location
			items['organizer'] = organizer
			items['topicCovered'] = topic
			items['date'] = date
			items['conflink'] = conflink
			yield items

		next_page = "https://www.worldconferencealerts.com/Interdisciplinary-Conference.php?page="+str(ConferencespiderSpider.page)
		if(ConferencespiderSpider.page <= 10):
			ConferencespiderSpider.page+=1
			yield response.follow(next_page, callback = self.parse)
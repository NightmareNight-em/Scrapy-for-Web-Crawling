# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

#Download MySQl from https://dev.mysql.com/downloads/installer/
#Now install mysql using 'pip install mysql'
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class ConfspiderPipeline:
	def __init__(self):
		self.createConnection()
		self.createTable()

	def createConnection(self):
		self.conn = mysql.connector.connect(
					host = 'localhost',
					user = 'root',
					passwd = 'MySQL@123',
					database = 'conferencedata'			
												)
		self.curr = self.conn.cursor()


	def createTable(self):
		self.curr.execute("""DROP TABLE IF EXISTS conf""")
		self.curr.execute("""CREATE TABLE conf(
						name text,
						location text,
						date text,
						organizer text,
						topicsCovered text,
						conflink text)""")

	def process_item(self, item, spider):
		self.add_values(item)
		return item
	
	def add_values(self,item):

		self.curr.execute("""INSERT INTO conf VALUES(%s,%s,%s,%s,%s,%s)""", (item['name'][0], item['location'][0].strip(', \n'), item['date'][0], item['organizer'][0], item['topicCovered'][0].strip(', \n'), item['conflink'][0]))
		self.conn.commit()
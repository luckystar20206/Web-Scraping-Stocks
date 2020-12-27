import scrapy
from scrapy.mail import MailSender
from scrapy.crawler import CrawlerProcess
import smtplib
from email.message import EmailMessage

class StocksSpider(scrapy.Spider):
    name = 'stocks'
    allowed_domains = ['https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_29-us-nyse-stocks--qc_1-alphabetical-order']
    start_urls = ['https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_29-us-nyse-stocks--qc_1-alphabetical-order/']

    def parse(self, response):
        #Extracting the content using css selectors
        instrument = response.css('a.tooltip-img::text').extract()
        ticker = response.css('span.delayquoteval::text').extract()
        
        #Give the extracted content row wise
        for item in zip(instrument, ticker):
            #create a dictionary to store the scraped info
            scraped_info = {
                'instrument' : item[0],
                'ticker' : item[1],
            }
            #yield or give the scraped info to scrapy
            yield scraped_info
            
# Sending email
def email():
    message = EmailMessage()
    message['From'] = 'abc@gmail.com'
    message['To'] = 'xyz@gmail.com'
    message['Subject'] = "Your Stocks Daily Digest"
    message.set_content("Body")
    with open('stocks.csv','r') as f:
        content = f.read()
    message.add_attachment(content, filename = "stocks.csv")

    # Connecting to the GMAIL server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.ehlo()
    server.login('abc@gmail.com', '*******')
    server.send_message(message)
    server.quit()
    print('Email sent successfully')
    
pro = CrawlerProcess()
pro.crawl(StocksSpider)
pro.start()
email()
# -*- coding: utf-8 -*-
import scrapy
from datetime import date,timedelta
#from scrapy.utils.response import open_in_browser

def first(sel, xpath):
    return sel.xpath(xpath).extract_first()


class OnsSpider(scrapy.Spider):
    name = 'onsEPECargaAnuario.'
    start_urls = ['http://www.epe.gov.br/AnuarioEstatisticodeEnergiaEletrica/Anu%C3%A1rio%20Estat%C3%ADstico%20de%20Energia%20El%C3%A9trica%202016.xls']
   
    def parse(self, response):

        self.logger.warning("parse:"+response.url)

        path ='AnuarioEPE.xls'
        self.logger.info('Saving xls %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
       
       
       

  
       
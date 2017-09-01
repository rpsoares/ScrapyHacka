# -*- coding: utf-8 -*-
import scrapy
from datetime import date,timedelta
#from scrapy.utils.response import open_in_browser

def first(sel, xpath):
    return sel.xpath(xpath).extract_first()


class OnsSpider(scrapy.Spider):
    name = 'onsEPECarga'
    start_urls = ['http://www.epe.gov.br/mercado/Documents/Box%20Mercado%20de%20Energia/Consumo%20Mensal%20de%20Energia%20El%C3%A9trica%20por%20Classe%20(regi%C3%B5es%20e%20subsistemas)%20%E2%80%93%202004-2017.xls']
   
    def parse(self, response):

        self.logger.warning("parse:"+response.url)

        path = 'EPECarga.xls'
        self.logger.info('Saving xls %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
       
       
       

  
       
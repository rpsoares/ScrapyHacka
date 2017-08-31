# -*- coding: utf-8 -*-
import scrapy
from datetime import date,timedelta
#from scrapy.utils.response import open_in_browser

def first(sel, xpath):
    return sel.xpath(xpath).extract_first()


class OnsSpider(scrapy.Spider):
    name = 'onsCargaModelo2017'
    start_urls = ['http://sdro.ons.org.br/SDRO/DIARIO/2017_02_01/HTML/12_CargaHorariaSub_01-02-2017.xlsx']
    refDate = date(2017,2, 1)
    def parse(self, response):

        self.logger.warning("parse:"+response.url)

        path = response.url.split('/')[-1]
        self.logger.info('Saving xls %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)
       
       
        if (self.refDate <=date.today()):
            self.refDate=self.refDate+timedelta(1)
            mes = str(self.refDate.month)
            if(self.refDate.month<10):
                mes='0'+mes
            dia = str(self.refDate.day)
            if(self.refDate.day<10):
                dia='0'+dia
            
            if(self.refDate<date(2017, 5, 16)):
                 item='12'
            else:
                 item='13'  
            url='http://sdro.ons.org.br/SDRO/DIARIO/{0}_{1}_{2}/HTML/{3}_CargaHorariaSub_{4}-{5}-{6}.xlsx'.format(self.refDate.year,mes,dia,item,dia,mes,self.refDate.year)
            yield scrapy.Request(url=url, callback=self.parse)

  
       
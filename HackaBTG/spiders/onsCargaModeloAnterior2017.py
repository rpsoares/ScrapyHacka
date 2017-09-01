# -*- coding: utf-8 -*-
import scrapy
from datetime import date,timedelta
#from scrapy.utils.response import open_in_browser

def first(sel, xpath):
    return sel.xpath(xpath).extract_first()


class OnsSpider(scrapy.Spider):
    name = 'onsCargaModeloAnterior2017'
    start_urls = ['http://sdro.ons.org.br/boletim_diario/2005_08_03/carga_arquivos/sheet001.htm']
    refDate = date(2005,8, 3)
    jumpDates =[date(2008,4,11),date(2011,7,10),date(2017,1,30)]
    submercados =['SE/CO','Itaipu','S','NE','N','SIN']
    def parse(self, response):

        self.logger.warning("parse:"+response.url)
        startGet = False
        countLoop=0
        dados=[]

        for sel in response.xpath('//td'):
             textResponse = sel.xpath('text()').extract_first() 
            
             if(textResponse in self.submercados):
                 print (textResponse)
                 startGet=True
             if(startGet):
                 countLoop+=1
                 if(countLoop<=4):
                     dados.append(textResponse)
                 else:
                    startGet=False
                    countLoop=0
                    yield {
                        'data':self.refDate,
                        'submercado': dados[0],
                        'GWhDia': dados[1],
                        'GWhAcMes': dados[2],
                        'GWhAcAno':dados[3],
                        'MWhDia': None,
                        'MWhAcMes': None,
                         'MWhAcAno': None,
                    }
                    dados=[]




       
       
        if(self.refDate<=date(2017, 1, 31)):
             self.refDate=self.refDate+timedelta(1)

             while (self.refDate in self.jumpDates):
                 self.refDate=self.refDate+timedelta(1)


             mes = str(self.refDate.month)
             if(self.refDate.month<10):
                 mes='0'+mes
             dia = str(self.refDate.day)
             if(self.refDate.day<10):
                 dia='0'+dia
            
             url='http://sdro.ons.org.br/boletim_diario/{0}_{1}_{2}/carga_arquivos/sheet001.htm'.format(self.refDate.year,mes,dia)
             yield scrapy.Request(url=url, callback=self.parse)

  
       
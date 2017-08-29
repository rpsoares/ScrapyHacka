# -*- coding: utf-8 -*-
import scrapy
from datetime import date,timedelta
#from scrapy.utils.response import open_in_browser

def first(sel, xpath):
    return sel.xpath(xpath).extract_first()


class OnsSpider(scrapy.Spider):
    name = 'onsProducaoTermicaModeloAnterior2017'
    start_urls = ['http://sdro.ons.org.br/boletim_diario/2005_08_03/geracao_arquivos/sheet002.htm']
    refDate = date(2005,8, 3)
    submercados =['SE/CO','Itaipu','S','NE','N','SIN']
    def parse(self, response):

        self.logger.warning("parse:"+response.url)
        startGet = False
        countLoop=0
        dados=[]

        for sel in response.xpath('//td'):
            textResponse = sel.xpath('text()').extract_first() 
            if(textResponse in submercados):
                startGet=True
            if(startGet):
                countLoop+=1
                if(countLoop<=4):
                    dados.append(textResponse)
                else:
                    startGet=False
                    countLoop=0



        yield {
                'tipo': "Termica",
                'data':self.refDate,
                'submercado': dados[0]
                'GWhDia': dados[1],
                'GWhAcMes': dados[2],
                'GWhAcAno':dados[3],
                'MWhDia': None,
                'MWhAcMes': None,
                'MWhAcAno': None,
        }
       
       
       if(self.refDate<=date(2017, 1, 31)):
            self.refDate=self.refDate+timedelta(1)
            mes = str(self.refDate.month)
            if(self.refDate.month<10):
                mes='0'+mes
            dia = str(self.refDate.day)
            if(self.refDate.day<10):
                dia='0'+dia
            
            url='http://sdro.ons.org.br/boletim_diario/{0}_{1}_{2}/HTML/geracao_arquivos/sheet002.htm'.format(self.refDate.year,mes,dia,item)
            yield scrapy.Request(url=url, callback=self.parse)

  
       
# -*- coding: utf-8 -*-
import scrapy
from datetime import date,timedelta
#from scrapy.utils.response import open_in_browser

def first(sel, xpath):
    return sel.xpath(xpath).extract_first()


class OnsSpider(scrapy.Spider):
    name = 'onsProducaoHidraulica'
    start_urls = ['http://www.ons.org.br/resultados_operacao/SDRO/Diario/2017_02_01/HTML/07_ProducaoHidraulicaUsina.html']
    refDate = date(2017,2, 1)
    def parse(self, response):

        self.logger.warning("parse:"+response.url)

        for num in range(2,7):
           yield {
                'tipo': "Hidraulica",
                'data':self.refDate,
                'submercado': first(response, '//span[@id="grdSubmercados_ctl0{0}_lblsme_id"]/text()'.format(num)),
                'GWhDia': first(response, '//span[@id="grdSubmercados_ctl0{0}_lblAcumDiario"]/text()'.format(num)),
                'GWhAcMes': first(response, '//span[@id="grdSubmercados_ctl0{0}_lblAcumMensal"]/text()'.format(num)),
                'GWhAcAno': first(response, '//span[@id="grdSubmercados_ctl0{0}_lblAcumAnual"]/text()'.format(num)),
                'MWhDia': first(response, '//span[@id="grdSubmercadosMWmed_ctl0{0}_lblAcumDiario"]/text()'.format(num)),
                'MWhAcMes': first(response, '//span[@id="grdSubmercadosMWmed_ctl0{0}_lblAcumMensal"]/text()'.format(num)),
                'MWhAcAno': first(response, '//span[@id="grdSubmercadosMWmed_ctl0{0}_lblAcumAnual"]/text()'.format(num)),
            }
       
       
        if (self.refDate <date.today()):
            self.refDate=self.refDate+timedelta(1)
            mes = str(self.refDate.month)
            if(self.refDate.month<10):
                mes='0'+mes
            dia = str(self.refDate.day)
            if(self.refDate.day<10):
                dia='0'+dia
            
            if(self.refDate<date(2017, 5, 16)):
                 item='07'
            else:
                 item='08'  
            url='http://www.ons.org.br/resultados_operacao/SDRO/Diario/{0}_{1}_{2}/HTML/{3}_ProducaoHidraulicaUsina.html'.format(self.refDate.year,mes,dia,item)
            yield scrapy.Request(url=url, callback=self.parse)

  
       
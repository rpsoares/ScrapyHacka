# -*- coding: utf-8 -*-
import scrapy
from datetime import date,timedelta
#from scrapy.utils.response import open_in_browser
import pandas as pd
import csv




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

        dt=pd.read_excel(path, 'Plan1',skiprows=6,index_col=None, na_values=['NA']) 
        dt.rename(columns=lambda x: x.replace('\n', ''), inplace=True) 

        mwSECO= dt['VerificadoMWh/h'].sum()
        gwSECO= mwSECO/ 1000

        self.logger.warning("parsegwSECO:")
        self.logger.warning(str(gwSECO))
        self.logger.warning("parsemwSECO:")
        self.logger.warning(str(mwSECO))
        yield {
               
                'data':self.refDate,
                'submercado': "SE/CO",
                'GWhDia' : gwSECO,
                'GWhAcMes': 0,
                'GWhAcAno': 0,
                'MWhDia': mwSECO,
                'MWhAcMes': 0,
                'MWhAcAno': 0,
            
        }
        mwS= dt['VerificadoMWh/h.1'].sum() 
        yield {
               
                 'data':self.refDate,
                 'submercado': "S",
                 'GWhDia':mwS / 1000,
                 'GWhAcMes': 0,
                 'GWhAcAno': 0,
                 'MWhDia':mwS,
                 'MWhAcMes': 0,
                 'MWhAcAno': 0,
            
        }
        mwNE= dt['VerificadoMWh/h.2'].sum() 
        yield {
              
                 'data':self.refDate,
                 'submercado': "NE",
                 'GWhDia':mwNE / 1000,
                 'GWhAcMes': 0,
                 'GWhAcAno': 0,
                 'MWhDia': mwNE,
                 'MWhAcMes': 0,
                 'MWhAcAno': 0,
            
        }
        mwN= dt['VerificadoMWh/h.3'].sum()
        yield {
               
                'data':self.refDate,
                'submercado': "N",
                'GWhDia':mwN / 1000,
                'GWhAcMes': 0,
                'GWhAcAno': 0,
                'MWhDia': mwN,
                'MWhAcMes': 0,
                'MWhAcAno': 0,
            
        }

        
       
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

  
       
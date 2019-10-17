# -*- coding: utf-8 -*-
import scrapy
import re

class SimarRoturasSpider(scrapy.Spider):
    name = 'simar_roturas'
    allowed_domains = ['simar-louresodivelas.pt']
    start_urls = ['http://www.simar-louresodivelas.pt/']

    def parse(self, response):
        print("procesing:" + response.url)
        roturas = response.xpath("//*[@id=\"ListView1_itemPlaceholderContainer\"]/span/text()").extract()

        #validate if there are no "roturas" before parsing anything
        if "Sem roturas" in str(roturas):
            return
        #remove and trim html
        trimmed_roturas = [re.sub(r'\n\s*\n', '\n\n', item).strip() for item in roturas]
        #remove empty strings
        trimmed_roturas_2 = list(filter(bool,trimmed_roturas))
        data_struct = {}
        data_struct['roturas']=[]
        #create data structure for each current event
        for item in trimmed_roturas_2:
            freguesia = item.split("freguesia de ")[1].split(" no local ")[0]
            local = item.split(" no local ")[1].split(" no dia ")[0]
            dia = item.split(" no dia ")[1].split(",")[0]
            hora = item.split(" com previsão de conclusão às ")[1].split(".")[0].strip()
            data_struct['roturas'].append({
                # key:value
                'freguesia': freguesia,
                'local': local,
                'dia': dia,
                'hora': hora,
            })

        yield data_struct

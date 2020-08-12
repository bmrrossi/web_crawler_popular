import scrapy
import json
import os

from html2json import collect

from scrapy.exceptions import CloseSpider
from web_crawler_popular.spiders.environment import popular 

EXTRACTED_HTML_FILE = 'extracted.txt'
JSON_FINAL_FILE = 'jsoned.txt'
LOG_FILE = 'log.txt'

class PopularSpider(scrapy.Spider):
    name = 'popularspider'
    start_urls = [popular['site_login']]
    
    data_inicial = ''
    data_final = ''
    
    def __init__(self, data_inicial="01/08/2020", data_final="04/08/2020", *a, **kw):
        self.write_log_in_file("Hello my friend! We will change the world!")
        self.erase_files()
        self.data_inicial = data_inicial
        self.data_final = data_final
        super().__init__(**kw)
        
    custom_settings = {'FEED_URI': 'outputfile.json', 'CLOSESPIDER_TIMEOUT' : 15}
        
    def erase_files(self):        
        if os.path.exists(EXTRACTED_HTML_FILE):
            self.write_log_in_file("Removing {} file".format(EXTRACTED_HTML_FILE))
            os.remove(EXTRACTED_HTML_FILE)
        
        if os.path.exists(JSON_FINAL_FILE):
            self.write_log_in_file("Removing {} file".format(JSON_FINAL_FILE))
            os.remove(JSON_FINAL_FILE)
        
        if os.path.exists(LOG_FILE):
            self.write_log_in_file("Removing {} file".format(LOG_FILE))      
            os.remove(LOG_FILE)
    
    def parse(self, response):
        self.write_log_in_file("Estamos na página de login: {}".format(response.url))
    
        yield scrapy.FormRequest(
            url=popular['site_login'],
            formdata={
                'formLogin': "formLogin",
                'formLogin:no_login': popular['user'],
                'formLogin:senha': popular['password'],
                'formLogin:j_idt25': "Acessar",
                'javax.faces.ViewState': response.xpath('//input[@name="javax.faces.ViewState"]/@value').extract_first()
            },
            callback=self.parse_crawler_page,
        )
        
    def parse_crawler_page(self, response):
        self.write_log_in_file("Estamos na página de consolidação: {}".format(response.url))
        
        has_logout_link = response.xpath('//a[@title="sair"]').extract_first()
        if not has_logout_link:
            raise CloseSpider('falha de autenticação')
        
        yield scrapy.FormRequest(
            url=popular['site_crawler'],
            formdata={
                'form': 'form',
                'form:dataInicio_input': self.data_inicial,
                'form:dataFim_input': self.data_final,
                'form:tabela_pagination': "true",
                'form:tabela_first': '0',
                'form:tabela_rows': '10',
                'form:j_idt86': "Consultar",
                'javax.faces.ViewState': response.xpath('//input[@name="javax.faces.ViewState"]/@value').extract_first()
            },
            callback=self.handle_page,
        )
        
    def handle_page(self, response):
        self.write_log_in_file("Gerenciando o número de páginas e fazendo o loop...")    
        
        text_with_pages = response.xpath('//span[@class="ui-paginator-current"]').extract_first()
        
        number_pages = self.discovery_number_of_pages(text_with_pages)
        self.write_log_in_file("Pages to iterate: {}".format(number_pages))
        
        first = 0
        iterator = 1
        while(iterator <= int(number_pages)):
            self.log("Iterator number {}".format(iterator))
            yield scrapy.FormRequest(
                url=popular['site_crawler'],
                formdata={
                    'form': 'form',
                    'form:dataInicio_input': self.data_inicial,
                    'form:dataFim_input': self.data_final,
                    'form:tabela_pagination': "true",
                    'form:tabela_first': str(first),
                    'form:tabela_rows': '10',
                    'form:j_idt86': "Consultar",
                    'javax.faces.ViewState': response.xpath('//input[@name="javax.faces.ViewState"]/@value').extract_first()
                },
                callback=self.handle_data,
            )
            
            first = first + 10
            iterator = iterator + 1
        
        
    def handle_data(self, response):
        
        
        self.write_log_in_file("Formatando o JSON...")
        ContentUrl = json.dumps({
            'page_content': str(response.css('tr').extract())
        })
        
        self.write_log_in_file("Escrevendo o JSON final...")
        f = open(JSON_FINAL_FILE, "a+")
        f.write(str(ContentUrl))
        f.close()
        
    def write_log_in_file(self, log):
        f = open(LOG_FILE, "a+")
        f.write(str(log))
        f.close()
        
    def discovery_number_of_pages(self, text_with_pages):
        text_final = 1
        if text_with_pages:
            broker_parentesis = text_with_pages.split("(")
        if broker_parentesis:    
            broker_space = broker_parentesis[1].split(" ")
        if broker_space:
            text_final = broker_space[2].replace(")</span>", "")
            
        return text_final
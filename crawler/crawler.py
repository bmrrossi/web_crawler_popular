import scrapy
from scrapy.exceptions import CloseSpider
from environment import popular 

class PopularSpider(scrapy.Spider):
    name = 'login-popular'
    start_urls = [popular['site_login']]
    
    def __init__(self, *a, **kw):
        print("Olá que tal!")
        print(popular['site_login'])
        print(popular['user'])
        print(popular['password'])
    
    def parse(self, response):
        self.log("Estamos na página de login: {}".format(response.url))
    
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
        has_logout_link = response.xpath('//a[@title="sair"]').extract_first()
        if not has_logout_link:
            raise CloseSpider('falha de autenticação')
        self.log('acabei de fazer login')
        self.log(str(response.xpath('//input[@name="javax.faces.ViewState"]/@value').extract_first()))
        
        yield scrapy.FormRequest(
            url=popular['site_crawler'],
            formdata={
                'form': 'form',
                'form:dataInicio_input': "01/08/2020",
                'form:dataFim_input': "04/08/2020",
                'form:j_idt86': "Consultar",
                'javax.faces.ViewState': response.xpath('//input[@name="javax.faces.ViewState"]/@value').extract_first()
            },
            callback=self.handle_data,
        )
        
    def handle_data(self, response):
        self.log("Cheguei no Handle")    

        f = open("results.txt", "a")        
        f.write(str(response.css('table').extract()))
        f.close()
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pokemon.items import PokemonItem


class PokspiderSpider(scrapy.Spider):
    name = "pokspider"
    allowed_domains = ["scrapeme.live"]
    start_urls = ["https://scrapeme.live/shop/"]

    rules = (
        Rule(LinkExtractor(allow=(r'page/\d+','shop/')), callback='parse_pok', follow=True)
        )
    
    custom_settings = {
        'FEEDS': {
            'pokemondata.sql':{'format': 'sql', 'overwrite': True},
        }
    }


    def start_requests(self):
        URL = 'https://scrapeme.live/shop/'
        yield scrapy.Request(url=URL, callback=self.parse_general)

    
    def parse_general(self,response):
        
        for pokemon in response.css('div.content-area ul.products li.product a.woocommerce-LoopProduct-link::attr(href)').extract():
            pokemon_url = pokemon #.css('a::attr(href)').get()
            yield response.follow(pokemon_url, self.parse_pok)
            #yield scrapy.Request(url=result, callback = self.parse_pok)   
        next_page = response.css('.page-numbers a.next::attr(href)').get()
        
        if next_page:
            yield response.follow(url=next_page, callback=self.parse_general)


    def parse_pok(self, response):

        pokemon_item = PokemonItem()

        #pokemon_item['url']= response.url,
        pokemon_item["name"]= response.css('div.summary h1.product_title::text').extract_first()
        pokemon_item["price"]=response.css('div div.summary p span.amount::text').extract_first()
        pokemon_item["description"]= response.css('div div.summary div.woocommerce-product-details__short-description p::text').extract()            
        pokemon_item["stock"]= response.css('div div.summary p.stock::text').extract_first()
        pokemon_item["sku"]= response.css('div div.summary div.product_meta span span.sku::text').extract_first()
        pokemon_item["categories"]= response.css('div div.summary div.product_meta span.posted_in a::text').extract()
        pokemon_item["tags"]= response.css('div div.summary div.product_meta span.tagged_as a::text').extract()
        pokemon_item["weight"]= response.css(' div.woocommerce-Tabs-panel table.shop_attributes tr td.product_weight::text').extract_first()
        pokemon_item["dimensions"]= response.css(' div.woocommerce-Tabs-panel table.shop_attributes tr td.product_dimensions::text').extract_first()
        
        yield pokemon_item
        
        
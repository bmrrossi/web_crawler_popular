import crochet
crochet.setup()
import time
import os

from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask import jsonify
from flask import request 

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

from web_crawler_popular.spiders.crawler import PopularSpider
from web_crawler_popular.environment import popular

app = Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner()

@app.route('/')
def home():
    text = "Estoy aqui..."
    return jsonify(text)

@app.route('/filter', methods=['POST']      )
def filter():
    if request.method == "POST":
        if os.path.exists("outputfile.json"): 
            os.remove("outputfile.json")
        
        global data_inicial 
        data_inicial = request.get_json()['data_inicial']
        
        global data_final 
        data_final = request.get_json()['data_final']
        
        return redirect(url_for('scrape'))
    
@app.route("/scrape")
def scrape():
    scrape_with_crochet() 
    
    time.sleep(20) 
    
    return jsonify(output_data)

@crochet.run_in_reactor
def scrape_with_crochet():

    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    
    eventual = crawl_runner.crawl(PopularSpider, data_inicial=data_inicial, data_final=data_final)
    return eventual

def _crawler_result(item, response, spider):
    print("Called me!")
    print(item)
    print(response)
    print(spider)
    output_data.append(dict(item))
    
if __name__ == '__main__':
    app.run(debug=True)
import crochet
import time

from flask import Flask
from flask import jsonify
from flask import request 

from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

from crawler.crawler import PopularSpider

app = Flask(__name__)

output_data = []
crawl_runner = CrawlerRunner()

crochet.setup()

@app.route('/')
def home():
    text = "Estoy aqui..."
    return jsonify(text)

@app.route('/filter')
def filter():
    data_inicial = request.args.get('data_inicial')
    data_final = request.args.get('data_final')
    print(data_inicial)
    print(data_final)
    #return redirect(url_for('scrape'))
    
@app.route("/scrape")
def scrape():
    crape_with_crochet() # Passing that URL to our Scraping Function

    time.sleep(20) # Pause the function while the scrapy spider is running
    
    return jsonify(output_data)

@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    
    eventual = crawl_runner.crawl(PopularSpider)
    return eventual

def _crawler_result(item, response, spider):
    output_data.append(dict(item))
    
if __name__ == '__main__':
    app.run(debug=True)
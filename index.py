import json
from sanic import Sanic
from sanic.response import json as json_response
from serpapi import GoogleSearch

from cors import add_cors_headers
from options import setup_options

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

config = json.load(open('config.json'))

app = Sanic(name=__name__)

@app.get('/')
async def root(request):
    return json_response({'message': 'Hello, world!'})

@app.route('/api/walmart')
async def walmart(request):
    try:
        params = {
        "api_key": config['api_key'],
        "engine": "walmart",
        "query": request.args['search']
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()

        # parsed = [[i["title"], i["primary_offer"], i["thumbnail"]] for i in results["organic_results"]]
        parsed = results["organic_results"]

        return json_response({
            'status': 'ok',
            'request':request.args,
            'results':parsed
        })
    except Exception as e:
        return json_response({
            'status': 'error',
            'request':request.args,
            'error':str(e)
        })
        

@app.route('/api/superstore')
async def safeway(request):
    # PSEUDO CODE
    # superstore selenium search(request.args['search'])
    # superstore selenium should return a list of objects including price, price per unit, name and image
    # send as a parsed list to the client

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    search = request.args['search'][0]
    driver.get("https://www.realcanadiansuperstore.ca/search?search-bar=" + search+"&sort=price-asc")
    c = 0 # counter
    while True:
        c+=1
        if c > 100:
            return json_response({
                'status': 'ok',
                'request':request.args,
                'results':[{"name":"None found","price":"$420.69/ea","img":"https://cdn.vox-cdn.com/thumbor/9j-s_MPUfWM4bWdZfPqxBxGkvlw=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/22312759/rickroll_4k.jpg","link":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}]
            })
        try:
            driver.find_element(by=By.TAG_NAME, value="li")
            for i in range(10):
                driver.execute_script(f"window.scrollTo(0, {i}*document.body.scrollHeight/10);") #scroll to the bottom, but interpolated
                time.sleep(0.05)
            items = driver.find_elements(by=By.TAG_NAME, value="li")
            parsed = []
            for i in items:
                if i.text.strip() != "":
                    try:
                        img=i.find_element(by=By.TAG_NAME, value="img").get_attribute("src")
                        link = i.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
                        text=i.text.split('\n')
                        if len(text) > 1:
                            parsed.append({"name":text[0], "price":text[1], "img":img, "link":link})                        
                    except:
                        pass
            if len(parsed) > 0:
                return json_response({
                    'status': 'ok',
                    'request':request.args,
                    'results':parsed # no nead for stringify because json_response automatically does that for us
                })
            else:
                return json_response({
                    'status': 'ok',
                    'request':request.args,
                    'results':[{"name":"None found","price":"$420.69/ea","img":"https://cdn.vox-cdn.com/thumbor/9j-s_MPUfWM4bWdZfPqxBxGkvlw=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/22312759/rickroll_4k.jpg","link":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}]
                })
            break
        except:
            try:
                driver.find_element(by=By.CLASS_NAME,value="search-no-results search-no-results--dym")
                return json_response({
                    'status': 'ok',
                    'request':request.args,
                    'results':[{"name":"None found","price":"$420.69/ea","img":"https://cdn.vox-cdn.com/thumbor/9j-s_MPUfWM4bWdZfPqxBxGkvlw=/1400x1050/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/22312759/rickroll_4k.jpg","link":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}]
                })
            except:
                pass  
        time.sleep(0.1)      
    driver.quit()

app.register_listener(setup_options, "before_server_start")

app.register_middleware(add_cors_headers, "response")

app.run(host='0.0.0.0', workers=4, port=6969, dev=True)
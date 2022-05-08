from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

search = "atartbartbatrb"
search= search.replace(" ","+")
driver.get("https://www.realcanadiansuperstore.ca/search?search-bar=" + search)
# wait until page is fully loaded
c = 0 # counter
while True:
    time.sleep(0.1)
    try:
        driver.find_element(by=By.TAG_NAME, value="li")
        # time.sleep(2) #alternative solution: choose an element that is loaded in at the same time, then wait for it to be loaded
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
                except Exception as e:
                    pass
        if len(parsed) > 0:
            print(json.dumps(parsed))
        else:
            print("No items found")
        break
    except:
        try:
            driver.find_element(by=By.CLASS_NAME,value="search-no-results search-no-results--dym")
            print("No results found")
            break
        except:
            pass
    c+=1
    if c > 100:
        break
    
driver.quit()
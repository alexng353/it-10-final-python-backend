from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)


search = "grapes"
# search https://www.walmart.ca/search?q={search}
search= search.replace(" ","+")
driver.get("https://www.walmart.ca/search?q=" + search)
# wait until page is fully loaded
# inside a <div> with data-automation="product":
# look in data-automation="name" for the name of the item
# look in data-automation="current-price" for the price of the item
# look in data-automation="image" for the image of the item
# look for an <a> tag with class="css-15x41f3 epettpn1" for the link to the item 

c = 0 # counter
while True:
    time.sleep(0.1)
    try:
        items = driver.find_element(by=By.XPATH, value="//div[@data-automation='product']")
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
            # <h1> data-automation="null-results-message"
            driver.find_element(by=By.XPYATH, value="//h1[@data-automation='null-results-message']" )
            print("No results found")
            break
        except:
            print("page not loaded")
            pass

    c+=1
    if c > 100:
        break

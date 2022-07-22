# Login to myLDR.com, take screenshots of RadFacts, save images, and PDFs of all Accounts in access
# Run this report 45 days after the close of the quarter: 2/15 for Q4, 5/15 for Q1, 8/15 for Q2, 11/15 for Q3
# Edit the main() function to tailor the report
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image
import time
import requests
from dotenv import load_dotenv
import os
from Screenshot import Screenshot_Clipping
ss = Screenshot_Clipping.Screenshot()

load_dotenv()

# website = "https://twitter.com/NuclearGeeketh/status/1547685440592834569"

api_key = os.environ["api_key"]
api_secret = os.environ["api_secret"]
api_token = os.environ["api_token"]

# pin_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
pin_url = "https://api.web3.storage/upload"

# headers = {
#   'pinata_api_key': api_key,
#   'pinata_secret_api_key': api_secret
# }

headers = {
  'accept': 'application/json',
  'Authorization': 'Bearer ' + api_token
  # 'Content-Type': 'multipart/form-data'
}

def startBot(website):
    website = website.lower()
    if website.startswith('http') == True:
      pass
    elif website.startswith('www') == True:
      website = 'https://' + website
    else:
      website = 'https://www.' + website
    print(website)
    time_stamp = time.time()
    filename = str(time_stamp) + '.png'
    filelocation = 'images/' + filename
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(website)
    # driver.implicitly_wait(2)

    # # original_size = driver.get_window_size()
    # required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    # required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    # driver.set_window_size(required_width, required_height)
    # # driver.save_screenshot(path)  # has scrollbar
    # time.sleep(5)
    driver.find_element(By.XPATH, '/html/body')
    # driver.save_screenshot(filelocation)  # avoids scrollbar
    # # driver.set_window_size(original_size['width'], original_size['height'])




    ss.full_Screenshot(driver, save_path='images/', image_name=filename)
    # ss.get_element(driver, element, filelocation)

    # S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
    # driver.set_window_size(S('Width'),S('Height'))
    # height = driver.execute_script("return document.body.scrollHeight")
    # driver.set_window_size(1920,height+250)
    # time.sleep(2)
    # driver.save_screenshot(filelocation)
    # el = driver.find_element_by_tag_name('body')
    # el.screenshot(filelocation)
    driver.quit()
    # time.sleep(5)
    payload={}
    files=[
    ('file',(filelocation,open(filelocation,'rb'),'image/png'))
    ]
    response = requests.request("POST", pin_url, headers=headers, data=payload, files=files)
    print(response.text)
    # ipfs_hash = response.json()['IpfsHash']
    ipfs_hash = response.json()['cid']
    # link = 'https://mintypa.mypinata.cloud/ipfs/' + ipfs_hash + '/' + filename
    link = ipfs_hash + '/' + filename
    return link


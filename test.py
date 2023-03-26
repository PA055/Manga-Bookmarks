from selenium import webdriver
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=options)
driver.get("https://nitroscans.com/series/i-stole-the-number-one-rankers-soul")

soup = BeautifulSoup(driver.page_source, 'html.parser')
chapters = [a for a in soup.findAll('a') if 'chapter ' in a.text.lower()]

while len(chapters) <= 0:
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    chapters = [a for a in soup.findAll('a') if 'chapter ' in a.text.lower()]

print(chapters)
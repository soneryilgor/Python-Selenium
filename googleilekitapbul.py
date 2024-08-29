from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
import time

browser = webdriver.Chrome()

kitap_adi= input("Kitap adını giriniz : ")
yayin_evi= input("Kitap yayın evi giriniz : ")

browser.get("https://www.google.com")

bkm_kitap_veri_girisi= browser.find_element(By.CSS_SELECTOR, "textarea.gLFyf")
bkm_kitap_veri_girisi.send_keys(kitap_adi+ " "+ yayin_evi+ " "+ "site:bkmkitap.com")
time.sleep(2)

bkm_kitap_veri_girisi.send_keys(Keys.ENTER)
time.sleep(2)

bkm_kitap_tikla = browser.find_element(By.XPATH,("//*[@id='rso']/div[1]/div/div/div/div[1]/div/div/span/a/h3"))
bkm_kitap_tikla.click()

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
import time
import xml.etree.ElementTree as ET
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://www.google.com/")

# XML dosyasını pandas DataFrame'e dönüştürme
df = pd.read_xml("schools.xml")

# Okul isimlerini bir listeye al
okul_isimleri = df['SchoolName'].tolist()  # 'okul_adi' sütununun adı değişebilir

# Her bir okul ismini sırayla arat
for okul in okul_isimleri:
    search_box = driver.find_element("name", "q")  # Google'daki arama kutusunu bulur
    search_box.clear()  # Arama kutusunu temizler
    search_box.send_keys(okul)  # Okul ismini arama kutusuna yazar
    search_box.send_keys(Keys.RETURN)  # Enter tuşuna basarak arama yapar
    
    time.sleep(1)  # Biraz bekler, böylece sonuçlar yüklenir

 # İlk sonucun linkini al
    first_result = driver.find_element("xpath", "//h3/ancestor::a")
    link = first_result.get_attribute("href")
    
    # Linki listeye ekle
    link_listesi.append((okul, link))
    print(okul + " " +link)

# Tarayıcıyı kapat
driver.quit()

# XML dosyası oluşturma
root = ET.Element("Okullar")

for okul, link in link_listesi:
    okul_eleman = ET.SubElement(root, "Okul")
    isim_eleman = ET.SubElement(okul_eleman, "Isim")
    isim_eleman.text = okul
    link_eleman = ET.SubElement(okul_eleman, "Link")
    link_eleman.text = link

# XML ağacını dosyaya kaydet
tree = ET.ElementTree(root)
tree.write("okul_linkleri.xml", encoding="utf-8", xml_declaration=True)

# Sonuçları ekrana yazdır
for i, (okul, link) in enumerate(link_listesi):
    print(f"{okul}: {link}")

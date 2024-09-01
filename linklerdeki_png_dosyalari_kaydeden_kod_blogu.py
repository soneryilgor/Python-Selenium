import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

# XML dosyasını yükle
tree = ET.parse('arabalar.xml')
root = tree.getroot()

# img_src öğelerini bir diziye ekle
img_src_list = [img_src.text for img_src in root.iter('img_src')]

print("img_src elemanları başarıyla diziye eklendi.")
print(img_src_list)

# Selenium WebDriver'ı başlat
driver = webdriver.Chrome()


for idx, img_url in enumerate(img_src_list):
    try:
        # PNG dosyasını indirmek için istek yap
        response = requests.get(img_url)
        
        # URL'den dosya adı çıkar
        parsed_url = urlparse(img_url)
        file_name = os.path.basename(unquote(parsed_url.path))
        
        # Dosya adı boşsa bir varsayılan ad kullan
        if not file_name:
            file_name = f'logo_{idx+1}.png'
        
        # Dosya yolu oluştur
        file_path = os.path.join('logolar', file_name)
        
        # PNG dosyasını kaydet
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        print(f'{file_path} başarıyla indirildi ve kaydedildi.')
    
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    # İndirme işleminden sonra bekleme
    time.sleep(1)

# WebDriver'ı kapat
driver.quit()

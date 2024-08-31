from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
import time
import xml.etree.ElementTree as ET
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()
driver.get("gireceğiniz site linki")

# Şehir isimlerini bul ve listeye ekle
city_options = driver.find_elements(By.XPATH, "//option")
cities = [option.text.strip() for option in city_options]

index = cities.index('DÜZCE')

# Sadece 'DÜZCE' elemanına kadar olan elemanları tut
yeni_liste = cities[:index + 1]

time.sleep(2) 
yeni_dizi = yeni_liste[1:]

# XML ağacı oluşturma
root = ET.Element("SchoolsData")

for city in yeni_dizi:
    print(city)
    time.sleep(2)
    
    # Şehri seçme
    city_dropdown = driver.find_element(By.XPATH, '//*[@id="q[il]"]/option[3]')  # Doğru select elementini bulmak için uygun XPATH'i gir
    city_dropdown.click()
    
    # İlgili şehri seç
    yeni_sehir = ' '.join(city)
    city_option = driver.find_element(By.XPATH, f"//option[contains(text(), '{city}')]")
    city_option.click()
    time.sleep(2)  # Sayfanın güncellenmesi için bekleme süresi

    while True:
        # Tabloyu bul
        table = driver.find_element(By.XPATH, "//*[@id='ktbl']")  # Tabloyu tanımlayan doğru XPATH'i gir //*[@id="ktbl"]
        
        # Satırları bul
        rows = table.find_elements(By.XPATH, ".//tr")
        
        for row in rows:
            cells = row.find_elements(By.XPATH, ".//td")
            
            if len(cells) > 0:
                school = ET.SubElement(root, "School")
                ET.SubElement(school, "City").text = city
                ET.SubElement(school, "District").text = cells[2].text
                ET.SubElement(school, "SchoolName").text = cells[3].text
                ET.SubElement(school, "SchoolID").text = cells[4].text
                ET.SubElement(school, "SchoolType").text = cells[5].text
        
        # "Sonraki" butonunu bul ve tıkla
        try:
            next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Sonraki')]")
            if "disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
            time.sleep(2)  # Sayfanın yüklenmesi için bekleme süresi
        except:
            break  # Eğer "Sonraki" butonu bulunamazsa, döngüyü kır
    
    # Tüm sayfalar gezildiğinde, diğer şehre geçmek için bekle
    time.sleep(2)

# XML dosyasını oluşturma ve kaydetme
tree = ET.ElementTree(root)
tree.write("C:\\Users\\Administrator\\Desktop\\python\\schools.xml", encoding='utf-8', xml_declaration=True)

# Tarayıcıyı kapat
browser.quit()

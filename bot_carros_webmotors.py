from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re 

def saveResult(driver, page):
    filename = "seminovos_webmotors.csv"
    
    try:
        # Aguardar container principal
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.vehicle-card-oem-desktop_bodyContent__EzeMW"))
        )
        
        offers = driver.find_elements(By.CSS_SELECTOR, "div.vehicle-card-oem-desktop_bodyContent__EzeMW")
        print(f"🔥 Página {page} | {len(offers)} ofertas")
        
        with open(filename, 'a', encoding='utf-8') as file:
            for i, offer in enumerate(offers, 1):
                try:
                    # Marca e Modelo
                    make_model = WebDriverWait(offer, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "p._web-title-medium-qtpsh_51"))
                    ).text.split(" ", 1)
                    
                    # Versão
                    version = offer.find_element(By.CSS_SELECTOR, "p._body-regular-small_qtpsh_152.vehicle-card-oem-desktop_Description__AIR_1").text
                    
                    # Preço
                    price = offer.find_element(By.CSS_SELECTOR, "div.vehicle-card-oem-desktop_BodyItem__xm4xG ").text.replace("R$ ", "").replace(".", "")
                    
                    
                   # Detalhes (KM e Ano) - CORREÇÃO AQUI!
                    details_text = offer.find_element(By.CSS_SELECTOR, "div..vehicle-card-oem-desktop_Cell__RWr0u ").text
                    
                    # Extrai KM (usando regex para encontrar números seguidos de "km")
                    km = "N/A"
                    km_match = re.search(r'(\d+\.?\d*)km', details_text)
                    if km_match:
                        km = km_match.group(1).replace(".", "")
                    
                    # Extrai Ano (usando regex para encontrar padrão "XXXX/YYYY")
                    year_manufacture = "N/A"
                    year_model = "N/A"
                    year_match = re.search(r'(\d{4})\/(\d{4})', details_text)
                    if year_match:
                        year_manufacture = year_match.group(1)
                        year_model = year_match.group(2)
                    # Escrever linha
                    line = f"{make_model[0]};{make_model[1]};{version};{year_manufacture};{year_model};{km};{price};\n"
                    file.write(line)
                    print(f"✅ Oferta {i} salva")
                
                except Exception as e:
                    print(f"🚨 Erro na oferta {i}: {str(e)}")
                    continue
    
    except Exception as e:
        print(f"💥 ERRO FATAL: {str(e)}")
        driver.save_screenshot(f"error_page_{page}.png")

# Configuração
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

# Execução
try:
    for page in range(1, 26):
        driver.get(f"https://www.webmotors.com.br/carros-usados/df-brasilia?lkid=1022&tipoveiculo=carros-usados&localizacao=-15.826691%2C-47.9218204x100km&estadocidade=Distrito%20Federal-Bras%C3%ADlia&page={page}")
        saveResult(driver, page)
finally:
    driver.quit()
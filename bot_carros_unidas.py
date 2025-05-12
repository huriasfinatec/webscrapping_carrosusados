from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re 

def saveResult(driver, page):
    filename = "seminovos_unidas.csv"
    
    try:
        # Aguardar container principal
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.new-card__gap"))
        )
        
        offers = driver.find_elements(By.CSS_SELECTOR, "div.new-card__gap")
        print(f"🔥 Página {page} | {len(offers)} ofertas")
        
        with open(filename, 'a', encoding='utf-8') as file:
            for i, offer in enumerate(offers, 1):
                try:
                    # Marca e Modelo
                    make_model = WebDriverWait(offer, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "span.name-vehicle"))
                    ).text.split(" ", 1)
                    
                    # Versão
                    version = offer.find_element(By.CSS_SELECTOR, "span.info-vehicle").text
                    
                    # Preço
                    price = offer.find_element(By.CSS_SELECTOR, "span.price-vehicle").text.replace("R$ ", "").replace(".", "")
                    
                    # Localização (span.text-ellipsis)
                    location = offer.find_element(By.CSS_SELECTOR, "span.text-ellipsis").text.split(" - ")[0].strip()
                    
                   # Extrair KM e Ano separadamente
                    details = offer.find_elements(By.CSS_SELECTOR, "span.details")
                    
                    # KM (primeiro span.details)
                    km = "N/A"
                    if len(details) >= 1:
                        km_text = details[0].text.strip()
                        km_match = re.search(r'(\d{1,3}(?:\.\d{3})*)\s*km', km_text)
                        if km_match:
                            km = km_match.group(1).replace(".", "")
                    
                    # Ano (segundo span.details)
                    year = "N/A"
                    if len(details) >= 2:
                        year_text = details[1].text.strip()
                        year = year_text.replace(" ", "")  # Remove espaços: "2022/2023" → "2022/2023"
                    # Escrever linha
                    line = f"{make_model[0]};{make_model[1]};{version};{year};{km};{price};{location}\n"
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
        driver.get(f"https://seminovos.unidas.com.br/veiculos?page={page}&perpage=100&layout=grid")
        saveResult(driver, page)
finally:
    driver.quit()
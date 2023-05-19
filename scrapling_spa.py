
# pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# pip install webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

# pandas
import pandas as pd
from datetime import date
import time


# creo tabella pandas dove salveremo i valori
df = pd.DataFrame(columns=['NomeAzienda', 'Citta', 'Provincia', 'Fatturato', 'DataIndagine'])
list_NomeAzienda = []
list_Citta = []
list_Provincia = []
list_Fatturato = []
list_DataIndagine = []
provincia = 'cesena'

options = Options()
options.add_argument("--incognito")
# Creazione di un'istanza del driver di Chrome
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# Creazione delle opzioni del browser
driver.set_window_size(1920, 1080)
# Accediamo al sito
driver.get('https://www.reportaziende.it/' + provincia)

# Accettiamo i cookies cliccando sul pulsante accetta facciamo caricare la pagina
driver.implicitly_wait(3)
pulsante_accetta = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[3]/div/div[2]/button[2]')
ActionChains(driver).click(pulsante_accetta).perform()

# troviamo il tasto prossimo
# pulsatne_prossimo = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/section/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[9]')
# dovendo cliccare il pulsante 40 volte faremo un for loop per scaricare i dati

ciclo = 0
while ciclo < 40:
    
    time.sleep(2)
    # troviamo la tabella
    tabella = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/section/div[1]/div[2]/div/div[2]/div/table')
    #print(tabella.text)                               

    # prendiamo le righe della tabella
    righe_tabella = tabella.find_elements(By.TAG_NAME, 'tr')
    for riga in righe_tabella:  
        celle_riga = riga.find_elements(By.TAG_NAME, 'td')
            
        for indice, cella in enumerate(celle_riga):
                if indice == 1:
                    list_NomeAzienda.append(cella.text)
                elif indice == 2:
                    list_Citta.append(cella.text)
                elif indice == 3:
                    list_Provincia.append(cella.text)
                elif indice == 4:
                    list_Fatturato.append(cella.text)
                elif indice == 0:
                    list_DataIndagine.append(str(date.today()))
                
    nuovo_df = pd.DataFrame({'NomeAzienda': list_NomeAzienda, 'Citta': list_Citta, 'Provincia': list_Provincia, 'Fatturato': list_Fatturato, 'DataIndagine': list_DataIndagine})
    df = pd.concat([df, nuovo_df])
    print(df)

    time.sleep(5)    
    # troviamo il tasto prossimo
    try:
        pulsatne_prossimo = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/section/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[9]/a')
        #eseguo lo scroll della pagina fino al pulsante prossimo
        driver.execute_script("arguments[0].scrollIntoView();", pulsatne_prossimo)
    except:
        pulsatne_prossimo = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/section/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[9]')
        #eseguo lo scroll della pagina fino al pulsante prossimo
        driver.execute_script("arguments[0].scrollIntoView();", pulsatne_prossimo)
    
    #driver.implicitly_wait(1)
    time.sleep(3)
    #ActionChains(driver).click(pulsatne_prossimo).perform()
    pulsatne_prossimo = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/section/div[1]/div[2]/div/div[3]/div[2]/div/ul/li[9]')
    time.sleep(3)
    driver.implicitly_wait(2)
    pulsatne_prossimo.click()
    
    list_NomeAzienda.clear()
    list_Citta.clear()
    list_Provincia.clear()
    list_Fatturato.clear()
    list_DataIndagine.clear()
    time.sleep(1)
    ciclo += 1
    print(ciclo)
    

df.to_csv('C:/Users/AndreaLatorre/Desktop/PrototipiPython/webscrapling/download/aziende.csv', sep=';', header=1, index=False)
        
                             


# Chiudere il browser
driver.quit()
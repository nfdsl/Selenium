from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import os
import pandas as pd
import pdfplumber

# Etapa 1: Login Automatizado
def login():
    driver = webdriver.Chrome()
    
    try:
        
        driver.get("https://the-internet.herokuapp.com/login")
        
        usuario = driver.find_element(By.ID, "username")
        usuario.send_keys("tomsmith")
        
        senha = driver.find_element(By.ID, "password")
        senha.send_keys("SuperSecretPassword!")
        
        botao_login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        botao_login.click()
        
        WebDriverWait(driver, 20).until(
            EC.url_to_be("https://the-internet.herokuapp.com/secure")
        )
        
        print("Sucesso!")
        
    except:
        print("Ocorreu um erro durante o login.")
        
    finally:
        driver.quit()

# Etapa 2: Download e Conversão de Arquivo       
def download_csv():
    driver = webdriver.Chrome()
    
    try:
        
        driver.get("https://admin:admin@the-internet.herokuapp.com/download_secure")
        
        link = driver.find_element(By.PARTIAL_LINK_TEXT, "OrderDetails.csv")
        link.click()
        download = os.path.expanduser("~/Downloads")
        csv_file_path = os.path.join(download, "OrderDetails.csv") 
        
        WebDriverWait(driver, 20).until(lambda driver: os.path.exists(csv_file_path))
        
        if os.path.exists(csv_file_path):
            print("Arquivo CSV baixado com sucesso!")
            
       
        
    except:
        print("Ocorreu um erro durante o download.")
        
    finally:
        driver.quit()
        
# Etapa 3: Download e Conversão de Arquivo PDF
def download_pdf():
    try:
        driver = webdriver.Chrome()
        driver.get("https://admin:admin@the-internet.herokuapp.com/download_secure")
        
        pdf_link = driver.find_element(By.PARTIAL_LINK_TEXT, "samplePDF.pdf")
        pdf_link.click()
        
        download = os.path.expanduser("~/Downloads")
        arquivo_pdf = os.path.join(download, "samplePDF.pdf") 
        
        WebDriverWait(driver, 20).until(lambda driver: os.path.exists(arquivo_pdf))
        
        if os.path.exists(arquivo_pdf):
            dados = []
            with pdfplumber.open(arquivo_pdf) as pdf:
                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    linhas = texto.split('\n')
                    for linha in linhas:
                        dados.append([linha])
                        
            df = pd.DataFrame(dados, columns=['Conteúdo'])
            arquivo_xlsx = arquivo_pdf.replace('.pdf', '.xlsx')
            df.to_excel(arquivo_xlsx, index=False)
        
            print(f"PDF convertido com sucesso para: {arquivo_xlsx}")
    except:
        print("Ocorreu um erro durante o download.")
        
    finally:
        driver.quit()

# Etapa 4: Seleção de Opção no Dropdown        
def dropdown():
    try:
        driver = webdriver.Chrome()
        driver.get("https://the-internet.herokuapp.com/dropdown")
        
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dropdown"))
        )
        
        select = Select(dropdown)
        select.select_by_visible_text("Option 2")
        
        opcao_select = select.first_selected_option
        if opcao_select.text == "Option 2":
            print("Opção 2 selecionada com sucesso!")
        else:
            print("Falha ao selecionar a opção 2")
            
    except:
        print("Ocorreu um erro durante a seleção.")
        
    finally:
        driver.quit()

# Desafio Bônus: Extração de Dados de Tabela
def extracao_dados():
    try:
        driver = webdriver.Chrome()
        driver.get("https://the-internet.herokuapp.com/tables")
        
        tabela = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "table1"))
        )
        
        cabecalhos = []
        for cabecalho in tabela.find_elements(By.TAG_NAME, "th"):
            cabecalhos.append(cabecalho.text)
            
        dados_todas_linhas = []
        linhas = tabela.find_elements(By.TAG_NAME, "tr")[1:] 
        for linha in linhas:
            dado_linha = []
            for item in linha.find_elements(By.TAG_NAME, "td"):
                dado_linha.append(item.text)
            dados_todas_linhas.append(dado_linha)
        
        df = pd.DataFrame(dados_todas_linhas, columns=cabecalhos)
        
        diretorio_atual = os.getcwd()
        arquivo_saida = os.path.join(diretorio_atual, "table_data.xlsx")
        df.to_excel(arquivo_saida, index=False)
        print(f"Dados salvos com sucesso em {arquivo_saida}")
        
    except:
        print("Ocorreu um erro na extração.")
        
    finally:
        driver.quit()

        
if __name__ == "__main__":
    download_pdf()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import pandas as pd

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
        
if __name__ == "__main__":
    login()
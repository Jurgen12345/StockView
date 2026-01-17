from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



class ShowData:
    def initializeWebdriver():
        service = Service(executable_path ="chromedriver.exe")
        options = Options()
        options.add_experimental_option('detach',True)
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        return webdriver.Chrome(service=service, options=options)  

    def getIndexPrice(url,driver):
        driver = driver 
        driver.get(url)
        price = driver.find_element(By.XPATH, "//span[@data-testid='qsp-price']")
        driver.quit()
        return price

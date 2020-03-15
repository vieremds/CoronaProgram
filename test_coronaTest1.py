import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import openpyxl
import configparser
import logging
import logging.handlers
import logging.config
import pandas as pd

def Transfer():
    #get running file location and change working directory to it if required

    mainPath = os.path.dirname(__file__)
    if os.getcwd() != mainPath:
        os.chdir(mainPath)

    #Record starting time
    start_time = time.time()

    #Setting Variable for Log Name
    fileStart_time = time.localtime()
    strStart_time = time_string = time.strftime("%m%d%Y%H%M%S", fileStart_time)


    #FROM GENERAL CONFIG

    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')

    #FROM LOG CONFIG FILE
        #Define File
    logPath = config['DEFAULT']['logPath']
    logFileName = config['DEFAULT']['logFileName']
    LOG_FILENAME = logFileName+strStart_time+'.log'

    #Create Log Path
    if not os.path.exists(logPath):
        os.makedirs(logPath)

    #LogConfigFile
    logging.config.fileConfig("logConfig.ini", disable_existing_loggers=False, defaults={ 'logfilename' : LOG_FILENAME } )
    my_logger = logging.getLogger("my_logger")

    #End of LogConfig File


    def TestCoronaBrowser():

        my_logger.info("Opening Browser...")

        driver = webdriver.Chrome("C:\\Users\\Vinicius.Mendes\\Documents\\Anaconda Python\\chromedriver_win32\\chromedriver.exe")
        driver.get("https://backoffice-ng.solaris-testing.de/")
        driver.set_window_size(516, 122)

        my_logger.info("Login...")
        driver.find_element(By.NAME, "username").send_keys("newsinisa@example.com")
        driver.find_element(By.NAME, "password").send_keys("5tc5tilvkj9ypb1c6ffif7yzm0ingpai4rr4caunib5h81jcfjixq8fafnx964qm3zh5lv")
        my_logger.info("Submiting Login...")
        driver.find_element(By.CSS_SELECTOR, ".sb-button").click()

        def InternalTransferFileRead():

            my_logger.info("Opening Sheet...")
            df = pd.read_excel('InternalTransferTest.xlsx', 'Template') # can also index sheet by name or fetch all sheets

            my_logger.info("Reading Values...")


            debt_IBAN = df['Debitor IBAN'].tolist()
            credit_IBAN = df['Creditor IBAN'].tolist()
            amount = df['Amount'].tolist()
            description = df['Description'].tolist()
            valDate = df['Value Date'].tolist()
            tx_Type = df['Type'].tolist()
            tx_Id = df['TxID'].tolist()

            def InternalTransferAction():

                tx = 1
                while tx <= len(debt_IBAN):
                    time.sleep(2)
                    driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/main/div/nav/ul/li[10]/ul/li[3]/a').click()
                    driver.find_element(By.ID, "iban").clear()
                    driver.find_element(By.ID, "iban").send_keys(debt_IBAN[tx-1])
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, ".s-filter-inputs .sb-button:nth-child(1)").click()

                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR, ".s-column-align-content:nth-child(1)").click()
                    driver.find_element(By.ID, "iban").clear()
                    driver.find_element(By.ID, "iban").send_keys(credit_IBAN[tx-1])
                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, ".s-filter-inputs .sb-button:nth-child(1)").click()

                    time.sleep(2)
                    driver.find_element(By.CSS_SELECTOR, ".s-column-align-content:nth-child(1)").click()
                    driver.find_element(By.NAME, "amount").send_keys(amount[tx-1])
                    driver.find_element(By.NAME, "description").send_keys(description[tx-1])
                    driver.find_element(By.ID, "valutaDate").send_keys(valDate[tx-1])
                    driver.find_element(By.NAME, "posting_key").click()
                    dropdown = driver.find_element(By.NAME, "posting_key")
                    #here would go tx_Type, for now just Transfer
                    dropdown.find_element(By.XPATH, "//option[. = 'Transfer']").click()
                    driver.find_element(By.NAME, "posting_key").click()

                    driver.find_element(By.NAME, "instruction_id").click()
                    driver.find_element(By.NAME, "instruction_id").send_keys(tx_Id[tx-1])

                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, ".sb-button:nth-child(2)").click()

                    time.sleep(1)
                    driver.find_element(By.CSS_SELECTOR, ".sb-button:nth-child(2)").click()

                    tx = tx + 1


intTransferFile = Transfer.TestCoronaBrowser.InternalTransferFileRead()

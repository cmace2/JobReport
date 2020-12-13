import os
import json
import logging
import pandas as pd
import numpy as np
from time import sleep
from dotenv import load_dotenv
import robin_stocks as r
from bs4 import BeautifulSoup
from tqdm.notebook import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class JobReport:
    
    def __init__(self):
        load_dotenv()
        login = r.login(
            username=os.getenv('robinhood_username'),
            password=os.getenv('robinhood_password')
        )
        f = open('names.json', 'r+')
        self.cmp_names = json.load(f)

        
    def getCompanyJobCount(self, company:str):
        """
        Collect number of job listings for a company on Indeed.com

        Args:
            company (str): the name of the company to search

        Returns:
            jobcnt (int): the number of job listings
        """
        company = company.replace(' ', '-')
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)# driver.minimize_window()

        try:
            driver.get(
                    f"https://www.indeed.com/cmp/{company}/jobs?&l=United+States" # TODO: confirm &l works
            )
            jobcnt_elm = driver.find_element_by_class_name('cmp-JobListJobCount-jobCount')
            jobcnt = int(jobcnt_elm.text.split()[0].replace(',',''))
        except:
            logging.warning(f'getCount: Company "{company}" did not return a valid page. May need to add to or update names.json...')
            jobcnt = -1
        finally:
            driver.close()

        return jobcnt
    
    
    def getCompanyHoldingsNames(self):
        """
        Returns the names of companies in holdings
        """
        holdings = r.account.build_holdings()
        cmp_holdings_names = []
        for ticker in holdings:
            cmp_nm = holdings[ticker]['name']
            if 'ETF' in cmp_nm:
                continue
            elif 'MTF' in cmp_nm:
                continue
            elif cmp_nm in self.cmp_names:
                cmp_holdings_names.append(self.cmp_names[cmp_nm])
            else:
                cmp_holdings_names.append(cmp_nm)
        
        return cmp_holdings_names
    
    
    def getHoldingsJobCounts(self):
        """
        Returns the job counts for each holding
        """
        logging.info('Getting Holdings Job Counts...')
        pbar = tqdm(total=len(names:=self.getCompanyHoldingsNames()))
        
        holding_counts = {}
        for name in names:
            pbar.set_description(name)
            holding_counts.update({name:self.getCompanyJobCount(name)})
            pbar.update(1)
            
        return holding_counts
    

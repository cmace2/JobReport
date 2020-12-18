import os
import json
import boto3
import logging
import pkgutil
import argparse
import pandas as pd
from tqdm import tqdm
from time import sleep
import robin_stocks as r
from getpass import getpass
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
import chromedriver_autoinstaller
from dynamodb_json import json_util
from botocore.exceptions import ClientError
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class JobReport:

    def __init__(self, container_env:bool=False):
        """
        Log into robinhood and load the company names map

        Args:
            container_env (bool): if launching with docker this will be overriden to true
        """
        # Setup logging
        logging.basicConfig(filename='JobReport.log', filemode='w', level=logging.INFO)

        # Login to Robinhood
        self.__logIn()
        
        # Class Attributes
        self.container_env = container_env

        if self.container_env:
            logging.info('Running in container mode')
        else:
            logging.info('Running in local mode')

        self.cmp_names = json.loads(
            pkgutil.get_data('JobReport', 'config/names.json').decode("utf-8")
            )
        
        # Setup Selenium
        self.__setupDriver()

        #self.dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        #self.table = self.dynamodb.Table('JobReport')


    def __setupDriver(self) -> None:
        """
        Setup the Selenium webdriver.
        Based on https://nander.cc/using-selenium-within-a-docker-container
        """

        # Install chromedriver if not already installed
        chromedriver_autoinstaller.install()

        if self.container_env:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_prefs = {}
            chrome_options.experimental_options["prefs"] = chrome_prefs
            chrome_prefs["profile.default_content_settings"] = {"images": 2}
        else:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(options=chrome_options)


    def __logIn(self) -> None:
        """ Log into all connections """
        
        load_dotenv()
        overwrite = False

        if not (username := os.getenv('robinhood_username')):
            username = input('Enter your Robinhood username (email): ')
            overwrite = True

        if not (password := os.getenv('robinhood_password')):
            getpass(prompt='Enter your Robinhood password: ')
            overwrite = True

        _ = r.login(
            username=username,
            password=password
        )

        #logging.info('login successful')

        if overwrite:
            f = open('JobReport/.env', 'w')
            f.write(f'robinhood_username={username}\nrobinhood_password={password}')
            f.close()


    def tearDown(self) -> None:
        """ Sign out of and end all sessions """
        r.authentication.logout()
        self.driver.quit()
        logging.info('Tear down complete.')

        
    def getCompanyJobCount(self, company:str) -> int:
        """
        Collect number of job listings for a company on Indeed.com

        Args:
            company (str): the name of the company to search

        Returns:
            jobcnt (int): the number of job listings
        """
        company = company.replace(' ', '-')

        try:
            self.driver.get(
                    f"https://www.indeed.com/cmp/{company}/jobs?&l=United+States" # TODO: confirm &l works
            )
            jobcnt_elm = self.driver.find_element_by_class_name('cmp-JobListJobCount-jobCount')
            jobcnt = int(jobcnt_elm.text.split()[0].replace(',',''))
        except:
            logging.warning(f'getCount: Company "{company}" did not return a valid page. May need to add to or update names.json...')
            jobcnt = -1

        return jobcnt
    
    
    def getCompanyHoldingsNames(self) -> List[str]:
        """
        Returns the names of companies in holdings (List[str])
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
    
    
    def getHoldingsJobCounts(self) -> Dict[str, int]:
        """
        Returns the job counts for each holding (Dict[str, int])
        """
        logging.info('Getting Holdings Job Counts...')
        pbar = tqdm(total=len(names:=self.getCompanyHoldingsNames()))
        
        holding_counts = {}
        for name in names:
            pbar.set_description(name)
            holding_counts.update({name:self.getCompanyJobCount(name)})
            pbar.update(1)
        pbar.close()
        return holding_counts

    
    def dynamoPush(self, item:Dict[str, int]) -> None:
        """
        Upload data to AWS DynamoDB.
        NOTE: Although current items are columnar, future items will 
        include job descriptions which is why we require NoSQL storage.

        Args:
            record (Dict[str, int]): the row you want to upload
        """
        item.update({'date': datetime.datetime.now().date()})
        response = self.table.put_item(Item=item)


    def dynamoPullAll(self) -> pd.DataFrame:
        try:
            response = self.table.scan()
        except ClientError as e:
            logging.error(e.response['Error']['Message'])
        else:
            return pd.DataFrame(json_util.loads(response))

    def displayDash(self):
        ...
    

if __name__=='__main__':
    parser = argparse.ArgumentParser(
        prog='JobReport',
        description='Intialize a JobReport',
        )

    parser.add_argument(
        '-c',
        '--container_env', 
        required=False, 
        help='this should be set if launching with Docker',
        action='store_true'
        )

    args = parser.parse_args()
    jr = JobReport(container_env=args.container_env)
    logging.info(f'Holdings Job Counts:\n{json.dumps(jr.getHoldingsJobCounts(), indent=1)}')
    jr.tearDown()
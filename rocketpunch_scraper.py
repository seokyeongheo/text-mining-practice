import requests
import time
import pandas as pd

from selenium import webdriver
from bs4 import BeautifulSoup

pw = input('Enter PW : ')

url = "https://www.rocketpunch.com/login"
driver = webdriver.Chrome()
driver.get(url)

login_google = driver.find_element_by_xpath('//*[@id="login-main"]/div[3]/a[2]')
login_google.click()

time.sleep(1)

google_id = driver.find_element_by_xpath('//*[@id="identifierId"]')
google_id.send_keys('syh602@gmail.com')

time.sleep(1)

google_id_submit = driver.find_element_by_xpath('//*[@id="identifierNext"]/content')
google_id_submit.click()

time.sleep(1)

google_pw = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
google_pw.send_keys(pw)

time.sleep(1)

google_pw_submit = driver.find_element_by_xpath('//*[@id="passwordNext"]/content/span')
google_pw_submit.click()

time.sleep(1)

url = "https://www.rocketpunch.com/@quartz/bookmark"
driver.get(url)

time.sleep(1)

# get page sourse, parse html
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# title

date_list = []
company_list = []
job_list = []
salary_list = []
condition_list = []
special_list = []

for i in range(100):

    try:
        date = soup.findAll('div', {'class': 'job-dates'})
        date = date[i].text.split("\n")[2].strip()
        date_list.append(date)

        company = soup.findAll('div', {'class': 'company-name'})
        company = company[i].text.split('\n')[2].strip()
        company_list.append(company)

        job = soup.findAll('a', {'class': 'nowrap job-title'})
        job = job[i].text
        job_list.append(job)

        salary_condition = soup.findAll('div', {'class': 'job-stat-info'})
        salary = salary_condition[i].text.split("/")[0].strip()
        condition = salary_condition[i].text.split("/")[1].strip()
        salary_list.append(salary)
        condition_list.append(condition)

        special = soup.findAll('div', {'class': 'nowrap job-specialties'})
        special = special[i].text
        special_list.append(special)
    except:
        print("The loop is ended. You have %d bookmarks." % (i))
        break
    
data_job = pd.DataFrame(columns=['date', 'company', 'job', 'salary', 'condition', 'special'])
data_job['date'] = date_list
data_job['company'] = company_list
data_job['job'] = job_list
data_job['salary'] = salary_list
data_job['condition'] = condition_list
data_job['special'] = special_list
data_job.to_csv('rocketpunch_bookmark.csv')

driver.quit()

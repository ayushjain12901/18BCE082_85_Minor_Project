from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
df_new = "global"
df_new = pd.DataFrame()
os.getcwd()

browser = webdriver.Chrome(ChromeDriverManager().install())

browser.get('https://agmarknet.gov.in/')


def checkOptions(element_id):
    time.sleep(5)
    select = Select(browser.find_element_by_id(element_id))
    values = select.options
    return 1 if len(values) > 0 else checkOptions(element_id)

def selectValues():
    select = Select(browser.find_element_by_id('ddlCommodity'))
    print(select)
    # select by visible text
    select.select_by_visible_text('Wheat')

    # To check if values are loaded in dropdown
    checkOptions('ddlState')
    select = Select(browser.find_element_by_id('ddlState'))

    str_year = str('Gujarat')
    select.select_by_visible_text(str_year)
    # checkOptions('txtDate')
    date_el = browser.find_element_by_id('txtDate')
    date_el.clear()
    date_el.send_keys("24-Nov-2019")

    # select.select_by_visible_text('30-Sep-2020')
    # time.sleep(5)
    submit = browser.find_element_by_id('btnGo')
    submit.click()
    time.sleep(5)

def goBack():
    browser.execute_script("window.history.go(-1)")


def concatDataFrame(df,index,year):
    global df_new,start_year
    if index == 0 and year == start_year:
        df_new = df
    else:
        df_new = pd.merge(df_new, df, on='State', how='outer')
    print(df_new)

def scrapeTable():
    i=0
    res = browser.current_url
    df_final=pd.DataFrame()
    while(i!=543):
        #page = requests.get(res)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        My_table = soup.find(id='cphBody_GridPriceData')
        #My_table
        tbody = My_table.find_all('tr')
        list_rows = []
        rangee= len(tbody)-2
        if(len(tbody)<50):
            rangee=len(tbody)
        for row in range(1,rangee):
            cols = tbody[row].find_all('td')
            cols = [x.text.strip() for x in cols]
            list_rows.append(cols)
            print(cols)
        df_final= df_final.append(pd.DataFrame(list_rows))

        # bt=tbody[len(tbody)-2].find('td')
        # bt1=bt.find('td')
        # bt2=bt1.find('input')
        # print(bt2.prettify)
        try:
            button=browser.find_element_by_xpath('//input[@type="image"][@src="../images/Next.png"]')
            browser.execute_script("arguments[0].click();", button)
            time.sleep(5)
            res = browser.current_url
            i = i + 1
        except NoSuchElementException:  # spelling error making this code not work as expected
            break

    #print(df_final)
    return df_final


selectValues()
df=scrapeTable()
print(df.head())
df.to_csv('Gujarat_Wheat.csv', index = False)


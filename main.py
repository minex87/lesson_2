import os
from selenium import webdriver
import datetime
import time
import pandas as pd
import logging
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(filename='test.log',level=logging.DEBUG)
logging.error('errorメッセージ')

def setup_class(cls):
    cls.driver =webdriver.Chrome(ChromeDriverMnager().install())

def find_table_target_word(th_elms, td_elms, target:str):
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

def main():
    exp_name_list = []
    exp_salary_list = []
    exp_work_location_list = []

    driver = webdriver.Chrome()
    driver.get("https://tenshoku.mynavi.jp")

    search_keyword = input()
    search_send = driver.find_element_by_xpath(f'/html/body/div[1]/header/div/div/div[2]/div/form/div[1]/input')
    search_send.send_keys(search_keyword)
    driver.find_element_by_xpath(f'//*/div[2]/div/div/div/div/a[1]').click()
    driver.find_element_by_xpath(f'/html/body/div[1]/header/div/div/div[2]/div/form/button').click()

    while True:
        name_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__name")
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")
        table_list2 = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")

        for name, table, table2 in zip(name_list,table_list,table_list2):
            try:
                exp_name_list.append(name.text)
                salary = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "給与")
                exp_salary_list.append(salary)
                work_location = find_table_target_word(table.find_elements_by_tag_name("th"), table.find_elements_by_tag_name("td"), "勤務地")
                exp_work_location_list.append(work_location)
            except:
                pass

        next_page = driver.find_elements_by_class_name("iconFont--arrowLeft")
        if len(next_page) >= 1:
            next_page_link = next_page[0].get_attribute("href")
            driver.get(next_page_link)
        else:
            break
    df = pd.DataFrame({'会社名':exp_name_list,'給料':exp_salary_list,'勤務地':exp_work_location_list})
    df.to_csv('mynavi.csv',encoding="UTF-8")

if __name__ == "__main__":
    main()
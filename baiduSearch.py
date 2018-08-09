#!/usr/bin/env python
# -*- coding:utf-8 -*-
# outhor:李仲新 time:2018/7/31
from selenium import webdriver
from bs4 import BeautifulSoup


class BaikeSearch:
    def __init__(self):
        self.driver = webdriver.PhantomJS()
        # self.driver.set_window_size(1366, 768)
        # self.driver = webdriver.Chrome()
        self.driver.get("https://baike.baidu.com")
        # 如果没有在环境变量指定PhantomJS位置
        # self.driver = webdriver.PhantomJS(executable_path = "./phantomjs/bin/phantomjs")

    def Search(self, words):
        content = "百度百科尚未收录词条{}".format(words)
        self.driver.find_element_by_id('query').clear()
        self.driver.find_element_by_id('query').send_keys(words)
        try:
            self.driver.find_element_by_id('search').click()
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.find('div', class_='para').get_text()
            return content
        except:
            return content

    def Close(self):
        try:
            self.driver.quit()
            self.driver.close()
        except:
            return True

if __name__ == '__main__':
    B = BaikeSearch()
    print(B.Search('python'))
    print(type(B.Search('python')))
    print("***************************************")
    print(B.Search('爬虫'))
    print("***************************************")
    print(B.Search('python爬虫'))
    B.Close()
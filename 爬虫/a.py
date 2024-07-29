# 代码测试
from selenium import webdriver
import requests

url = "https://vacations.ctrip.com/list/whole/sc206.html?st=%E6%B9%96%E5%8D%97&startcity=206&sv=%E6%B9%96%E5%8D%97"

driver = webdriver.Chrome()
driver.get(url)
print(driver.page_source)

print(requests.get(url).text)
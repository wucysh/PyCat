"""
键盘操作--将百度搜索的关键字复制到必应中进行搜索
--导入模块from selenium.webdriver.common.keys import Keys
--剪切
--复制
--  问题Chrome 71 version 无效
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome("/Users/wucysh/Desktop/Tengern/Python/soft/chromedriver")  # 驱动浏览器
driver.get("http://www.baidu.com/")

driver.find_element_by_css_selector("#kw").send_keys("Python")
sleep(4)

# 键盘全选操作
driver.find_element_by_css_selector("#kw").send_keys(Keys.COMMAND, 'a')

# js 复制
driver.execute_script('document.getElementById("kw").select()')
driver.execute_script('document.execCommand("Copy")')
driver.execute_script('var element = $("<textarea>YYC</textarea>");$("body").append(element);element[0].select();document.execCommand("Paste");')

sleep(2)

# 键盘复制操作
driver.find_element_by_css_selector("#kw").send_keys(Keys.COMMAND, 'c')
sleep(2)

# 键盘剪切操作
# driver.find_element_by_css_selector("#kw").send_keys(Keys.CONTROL,'x')
# sleep(2)

driver.get("https://cn.bing.com/")
sleep(4)
driver.execute_script('document.getElementById("sb_form_q").select()')
driver.execute_script('document.execCommand("Paste")')
driver.find_element_by_css_selector("#sb_form_q").send_keys(Keys.COMMAND, 'v')
sleep(4)
driver.find_element_by_css_selector(".b_searchboxSubmit").click()
sleep(4)

driver.quit()

# coding=utf-8
# author='Shichao-Dong'
# create time: 2018/7/3
import sys

from appium import webdriver
import time

desired_caps = {
                'platformName': 'Android',
                'platformVersion': '7.0',
                'deviceName': 'WTKGY17811000030',
                'appPackage': 'com.tencent.mm',
                'appActivity': '.ui.LauncherUI',
                'unicodeKeyboard': True,
                'resetKeyboard': True,
                'noReset': True,
                'chromedriverExecutableDir':"D://chromedriver//2.20",
                'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'}
                }

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(10)
driver.save_screenshot('D://code//test/demo.png')
#进入订阅号
driver.find_elements_by_id("com.tencent.mm:id/apv")[3].click()
driver.find_elements_by_id("com.tencent.mm:id/apv")[0].click()
driver.find_elements_by_id("com.tencent.mm:id/aaq")[0].click()
driver.find_elements_by_class_name("android.widget.TextView")[0].click()
time.sleep(3)
#切换webview
print(driver.contexts)
driver.switch_to.context('WEBVIEW_com.tencent.mm:tools')
time.sleep(2)
handles = driver.window_handles
print len(handles)

try:
    driver.switch_to_window(handles[1])
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="namespace_1"]/div[2]/div[1]/a[1]').click()
    time.sleep(2)
    print('定位成功')
except Exception :
    print('切换之下一个handle')

print('开始截图')
driver.switch_to.context('NATIVE_APP')
driver.save_screenshot('D://code//test/lihai.png')
print('截图成功')
driver.find_element_by_id('com.tencent.mm:id/i2').click()
time.sleep(1)
driver.find_element_by_id('com.tencent.mm:id/hm').click()
driver.save_screenshot('D://code//test/dingyue.png')
driver.quit()
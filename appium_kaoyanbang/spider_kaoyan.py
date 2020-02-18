import time

from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

cap = {
  "platformName": "Android",
  "platformVersion": "5.1.1",
  "deviceName": "127.0.0.1:62025",
  "appPackage": "com.tal.kaoyan",
  "appActivity": "com.tal.kaoyan.ui.activity.SplashActivity",
  "noReset": True
}

driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub', desired_capabilities=cap)

def get_size():
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    return (x, y)


try:
    #同意隐私条款
    if WebDriverWait(driver, 3).until(lambda x:x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tip_title']")):
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tip_commit']").click()
except:
    pass


try:
    #是否跳过
    if WebDriverWait(driver, 30).until(lambda x:x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_skip']")):
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/tv_skip']").click()
except:
    pass

try:
    #访客随便看看
    if WebDriverWait(driver, 3).until(lambda x:x.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.tal.kaoyan:id/login_scan_btn']")):
        driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.tal.kaoyan:id/login_scan_btn']").click()
except:
    pass

try:
    #选择默认考研年份进入
    if WebDriverWait(driver, 3).until(lambda x:x.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/kylogin_perfect_year_commit']")):
        driver.find_element_by_xpath("//android.widget.TextView[@resource-id='com.tal.kaoyan:id/kylogin_perfect_year_commit']").click()
except:
    pass

try:
    #关掉第一个广告，不绑定手机号
    if WebDriverWait(driver, 3).until(lambda x:x.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.tal.kaoyan:id/view_wemedia_image']")):
        driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.tal.kaoyan:id/view_wemedia_cacel']").click()
except:
    pass

try:
    #关掉第二个广告，不定目标
    if WebDriverWait(driver, 3).until(lambda x:x.find_element_by_xpath("//android.widget.LinearLayout")):
        driver.find_element_by_xpath("//android.widget.ImageView[@resource-id='com.tal.kaoyan:id/kaoyan_home_schtip_close']").click()
except:
    pass

#点击研讯
if WebDriverWait(driver, 3).until(lambda x:x.find_element_by_xpath("//android.view.View[@resource-id='com.tal.kaoyan:id/date_fix']/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]")):
    driver.find_element_by_xpath("//android.view.View[@resource-id='com.tal.kaoyan:id/date_fix']/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]/android.widget.ImageView[1]").click()

    s = get_size()

    x1 = int(s[0]*0.5)
    y1 = int(s[1]*0.75)
    y2 = int(s[1]*0.25)

    #滑动操作
    while True:
        driver.swipe(x1, y1, x1, y2)
        time.sleep(1)

import pickle
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# 使用无头模式
options = Options()
options.add_argument("--headless")

driver_path = '/Users/nebneb/Downloads/chromedriver-mac-arm64/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path, options=options)

# 打开网址但不立即加载Cookies
driver.get("https://glados.rocks/console/checkin")

# 等待页面完全加载（你可以根据需要增加或减少等待时间）
time.sleep(5)

# 加载Cookies
with open("/Users/nebneb/Desktop/cookies.pkl", "rb") as cookies_file:
    cookies = pickle.load(cookies_file)
    for cookie in cookies:
        driver.add_cookie(cookie)

# 导航到同一页面或其他需要身份验证的页面
driver.get("https://glados.rocks/console/checkin")

# 等待签到按钮出现
wait = WebDriverWait(driver, 20)  # 最多等待20秒

# 找到签到按钮并点击
checkin_button = driver.find_element_by_css_selector('.ui.positive.button')
checkin_button.click()

# input("请检查是否签到成功，然后按Enter键继续...")

# 关闭浏览器
driver.quit()

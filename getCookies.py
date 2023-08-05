from selenium import webdriver
import pickle

# 这边将路径改为自己的chrome driven的文件路径
driver_path = '/Users/nebneb/Downloads/chromedriver-mac-arm64/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)

driver.get("https://glados.rocks/console/checkin")

# 等待手动登录
input("请手动登录到网站，然后按Enter键继续...")

# 保存Cookies，这边需要修改cookie的保存路径至自己的路径下
with open("/Users/nebneb/Desktop/cookies.pkl", "wb") as cookies_file:
    pickle.dump(driver.get_cookies(), cookies_file)

print("Cookies已保存！")
driver.quit()

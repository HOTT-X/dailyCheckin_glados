# dailyCheckin_glados
Glados的每日自动签到脚本
Glados每日签到可以白嫖一天的使用时间，于是在chatgpt的帮助下写了一个在本地自动运行的脚本，以下是几点说明

- 应该还有很多优化空间，目前的操作步骤还是有些繁琐的

- 每日脚本运行时需要计算机是运行着的，如果处于关机状态则脚本无法运行。（感觉可以通过多设置几个运行时间解决这个问题）
- 写完了回过头看发现怎么这么一长串内容www，欢迎各位大佬批评指正

以下为操作流程：



### 宏观版：

安装环境 -> 手动获取cookie ->  测试脚本 -> 修改为无头脚本 -> 设置定时



### 微观版：

1. 安装环境：

   - 在如下的网页中下载对应自己谷歌浏览器版本的驱动https://sites.google.com/chromium.org/driver/downloads/version-selection ，保存至某一路径下供后面脚本使用

   - 在终端运行命令安装相关包文件 `pip3 install selenium`

2. 获取cookie

   - 先新建一个getCookie.py的文件，将以下代码复制进去，将路径修改为自己的本地路径后运行。在脚本打开chrome后需要先手动登陆下glados，然后回到终端随便按什么键往下运行即可。

   ```python
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
   
   ```

   - 现在我们就已经获取到我们的 cookie 了，以我的路径为例，保存在`/Users/nebneb/Desktop/cookies.pkl`路径下

3. 测试自动化脚本

   - 然后再新建一个 dailyCheckin_glados.py 的文件，将以下代码复制进去，我们验证一下脚本是否能够正常使用。**需要在 driver_path 和加载 Cookies 处替换为自己的路径！**

     ```python
     import pickle
     import time
     from selenium import webdriver
     from selenium.webdriver.support.ui import WebDriverWait
     from selenium.webdriver.chrome.options import Options
     
     # 使用无头模式
     options = Options()
     # options.add_argument("--headless")
     
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
     
     input("请检查是否签到成功，然后按Enter键继续...")
     
     # 关闭浏览器
     driver.quit()
     
     ```

   - 若流程正常则说明脚本无误已能够正常使用

4. 修改为无头脚本

   - 开启无头模式，因为我们肯定不希望每天还看着这个脚本把chrome呼出来然后签完道又关闭，所以我们再稍微修改一下我们的代码。只需将 `# options.add_argument("--headless")` 的#删去，将 `input("请检查是否签到成功，然后按Enter键继续...")` 加上#作为注释即可，完整示例代码如下

     ```python
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
     
     ```

5. 设置定时

   - 根据GPT所云，mac和windows系统不太一样

     - mac：在mac系统中，可以通过crontab命令来创建定时任务。

       ```
       1. 打开terminal终端
       2. 输入 crontab -e 并按回车键。这将打开一个编辑器，允许你编辑你的crontab文件
       3. 在文件中添加以下三行，每行表示一个任务。为我的示例，将脚步路径改为自己的即可，这边为了确保每天我能签上到所以我设置了三个重复定时。
       0 11 * * * /usr/bin/python3 /Users/nebneb/Desktop/dailyCheckIn_glados.py
       0 16 * * * /usr/bin/python3 /Users/nebneb/Desktop/dailyCheckIn_glados.py
       0 20 * * * /usr/bin/python3 /Users/nebneb/Desktop/dailyCheckIn_glados.py
       4. 在terminal的文本编辑器中，在英文输入下，按 i 是开启输入，输入完后按下 ctrl c，然后输入 :wq 即可保存退出
       ```

       


     - Windows：可以使用任务计划程序，以下为chatGPT口述内容转达

       ```
       1. 在Windows中，你可以使用任务计划程序来创建定时任务。以下是如何创建一个每天特定时间运行Python脚本的基本步骤：
       
       2. 打开任务计划程序。你可以在开始菜单中搜索"任务计划程序"或在运行对话框（Win+R）中输入 taskschd.msc 来打开它。
       
       3. 在右侧的操作面板中，点击"创建基本任务"。
       
       4. 在弹出的向导中，输入任务的名称和描述，然后点击"下一步"。
       
       5. 在"触发器"选项中，选择"每日"，然后点击"下一步"。
       
       6. 在"每日"选项中，设置你想要任务开始执行的时间，例如上午11点或下午4点，然后点击"下一步"。
       
       7. 在"操作"选项中，选择"启动程序"，然后点击"下一步"。
       
       8. 在"启动程序"选项中，浏览并选择你的Python解释器的路径（例如，C:\Python39\python.exe）并在"添加参数（可选）"框中输入你的脚本的路径。确保所有路径都是绝对路径。
       
       9. 最后，点击"下一步"，然后在概览页面中确认你的设置，并点击"完成"。
       
       现在，你应该已经设置好了一个任务，它会在每天特定的时间运行你的Python脚本。
       ```

       

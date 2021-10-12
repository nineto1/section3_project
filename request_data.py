from selenium import webdriver
import time
import os

webdriver_path = os.getcwd() + '\chromedriver\chromedriver'
download_path = os.getcwd() + '\\rawdata\\'

print(download_path)

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "download.default_directory" : download_path,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
driver = webdriver.Chrome(webdriver_path, options=options)

driver.get("http://data.seoul.go.kr/dataList/OA-15548/S/1/datasetView.do")
driver.implicitly_wait(5)

driver.find_element_by_xpath("""//*[@id="baseHeader"]/div[2]/div/a[1]""").click()
driver.implicitly_wait(3)

driver.find_element_by_xpath("""//*[@id="userid"]""").send_keys("nineto1")
driver.find_element_by_xpath("""//*[@id="userpwd"]""").send_keys("kyehyun!44")
driver.find_element_by_xpath("""//*//*[@id="baseBody"]/div[2]/div/div/div[1]/button""").click()
driver.implicitly_wait(5)

for idx in range(1, 6) :
    name = "fileTr_"+str(idx)
    driver.find_element_by_xpath(f"""//*[@id="{name}"]/td[6]/a""").click()
    driver.implicitly_wait(5)

time.sleep(60)
driver.quit()



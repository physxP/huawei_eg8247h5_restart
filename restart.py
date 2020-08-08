import selenium
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
while True:

	try:
		print('Loading Driver')
		WINDOW_SIZE = "1920,1080"

		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)


		driver = webdriver.Chrome(options=chrome_options)

		driver.implicitly_wait(20)
		driver.get("http://192.168.18.1/")

		id_username = driver.find_element_by_class_name("logininputcss")
		id_username.send_keys('Epuser')
		id_password = driver.find_element_by_name("txt_Password")
		id_password.send_keys('userEp')

		driver.find_element_by_id("loginbutton").click()


		driver.switch_to.frame("menuIframe")
		driver.implicitly_wait(20)

		driver.find_element_by_id("RestartIcon").click()
		#
		driver.switch_to.frame("routermngtpageSrc")
		time.sleep(5)
		reboot_button = driver.find_element_by_id("btnReboot")
		reboot_button.click()
		time.sleep(5)
		driver.switch_to.alert.accept()
		time.sleep(30)
		driver.quit()
		print('Done')
		break
	except Exception as e:

		print("Error while trying to restart router: ",e)
		print("Retrying...")
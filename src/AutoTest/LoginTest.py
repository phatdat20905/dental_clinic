# import unittest
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time
# from selenium.webdriver.support.ui import WebDriverWait 
# from selenium.webdriver.support import expected_conditions as EC
# # inherit TestCase Class and create a new test class
# username ='ADMIN'
# access_key = ''
# class DjangoTest(unittest.TestCase):
#     # initialization of webdriver
#     def setUp(self):
#         self.driver = webdriver.Chrome()
      
  
#     # cleanup method called after every test performed
#     # TH1 nhap email đ, pw sai  ---> KQ kỳ vọng login f
#     # TH2 Nhap email sai, pw đúng --> login f 
#     # TH3 nhập đúng cả 2 --> loging thành công ---> vào trong trang hệ thông 
#     # TH4 Nhap sai ca email, pw
#     # khong nhap gi het --- login f 
#     def tearDown(self):
#         self.driver.close()
#     # unittest
#     # quy tac dat ten : test_unit_[ten functoin]
#     def test_unit_login_3(self): 
#         """
#         Test the login functionality of the admin site.
#         This test performs the following steps:
#         1. Opens the admin login page.
#         2. Enters the email "ngophatdat2k5@gmail.com".
#         3. Enters the password "123456".
#         4. Submits the login form.
#         5. Verifies that the page title is "Site administration | Django site admin".
#         Assertions:
#         - The page title should be "Site administration | Django site admin" after login.
#         """
#         # try:
#         # get driver
#         print('bat dau')
#         driver = self.driver
#         # get python.org using selenium
#         driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
#         # Chờ đợi email input hiện diện 
#         inputEmail = WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.NAME, "email")) ) 
#         inputEmail.send_keys("ngophatdat2k5@gmail.com")

#         password  = driver.find_element(By.NAME,value="password")
   
#         password.send_keys("123456")
#         # time.sleep(5)

#         password.send_keys(Keys.RETURN)

#         # time.sleep(10)
#         actualTitle = driver.title 
#         print(actualTitle)
#         # assert actualTitle ,"Site administration | Django site admin"
#         assert(actualTitle == "Site administration | Django site admin")

#         # receive data
#         # elem.send_keys(Keys.RETURN)
#         # assert "No results found." not in driver.page_source

#     # def test_unit_login_2(self): 
#     #     """
#     #     Test the login functionality of the Django admin site.
#     #     This test performs the following steps:
#     #     1. Opens the Django admin login page.
#     #     2. Enters the email "ngophatdat2k5@gmail.com".
#     #     3. Enters the password "qqqqqqqqqq".
#     #     4. Submits the login form.
#     #     5. Verifies that the page title after login is "Log in | Django site admin".
#     #     Asserts:
#     #         The page title after login is "Log in | Django site admin".
#     #     """
#     #     # try:
#     #     # get driver
#     #     print('bat dau')
#     #     driver = self.driver
#     #     # get python.org using selenium
#     #     driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
#     #     inputEmail  = driver.find_element(By.NAME,value="email")
    
#     #     inputEmail.send_keys("ngophatdat2k5@gmail.com")
#     #     # time.sleep(5)
#     #     password  = driver.find_element(By.NAME,value="password")
#     #     password.send_keys("qqqqqqqqqq")
#     #     # time.sleep(5)

#     #     password.send_keys(Keys.RETURN)

#     #     # time.sleep(10)
#     #     actualTitle = driver.title 
#     #     print(actualTitle)
#     #     # assert actualTitle ,"Site administration | Django site admin"
#     #     assert(actualTitle == "Log in | Django site admin")
#     # def test_unit_login_1(self): 
#     #     """
#     #     Test the login functionality of the Django admin site.
#     #     This test performs the following steps:
#     #     1. Opens the Django admin login page.
#     #     2. Enters the email "ngophatdat2k5@gmail.com".
#     #     3. Enters the password "qqqqqqqqqq".
#     #     4. Submits the login form.
#     #     5. Verifies that the page title after login is "Log in | Django site admin".
#     #     Asserts:
#     #         The page title after login is "Log in | Django site admin".
#     #     """
#     #     # try:
#     #     # get driver
#     #     print('bat dau')
#     #     driver = self.driver
#     #     # get python.org using selenium
#     #     driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
#     #     inputEmail  = driver.find_element(By.NAME,value="email")
    
#     #     inputEmail.send_keys("ngophatdat@gmail.com")
#     #     # time.sleep(5)
#     #     password  = driver.find_element(By.NAME,value="password")
#     #     password.send_keys("123456")
#     #     # time.sleep(5)

#     #     password.send_keys(Keys.RETURN)

#     #     # time.sleep(10)
#     #     actualTitle = driver.title 
#     #     print(actualTitle)
#     #     # assert actualTitle ,"Site administration | Django site admin"
#     #     assert(actualTitle == "Log in | Django site admin")

# # execute the script
# if __name__ == "__main__":
#     unittest.main()

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class LoginTest(unittest.TestCase):
    def setUp(self):
        # Khởi tạo driver của bạn ở đây, ví dụ:
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_unit_login_3(self):
        """
        Test the login functionality of the admin site.
        This test performs the following steps:
        1. Opens the admin login page.
        2. Enters the email "ngophatdat2k5@gmail.com".
        3. Enters the password "123456".
        4. Submits the login form.
        5. Verifies that the page title is "Site administration | Django site admin".
        Assertions:
        - The page title should be "Site administration | Django site admin" after login.
        """
        print('bat dau')
        driver = self.driver
        driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/")
        
        # Chờ trang tải hoàn toàn
        WebDriverWait(driver, 20).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        
        # Sử dụng XPATH để tìm inputEmail
        inputEmail = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='email']"))
        )
        inputEmail.send_keys("ngophatdat2k5@gmail.com")

        # Sử dụng XPATH để tìm password
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        password.send_keys("123456")
        password.send_keys(Keys.RETURN)

        # Chờ tiêu đề trang
        WebDriverWait(driver, 10).until(
            EC.title_is("Site administration | Django site admin")
        )
        actualTitle = driver.title 
        print(actualTitle)
        assert actualTitle == "Site administration | Django site admin"

if __name__ == "__main__":
    unittest.main()

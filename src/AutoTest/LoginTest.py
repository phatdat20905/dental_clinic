import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
      
    def tearDown(self):
        self.driver.quit()
    
    def test_login_with_valid_credentials(self):
        """
        Test the login functionality with valid credentials.
        This test performs the following steps:
        1. Opens the login page.
        2. Enters the email and password.
        3. Submits the login form.
        4. Verifies the redirection based on user role.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")
        
        # Điền thông tin đăng nhập hợp lệ
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("ngophatdat2k5@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("123456")
        
        # Gửi biểu mẫu
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        # Đợi và kiểm tra sự chuyển hướng sau khi đăng nhập
        try:
            WebDriverWait(driver, 20).until(EC.url_contains("/home/"))
            self.assertIn("home", driver.current_url)
        except TimeoutException:
            # Kiểm tra xem người dùng có đăng nhập thành công hay không
            try:
                user_menu = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".nav-item.dropdown"))
                )
                self.assertTrue(user_menu.is_displayed(), "User menu not displayed; login may have failed")
            except TimeoutException:
                self.fail("Redirection to home page failed and user menu not displayed")
    
    def test_login_with_invalid_credentials(self):
        """
        Test the login functionality with invalid credentials.
        This test performs the following steps:
        1. Opens the login page.
        2. Enters the email and incorrect password.
        3. Submits the login form.
        4. Verifies the error message is displayed.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")
        
        # Điền thông tin đăng nhập không hợp lệ
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("ngophatdat2k5@gmail.com")
        driver.find_element(By.NAME, "password").send_keys("wrongpassword")
        
        # Gửi biểu mẫu
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        # Đợi và kiểm tra thông báo lỗi
        try:
            error_message = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error"))
            )
            self.assertTrue(error_message.is_displayed())
            self.assertIn("Wrong Email Or Password!", error_message.text)
        except TimeoutException:
            self.fail("Error message not displayed within the time limit")
    
    def test_login_with_nonexistent_user(self):
        """
        Test the login functionality with a non-existent user.
        This test performs the following steps:
        1. Opens the login page.
        2. Enters the email of a non-existent user.
        3. Submits the login form.
        4. Verifies the error message is displayed.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")
        
        # Điền thông tin đăng nhập của người dùng không tồn tại
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("nonexistent@example.com")
        driver.find_element(By.NAME, "password").send_keys("123456")
        
        # Gửi biểu mẫu
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        # Đợi và kiểm tra thông báo lỗi
        try:
            error_message = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error"))
            )
            self.assertTrue(error_message.is_displayed())
            self.assertIn("Can't Find User", error_message.text)
        except TimeoutException:
            self.fail("Error message not displayed within the time limit")
    
    def test_login_with_empty_fields(self):
        """
        Test the login functionality with empty email and password fields.
        This test performs the following steps:
        1. Opens the login page.
        2. Leaves the email and password fields empty.
        3. Submits the login form.
        4. Verifies the validation error messages are displayed.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")
        
        # Để trống các trường email và mật khẩu
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email")))
        
        # Gửi biểu mẫu
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

        # Đợi và kiểm tra thông báo lỗi
        try:
            error_message = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "error"))
            )
            self.assertTrue(error_message.is_displayed())
            self.assertIn("This field is required.", error_message.text)
        except TimeoutException:
            self.fail("Error message not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

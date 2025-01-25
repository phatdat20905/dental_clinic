import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class RegisterTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
      
    def tearDown(self):
        self.driver.quit()
    
    def test_register_with_valid_data(self):
        """
        Test the register functionality with valid data.
        This test performs the following steps:
        1. Opens the register page.
        2. Fills in the registration form with valid data.
        3. Submits the registration form.
        4. Verifies that the success message is displayed.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/register/")
        
        # Điền thông tin vào form đăng ký
        driver.find_element(By.NAME, "email").send_keys("ngophatdat160@gmail.com")
        driver.find_element(By.NAME, "full_name").send_keys("Trần Văn A")
        driver.find_element(By.NAME, "gender").send_keys("Nam")
        driver.find_element(By.NAME, "phone_number").send_keys("0123456789")
        driver.find_element(By.NAME, "address").send_keys("123 Đường ABC")
        driver.find_element(By.NAME, "password1").send_keys("password123")
        driver.find_element(By.NAME, "password2").send_keys("password123")
        # Trường ảnh có thể để trống hoặc upload ảnh mặc định nếu cần thiết.
        
        # Gửi biểu mẫu
        driver.find_element(By.NAME, "password2").send_keys(Keys.RETURN)

        # Đợi trang tải và kiểm tra thông báo thành công
        try:
            success_message = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".alert-success"))
            )
            self.assertTrue(success_message.is_displayed())
            self.assertIn("Account created successfully!", success_message.text)
        except TimeoutException:
            self.fail("Success message not displayed within the time limit")
    
    def test_register_with_invalid_data(self):
        """
        Test the register functionality with invalid data.
        This test performs the following steps:
        1. Opens the register page.
        2. Fills in the registration form with invalid data (e.g., mismatched passwords).
        3. Submits the registration form.
        4. Verifies that the error message is displayed.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/register/")
        
        # Điền thông tin vào form đăng ký với dữ liệu không hợp lệ
        driver.find_element(By.NAME, "email").send_keys("ngophatdat160@gmail.com")
        driver.find_element(By.NAME, "full_name").send_keys("Trần Văn A")
        driver.find_element(By.NAME, "gender").send_keys("Nam")
        driver.find_element(By.NAME, "phone_number").send_keys("0123456789")
        driver.find_element(By.NAME, "address").send_keys("123 Đường ABC")
        driver.find_element(By.NAME, "password1").send_keys("password123")
        driver.find_element(By.NAME, "password2").send_keys("differentpassword")
        
        # Gửi biểu mẫu
        driver.find_element(By.NAME, "password2").send_keys(Keys.RETURN)

        # Đợi trang tải và kiểm tra thông báo lỗi
        try:
            error_message = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".error"))
            )
            self.assertTrue(error_message.is_displayed())
            self.assertIn("The two password fields didn't match.", error_message.text)
        except TimeoutException:
            self.fail("Error message not displayed within the time limit")
    
    def test_register_with_missing_data(self):
        """
        Test the register functionality with missing data.
        This test performs the following steps:
        1. Opens the register page.
        2. Leaves some fields empty in the registration form.
        3. Submits the registration form.
        4. Verifies that the error message is displayed.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/register/")
        
        # Điền thông tin vào form đăng ký với dữ liệu thiếu
        driver.find_element(By.NAME, "email").send_keys("ngophatdat160@gmail.com")
        # Bỏ qua các trường full_name, gender, phone_number, address
        
        driver.find_element(By.NAME, "password1").send_keys("password123")
        driver.find_element(By.NAME, "password2").send_keys("password123")
        
        # Gửi biểu mẫu
        driver.find_element(By.NAME, "password2").send_keys(Keys.RETURN)

        # Đợi trang tải và kiểm tra thông báo lỗi
        try:
            error_message = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".error"))
            )
            self.assertTrue(error_message.is_displayed())
            self.assertIn("This field is required.", error_message.text)
        except TimeoutException:
            self.fail("Error message not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

class UpdateUserTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
      
    def tearDown(self):
        self.driver.quit()

    def test_update_user_info(self):
        """
        Test the update user information functionality with valid data.
        This test performs the following steps:
        1. Opens the login page and logs in.
        2. Opens the user's profile page.
        3. Clicks on the "Edit" button to open the modal.
        4. Fills in the update form with valid data.
        5. Submits the update form.
        6. Verifies that the user's name is displayed after update.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")

        # Đăng nhập
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("ngophatdat80@gmail.com")
        password_input.send_keys("123456")
        password_input.send_keys(Keys.RETURN)

        # Chờ trang tải hoàn toàn
        sleep(3)  # Thêm khoảng chờ 3 giây

        # Mở trang hồ sơ người dùng
        driver.get("http://127.0.0.1:8000/profile/ngo-phat-dat/")  # Thay thế bằng URL thực tế của trang hồ sơ người dùng

        # Chờ và bấm vào nút "Edit"
        edit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Edit')]"))
        )
        edit_button.click()

        # Chờ modal tải hoàn toàn
        modal_visible = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'exampleModal'))
        )

        if modal_visible:
            # Thêm khoảng chờ để đảm bảo modal đã mở hoàn toàn
            sleep(2)  # Chờ thêm 2 giây

            # # Điền form cập nhật thông tin người dùng
            # email_input = driver.find_element(By.NAME, 'email')
            # email_input.clear()
            # email_input.send_keys('updated_email@example.com')  # Thay thế bằng email mới

            fullname_input = driver.find_element(By.NAME, 'fullname')
            fullname_input.clear()
            fullname_input.send_keys('Nguyễn Văn B')  # Thay thế bằng tên đầy đủ mới

            gender_select = Select(driver.find_element(By.NAME, 'gender'))
            gender_select.select_by_visible_text('Nữ')  # Thay đổi giới tính nếu cần

            phone_input = driver.find_element(By.NAME, 'phone')
            phone_input.clear()
            phone_input.send_keys('0987654321')  # Thay thế bằng số điện thoại mới

            address_input = driver.find_element(By.NAME, 'address')
            address_input.clear()
            address_input.send_keys('456 Đường XYZ')  # Thay thế bằng địa chỉ mới

            # Gửi form cập nhật
            save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
            save_button.click()

            # Chờ và kiểm tra kết quả
            try:
                updated_name = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Nguyễn Văn B')]"))
                )
                self.assertTrue(updated_name.is_displayed())
            except TimeoutException:
                self.fail("Updated name not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

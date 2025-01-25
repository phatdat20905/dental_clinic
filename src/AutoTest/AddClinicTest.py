import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import urllib.request

class AddClinicTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
      
    def tearDown(self):
        self.driver.quit()

    def test_add_clinic(self):
        """
        Test the add clinic functionality with valid data.
        This test performs the following steps:
        1. Opens the login page and logs in.
        2. Clicks on the "Thêm phòng khám" button to go to the add clinic page.
        3. Fills in the clinic form with valid data.
        4. Submits the clinic form.
        5. Verifies that the clinic list page is displayed again.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")

        # Đăng nhập
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("nguyenthanhtung@gmail.com")
        password_input.send_keys("123456")
        password_input.send_keys(Keys.RETURN)

        # Chờ trang tải hoàn toàn
        sleep(3)  # Thêm khoảng chờ 3 giây

        # Mở trang danh sách phòng khám của tôi
        driver.get("http://127.0.0.1:8000/manage/my-clinics/")

        # Chờ và bấm vào nút "Thêm phòng khám"
        add_clinic_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Thêm phòng khám')]"))
        )
        add_clinic_button.click()

        # Chờ trang thêm phòng khám tải hoàn toàn
        form_loaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'clinic_name'))
        )

        if form_loaded:
            # Điền form thêm phòng khám
            clinic_name_input = driver.find_element(By.NAME, 'clinic_name')
            clinic_name_input.send_keys('Phòng Khám Nha Khoa Tâm Đức')
            sleep(1)  # Thêm khoảng chờ 1 giây

            address_input = driver.find_element(By.NAME, 'address')
            address_input.send_keys('123 Đường ABC')
            sleep(1)  # Thêm khoảng chờ 1 giây


            phone_number_input = driver.find_element(By.NAME, 'phone_number')
            phone_number_input.send_keys('0123456789')
            sleep(1)  # Thêm khoảng chờ 1 giây

            opening_hours_input = driver.find_element(By.NAME, 'opening_hours')
            opening_hours_input.send_keys('08:00 - 18:00')
            sleep(1)  # Thêm khoảng chờ 1 giây

            max_patients_per_slot_input = driver.find_element(By.NAME, 'max_patients_per_slot')
            max_patients_per_slot_input.send_keys('1')
            sleep(1)  # Thêm khoảng chờ 1 giây

            max_treatment_per_slot_input = driver.find_element(By.NAME, 'max_treatment_per_slot')
            max_treatment_per_slot_input.send_keys('3')
            sleep(1)  # Thêm khoảng chờ 1 giây


            # Gửi form thêm phòng khám
            save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Thêm phòng khám')]")
            save_button.click()

            # Chờ trang danh sách phòng khám tải hoàn toàn sau khi gửi form
            clinic_list_page_loaded = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Danh sách phòng khám của bạn')]"))
            )

            # Kiểm tra xem trang danh sách phòng khám đã tải lại thành công
            if clinic_list_page_loaded:
                self.assertTrue(clinic_list_page_loaded.is_displayed())
            else:
                self.fail("Clinic list page not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

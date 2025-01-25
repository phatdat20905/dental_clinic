import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request

class EditClinicTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
      
    def tearDown(self):
        self.driver.quit()

    def test_edit_clinic(self):
        """
        Test the edit clinic functionality with valid data.
        This test performs the following steps:
        1. Opens the login page and logs in.
        2. Opens the my clinics page.
        3. Clicks on the "Sửa" button to go to the edit clinic page.
        4. Fills in the clinic form with valid data.
        5. Submits the clinic form.
        6. Verifies that the my clinics page is displayed again.
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

        # Chờ và bấm vào nút "Sửa"
        edit_clinic_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Sửa')]"))
        )
        edit_clinic_button.click()

        # Chờ trang sửa phòng khám tải hoàn toàn
        form_loaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'clinic_name'))
        )

        if form_loaded:
            # Điền thông tin phòng khám
            clinic_name_input = driver.find_element(By.NAME, 'clinic_name')
            driver.execute_script("arguments[0].value='Phòng Khám Nha Khoa Kim';", clinic_name_input)
            sleep(1)  # Thêm khoảng chờ 1 giây

            address_input = driver.find_element(By.NAME, 'address')
            driver.execute_script("arguments[0].value='150 – 152 Hai Bà Trưng, P.Đa Kao, Q.1, TP.HCM';", address_input)
            sleep(1)  # Thêm khoảng chờ 1 giây

            phone_number_input = driver.find_element(By.NAME, 'phone_number')
            driver.execute_script("arguments[0].value='0373684800';", phone_number_input)
            sleep(1)  # Thêm khoảng chờ 1 giây

            opening_hours_input = driver.find_element(By.NAME, 'opening_hours')
            driver.execute_script("arguments[0].value='8am - 10pm';", opening_hours_input)
            sleep(1)  # Thêm khoảng chờ 1 giây

            max_patients_per_slot_input = driver.find_element(By.NAME, 'max_patients_per_slot')
            driver.execute_script("arguments[0].value='1';", max_patients_per_slot_input)
            sleep(1)  # Thêm khoảng chờ 1 giây

            max_treatment_per_slot_input = driver.find_element(By.NAME, 'max_treatment_per_slot')
            driver.execute_script("arguments[0].value='3';", max_treatment_per_slot_input)
            sleep(1)  # Thêm khoảng chờ 1 giây

            slot_duration_minutes_input = driver.find_element(By.NAME, 'slot_duration_minutes')
            driver.execute_script("arguments[0].value='45';", slot_duration_minutes_input)
            sleep(1)  # Thêm khoảng chờ 1 giây

            # Gửi form sửa phòng khám
            save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Lưu thay đổi')]")
            driver.execute_script("arguments[0].click();", save_button)

            # Chờ trang danh sách phòng khám tải hoàn toàn sau khi gửi form
            clinic_list_page_loaded = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Danh sách phòng khám của bạn')]"))
            )
            sleep(2)
            # Kiểm tra xem trang danh sách phòng khám đã tải lại thành công
            if clinic_list_page_loaded:
                self.assertTrue(clinic_list_page_loaded.is_displayed())
            else:
                self.fail("Clinic list page not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

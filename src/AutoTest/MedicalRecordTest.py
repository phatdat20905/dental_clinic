import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class MedicalRecordTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
      
    def tearDown(self):
        self.driver.quit()

    def test_add_medical_record(self):
        """
        Test the add medical record functionality with valid data.
        This test performs the following steps:
        1. Opens the login page and logs in.
        2. Opens the appointment schedule page.
        3. Clicks on the "Hoàn thành" button to go to the medical record page.
        4. Fills in the medical record form with valid data.
        5. Submits the medical record form.
        6. Verifies that the success message or redirect occurs.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")

        # Đăng nhập
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("tranthinga@gmail.com")
        password_input.send_keys("123456")
        password_input.send_keys(Keys.RETURN)

        # Chờ trang tải hoàn toàn
        sleep(3)  # Thêm khoảng chờ 3 giây

        # Mở trang lịch hẹn
        driver.get("http://127.0.0.1:8000/manage/appointment_schedule/")

        # Chờ và bấm vào nút "Hoàn thành"
        complete_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Hoàn thành')]"))
        )
        complete_button.click()

        # Chờ trang nhập kết quả khám tải hoàn toàn
        form_loaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'dentist_notes'))
        )

        if form_loaded:
            # Điền form nhập kết quả khám
            dentist_notes_input = driver.find_element(By.NAME, 'dentist_notes')
            dentist_notes_input.send_keys('Ghi chú của nha sĩ')

            diagnosis_input = driver.find_element(By.NAME, 'diagnosis')
            diagnosis_input.send_keys('Chẩn đoán bệnh lý')

            treatment_plan_input = driver.find_element(By.NAME, 'treatment_plan')
            treatment_plan_input.send_keys('Kế hoạch điều trị')

            medication_input = driver.find_element(By.NAME, 'medication')
            medication_input.send_keys('Thuốc kê đơn')

            follow_up_date_input = driver.find_element(By.NAME, 'follow_up_date')
            follow_up_date_input.send_keys('02/25/2025')

            # Thêm khoảng chờ trước khi gửi form
            sleep(2)  # Chờ thêm 2 giây

            # Gửi form nhập kết quả khám
            save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Lưu kết quả')]")
            save_button.click()

            # Chờ trang lịch hẹn tải hoàn toàn sau khi gửi form
            schedule_loaded = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Lịch hẹn')]"))
            )

            # Kiểm tra xem trang lịch hẹn đã tải lại thành công
            if schedule_loaded:
                self.assertTrue(schedule_loaded.is_displayed())
            else:
                self.fail("Appointment schedule page not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

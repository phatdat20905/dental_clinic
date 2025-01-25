import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AddScheduleTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
      
    def tearDown(self):
        self.driver.quit()

    def test_add_schedule(self):
        """
        Test the add schedule functionality with valid data.
        This test performs the following steps:
        1. Opens the login page and logs in.
        2. Opens the my clinics page.
        3. Clicks on the "Lịch làm việc" button to go to the clinic schedule page.
        4. Clicks on the "Thêm lịch làm việc" button to go to the add schedule page.
        5. Fills in the schedule form with valid data.
        6. Submits the schedule form.
        7. Verifies that the clinic schedule page is displayed again.
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

        # Chờ và bấm vào nút "Lịch làm việc"
        schedule_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Lịch làm việc')]"))
        )
        schedule_button.click()

        # Chờ trang lịch làm việc tải hoàn toàn
        schedule_page_loaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Thêm lịch làm việc')]"))
        )

        if schedule_page_loaded:
            # Bấm vào nút "Thêm lịch làm việc"
            add_schedule_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Thêm lịch làm việc')]")
            add_schedule_button.click()

            # Chờ trang thêm lịch làm việc tải hoàn toàn
            form_loaded = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'day'))
            )

            if form_loaded:
                # Điền form thêm lịch làm việc
                day_input = driver.find_element(By.NAME, 'day')
                day_input.send_keys('02/25/2025')

                time_input = driver.find_element(By.NAME, 'time')
                time_input.send_keys('08:00 - 08:45')

                dentist_select = driver.find_element(By.NAME, 'dentist')
                dentist_select.send_keys('Trần Thị Nga')  # Thay thế bằng tên nha sĩ thực tế

                # Gửi form thêm lịch làm việc
                save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Thêm lịch làm việc')]")
                save_button.click()

                # Chờ trang lịch làm việc tải hoàn toàn sau khi gửi form
                schedule_page_loaded_again = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Lịch làm việc của phòng khám:')]"))
                )
                sleep(3)

                # Kiểm tra xem trang lịch làm việc đã tải lại thành công
                if schedule_page_loaded_again:
                    self.assertTrue(schedule_page_loaded_again.is_displayed())
                else:
                    self.fail("Clinic schedule page not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

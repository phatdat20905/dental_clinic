# import unittest
# from time import sleep
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# class AppointmentTest(unittest.TestCase):
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.maximize_window()
      
#     def tearDown(self):
#         self.driver.quit()

#     def test_book_appointment_success(self):
#         """
#         Test the booking appointment functionality with valid data.
#         This test performs the following steps:
#         1. Opens the login page and logs in.
#         2. Clicks on the "Đặt lịch" button to go to the clinic booking page.
#         3. Fills in the booking form with valid data.
#         4. Submits the booking form.
#         5. Verifies that the success message is displayed or the failure message if already booked.
#         """
#         driver = self.driver
#         driver.get("http://127.0.0.1:8000/login/")

#         # Đăng nhập
#         email_input = driver.find_element(By.NAME, "email")
#         password_input = driver.find_element(By.NAME, "password")
#         email_input.send_keys("ngophatdat80@gmail.com")
#         password_input.send_keys("123456")
#         password_input.send_keys(Keys.RETURN)

#         # Chờ trang tải hoàn toàn
#         sleep(3)  # Thêm khoảng chờ 3 giây

#         # Mở trang hồ sơ người dùng
#         driver.get("http://127.0.0.1:8000/clinic/nha-khoa-kim")  # Thay thế bằng URL thực tế của trang hồ sơ người dùng

#         # Chờ trang có form đặt lịch tải hoàn toàn
#         form_loaded = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.NAME, 'clinic'))
#         )

#         if form_loaded:
#             # Điền form đặt lịch hẹn
#             clinic_select = driver.find_element(By.NAME, 'clinic')
#             clinic_select.send_keys('Phòng Khám Nha Khoa Kim')  # Thay thế bằng tên phòng khám thực tế

#             dentist_select = driver.find_element(By.NAME, 'dentist')
#             dentist_select.send_keys('Trần Thị Nga')  # Thay thế bằng tên bác sĩ thực tế

#             service_select = driver.find_element(By.NAME, 'service')
#             service_select.send_keys('Niềng răng')  # Thay thế bằng tên dịch vụ thực tế

#             date_input = driver.find_element(By.NAME, 'date')
#             date_input.send_keys('01/22/2025')

#             # Chọn thời gian từ danh sách thả xuống
#             time_select = driver.find_element(By.NAME, 'time')
#             time_select.click()
#             time_option = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//option[@value='08:00-08:45']")))
#             time_option.click()

#             name_input = driver.find_element(By.NAME, 'name')
#             name_input.send_keys('Ngô Phát Đạt')

#             phone_input = driver.find_element(By.NAME, 'phone')
#             phone_input.send_keys('0123456789')

#             address_input = driver.find_element(By.NAME, 'address')
#             address_input.send_keys('Địa chỉ 1')

#             # Gửi form
#             address_input.send_keys(Keys.RETURN)

#             # Chờ và kiểm tra kết quả
#             try:
#                 success_message = WebDriverWait(driver, 20).until(
#                     EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Đặt lịch thành công!')]"))
#                 )
#                 self.assertTrue(success_message.is_displayed())
#                 self.assertIn("Đặt lịch thành công!", success_message.text)
#             except TimeoutException:
#                 try:
#                     failure_message = WebDriverWait(driver, 20).until(
#                         EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Đặt lịch hẹn thất bại')]"))
#                     )
#                     self.assertTrue(failure_message.is_displayed())
#                     self.assertIn("Đặt lịch hẹn thất bại", failure_message.text)
#                 except TimeoutException:
#                     self.fail("Neither success nor failure message displayed within the time limit")

#     def test_book_appointment_with_missing_data(self):
#         """
#         Test the booking appointment functionality with missing data.
#         This test performs the following steps:
#         1. Opens the login page and logs in.
#         2. Clicks on the "Đặt lịch" button to go to the clinic booking page.
#         3. Leaves some fields empty in the booking form.
#         4. Submits the booking form.
#         5. Verifies that the error message is displayed.
#         """
#         driver = self.driver
#         driver.get("http://127.0.0.1:8000/login/")

#         # Đăng nhập
#         email_input = driver.find_element(By.NAME, "email")
#         password_input = driver.find_element(By.NAME, "password")
#         email_input.send_keys("ngophatdat80@gmail.com")
#         password_input.send_keys("123456")
#         password_input.send_keys(Keys.RETURN)

#         # Chờ trang tải hoàn toàn
#         sleep(3)  # Thêm khoảng chờ 3 giây

#         # Mở trang hồ sơ người dùng
#         driver.get("http://127.0.0.1:8000/clinic/nha-khoa-kim")  # Thay thế bằng URL thực tế của trang hồ sơ người dùng

#         # Chờ trang có form đặt lịch tải hoàn toàn
#         form_loaded = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.NAME, 'clinic'))
#         )

#         if form_loaded:
#             # Điền form đặt lịch hẹn với dữ liệu thiếu
#             clinic_select = driver.find_element(By.NAME, 'clinic')
#             clinic_select.send_keys('Phòng Khám Nha Khoa Kim')  # Thay thế bằng tên phòng khám thực tế

#             dentist_select = driver.find_element(By.NAME, 'dentist')
#             dentist_select.send_keys('Trần Thị Nga')  # Thay thế bằng tên bác sĩ thực tế

#             service_select = driver.find_element(By.NAME, 'service')
#             service_select.send_keys('Niềng răng')  # Thay thế bằng tên dịch vụ thực tế

#             # Bỏ qua các trường date và time

#             name_input = driver.find_element(By.NAME, 'name')
#             name_input.send_keys('Ngô Phát Đạt')

#             phone_input = driver.find_element(By.NAME, 'phone')
#             phone_input.send_keys('0123456789')

#             address_input = driver.find_element(By.NAME, 'address')
#             address_input.send_keys('Địa chỉ 1')

#             # Gửi form
#             address_input.send_keys(Keys.RETURN)

#             # Chờ và kiểm tra thông báo lỗi
#             try:
#                 error_message = WebDriverWait(driver, 20).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, ".error"))
#                 )
#                 self.assertTrue(error_message.is_displayed())
#                 self.assertIn("This field is required.", error_message.text)
#             except TimeoutException:
#                 self.fail("Error message not displayed within the time limit")

# if __name__ == "__main__":
#     unittest.main()
import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class AppointmentTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
      
    def tearDown(self):
        self.driver.quit()

    def test_book_appointment_success(self):
        """
        Test the booking appointment functionality with valid data.
        This test performs the following steps:
        1. Opens the login page and logs in.
        2. Clicks on the "Đặt lịch" button to go to the clinic booking page.
        3. Fills in the booking form with valid data.
        4. Submits the booking form.
        5. Verifies that the success message is displayed or the failure message if already booked.
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

        # Chờ đăng nhập xong và bấm vào nút "Đặt lịch"
        dat_lich_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Đặt lịch"))
        )
        dat_lich_button.click()

        sleep(2)
        # Điền form đặt lịch hẹn
        clinic_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'clinic')))
        clinic_select.send_keys('Phòng Khám Nha Khoa Kim')  # Thay thế bằng tên phòng khám thực tế

        dentist_select = driver.find_element(By.NAME, 'dentist')
        dentist_select.send_keys('Trần Thị Nga')  # Thay thế bằng tên bác sĩ thực tế

        service_select = driver.find_element(By.NAME, 'service')
        service_select.send_keys('Niềng răng')  # Thay thế bằng tên dịch vụ thực tế

        date_input = driver.find_element(By.NAME, 'date')
        date_input.send_keys('01/22/2025')

        # Chọn thời gian từ danh sách thả xuống
        # time_select = driver.find_element(By.NAME, 'time')
        # time_select.click()
        # time_option = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//option[@value='08:00-08:45']")))
        # time_option.click()
        
        time_select = driver.find_element(By.NAME, 'time')
        time_select.send_keys('08:00-08:45')  # Thay thế bằng tên bác sĩ thực tế

        name_input = driver.find_element(By.NAME, 'name')
        name_input.send_keys('Ngô Phát Đạt')

        phone_input = driver.find_element(By.NAME, 'phone')
        phone_input.send_keys('0123456789')

        address_input = driver.find_element(By.NAME, 'address')
        address_input.send_keys('Địa chỉ 1')

        # Gửi form
        address_input.send_keys(Keys.RETURN)

        # Chờ và kiểm tra kết quả
        try:
            success_message = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Đặt lịch thành công!')]"))
            )
            sleep(2)
            self.assertTrue(success_message.is_displayed())
            self.assertIn("Đặt lịch thành công!", success_message.text)
        except TimeoutException:
            try:
                failure_message = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Đặt lịch hẹn thất bại')]"))
                )
                sleep(2)
                self.assertTrue(failure_message.is_displayed())
                self.assertIn("Đặt lịch hẹn thất bại", failure_message.text)
            except TimeoutException:
                self.fail("Neither success nor failure message displayed within the time limit")

    def test_book_appointment_with_missing_data(self):
        """
        Test the booking appointment functionality with missing data.
        This test performs the following steps:
        1. Opens the login page and logs in.
        2. Clicks on the "Đặt lịch" button to go to the clinic booking page.
        3. Leaves some fields empty in the booking form.
        4. Submits the booking form.
        5. Verifies that the error message is displayed.
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

        # Chờ đăng nhập xong và bấm vào nút "Đặt lịch"
        dat_lich_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Đặt lịch"))
        )
        dat_lich_button.click()

        # Điền form đặt lịch hẹn với dữ liệu thiếu
        clinic_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'clinic')))
        clinic_select.send_keys('Phòng Khám Nha Khoa Kim')  # Thay thế bằng tên phòng khám thực tế

        dentist_select = driver.find_element(By.NAME, 'dentist')
        dentist_select.send_keys('Trần Thị Nga')  # Thay thế bằng tên bác sĩ thực tế

        service_select = driver.find_element(By.NAME, 'service')
        service_select.send_keys('Niềng răng')  # Thay thế bằng tên dịch vụ thực tế

        # Bỏ qua các trường date và time

        name_input = driver.find_element(By.NAME, 'name')
        name_input.send_keys('Ngô Phát Đạt')

        phone_input = driver.find_element(By.NAME, 'phone')
        phone_input.send_keys('0123456789')

        address_input = driver.find_element(By.NAME, 'address')
        address_input.send_keys('Địa chỉ 1')

        # Gửi form
        address_input.send_keys(Keys.RETURN)

        # Chờ và kiểm tra thông báo lỗi
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

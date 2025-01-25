import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request

class AddDentistTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
      
    def tearDown(self):
        self.driver.quit()

    def test_add_dentist(self):
        """
        Test the add dentist functionality with valid data.
        This test performs the following steps:
        1. Opens the login page and logs in.
        2. Opens the my clinics page.
        3. Clicks on the "Danh sách nha sĩ" button to go to the dentist list page.
        4. Clicks on the "Thêm nha sĩ" button to go to the add dentist page.
        5. Fills in the dentist form with valid data.
        6. Submits the dentist form.
        7. Verifies that the dentist list page is displayed again.
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

        # Chờ và bấm vào nút "Danh sách nha sĩ"
        dentist_list_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Danh sách nha sĩ')]"))
        )
        dentist_list_button.click()

        # Chờ trang danh sách nha sĩ tải hoàn toàn
        dentist_list_page_loaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Thêm nha sĩ')]"))
        )

        if dentist_list_page_loaded:
            # Bấm vào nút "Thêm nha sĩ"
            add_dentist_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Thêm nha sĩ')]")
            add_dentist_button.click()

            # Chờ trang thêm nha sĩ tải hoàn toàn
            form_loaded = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'email'))
            )

            if form_loaded:
                # Điền thông tin tài khoản
                email_input = driver.find_element(By.NAME, 'email')
                email_input.send_keys('nguyenvanc@example.com')

                full_name_input = driver.find_element(By.NAME, 'full_name')
                full_name_input.send_keys('Nguyễn Văn C')

                gender_select = driver.find_element(By.NAME, 'gender')
                gender_select.send_keys('Nam')

                phone_number_input = driver.find_element(By.NAME, 'phone_number')
                phone_number_input.send_keys('0937364012')

                address_input = driver.find_element(By.NAME, 'address')
                address_input.send_keys('Hồ Chí Minh')

                password1_input = driver.find_element(By.NAME, 'password1')
                password1_input.send_keys('123456')

                password2_input = driver.find_element(By.NAME, 'password2')
                password2_input.send_keys('123456')
                sleep(1)  # Thêm khoảng chờ 1 giây

                # Điền thông tin chuyên môn
                specialization_input = driver.find_element(By.NAME, 'specialization')
                specialization_input.send_keys('Nha Khoa')

                position_input = driver.find_element(By.NAME, 'position')
                position_input.send_keys('Thạc sĩ')

                experience_years_input = driver.find_element(By.NAME, 'experience_years')
                experience_years_input.send_keys('10')


                # Gửi form thêm nha sĩ
                save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Thêm')]")
                driver.execute_script("arguments[0].click();", save_button)

                # Chờ trang danh sách nha sĩ tải hoàn toàn sau khi gửi form
                dentist_list_page_loaded_again = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Danh sách nha sĩ của phòng khám')]"))
                )

                # Kiểm tra xem trang danh sách nha sĩ đã tải lại thành công
                if dentist_list_page_loaded_again:
                    self.assertTrue(dentist_list_page_loaded_again.is_displayed())
                else:
                    self.fail("Dentist list page not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

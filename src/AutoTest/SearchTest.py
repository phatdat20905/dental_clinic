import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class SearchTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
      
    def tearDown(self):
        self.driver.quit()

    def test_search_with_results(self):
        """
        Test the search functionality with valid data.
        This test performs the following steps:
        1. Opens the search page.
        2. Enters search data into the search field.
        3. Submits the search form.
        4. Verifies that the search results page is displayed.
        5. Verifies the results for clinics, dentists, and services.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")

        # Chờ trang tải hoàn toàn
        sleep(2)  # Thêm khoảng chờ 2 giây

        # Nhập dữ liệu vào trường tìm kiếm
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_input.send_keys('Phòng Khám Nha Khoa Kim')  # Thay thế bằng dữ liệu tìm kiếm thực tế

        # Bấm nút "Tìm kiếm"
        search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Tìm kiếm')]")
        search_button.click()

        # Chờ trang kết quả tìm kiếm tải hoàn toàn
        search_results_loaded = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.clinic-container, div.dentist-container, div.services-container'))
        )

        # Kiểm tra kết quả tìm kiếm cho phòng khám
        try:
            clinic_results = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.clinic-container'))
            )
            self.assertTrue(clinic_results.is_displayed())
        except TimeoutException:
            pass

        # Kiểm tra kết quả tìm kiếm cho nha sĩ
        try:
            dentist_results = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.dentist-container'))
            )
            self.assertTrue(dentist_results.is_displayed())
        except TimeoutException:
            pass

        # Kiểm tra kết quả tìm kiếm cho dịch vụ
        try:
            service_results = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.services-container'))
            )
            self.assertTrue(service_results.is_displayed())
        except TimeoutException:
            pass

    def test_search_no_results(self):
        """
        Test the search functionality with no results.
        This test performs the following steps:
        1. Opens the search page.
        2. Enters search data that yields no results into the search field.
        3. Submits the search form.
        4. Verifies that the no results message is displayed.
        """
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")

        # Chờ trang tải hoàn toàn
        sleep(2)  # Thêm khoảng chờ 2 giây

        # Nhập dữ liệu vào trường tìm kiếm
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'q'))
        )
        search_input.send_keys('Không có kết quả')  # Thay thế bằng dữ liệu tìm kiếm không có kết quả thực tế

        # Bấm nút "Tìm kiếm"
        search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Tìm kiếm')]")
        search_button.click()

        # Chờ trang kết quả tìm kiếm tải hoàn toàn
        try:
            no_results = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Không tìm thấy kết quả phù hợp.')]"))
            )
            sleep(2)
            self.assertTrue(no_results.is_displayed())
        except TimeoutException:
            self.fail("No results message not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

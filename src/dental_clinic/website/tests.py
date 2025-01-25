# from django.contrib.auth import get_user_model
# from django.test import TestCase


# class UsersManagersTests(TestCase):

#     def test_create_user(self):
#         User = get_user_model()
#         user = User.objects.create_user(email="normal@user.com", password="foo")
#         self.assertEqual(user.email, "normal@user.com")
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(TypeError):
#             User.objects.create_user()
#         with self.assertRaises(TypeError):
#             User.objects.create_user(email="")
#         with self.assertRaises(ValueError):
#             User.objects.create_user(email="", password="foo")

#     def test_create_superuser(self):
#         User = get_user_model()
#         admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
#         self.assertEqual(admin_user.email, "super@user.com")
#         self.assertTrue(admin_user.is_active)
#         self.assertTrue(admin_user.is_staff)
#         self.assertTrue(admin_user.is_superuser)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(admin_user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(ValueError):
#             User.objects.create_superuser(
#                 email="super@user.com", password="foo", is_superuser=False)

import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from django.test import LiveServerTestCase
from models import Clinic, Dentist, Service

class AppointmentTestCase(LiveServerTestCase):
    def setUp(self):
        # Sử dụng dữ liệu có sẵn trong database
        self.clinic = Clinic.objects.first()
        self.dentist = Dentist.objects.first()
        self.service = Service.objects.first()

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()

    def test_book_appointment_success(self):
        """
        Kiểm tra chức năng đặt lịch hẹn thành công.
        """
        driver = self.driver
        driver.get(self.live_server_url + '/login/')

        # Đăng nhập
        email_input = driver.find_element(By.NAME, "email")
        password_input = driver.find_element(By.NAME, "password")
        email_input.send_keys("ngophatdat80@gmail.com")
        password_input.send_keys("123456")
        password_input.send_keys(Keys.RETURN)

        # Chờ đăng nhập xong và chuyển hướng đến trang đặt lịch hẹn
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Đặt lịch hẹn")))
        driver.get(self.live_server_url + f'/clinic/{self.clinic.slug}/')

        # Điền form đặt lịch hẹn
        clinic_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'clinic')))
        clinic_select.send_keys(self.clinic.clinic_name)

        dentist_select = driver.find_element(By.NAME, 'dentist')
        dentist_select.send_keys(self.dentist.dentist.full_name)

        service_select = driver.find_element(By.NAME, 'service')
        service_select.send_keys(self.service.service_name)

        date_input = driver.find_element(By.NAME, 'date')
        date_input.send_keys('2023-05-01')

        time_select = driver.find_element(By.NAME, 'time')
        time_select.send_keys('09:00')

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
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'message'))
            )
            self.assertTrue(success_message.is_displayed())
            self.assertIn("Đặt lịch hẹn thành công!", success_message.text)
        except TimeoutException:
            self.fail("Success message not displayed within the time limit")

if __name__ == "__main__":
    unittest.main()

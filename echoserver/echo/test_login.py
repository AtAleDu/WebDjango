from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        print(f"Пользователь создан: {self.user.username}")

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        print(f"Пользователи в базе данных: {User.objects.all()}")
        self.driver.get(f"{self.live_server_url}/login/")

        # Вводим логин и пароль
        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword123')

        # Вводим капчу (если она есть)
        captcha_input = self.driver.find_element(By.NAME, "captcha_1")
        captcha_input.send_keys('PASSED')

        # Нажимаем кнопку "Войти"
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()

        # Ожидание появления сообщения "Вы вошли как"
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Вы вошли как')]"))
            )
            print("Сообщение 'Вы вошли как' найдено.")
        except Exception as e:
            print(f"Ошибка: {e}")
            print(f"Текущий HTML: {self.driver.page_source}")  # Отладочный вывод

        # Проверяем, что пользователь успешно авторизовался
        self.assertIn("Вы вошли как", self.driver.page_source)
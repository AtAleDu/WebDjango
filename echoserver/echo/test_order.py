from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from .models import Book

class BookListTest(LiveServerTestCase):
    def setUp(self):
        # Настройка драйвера Selenium
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

        # Создаем несколько тестовых книг
        self.book1 = Book.objects.create(
            title='1984',
            author='Джордж Оруэлл',
            price=10.99
        )
        self.book2 = Book.objects.create(
            title='Мастер и Маргарита',
            author='Михаил Булгаков',
            price=12.99
        )

    def tearDown(self):
        # Закрываем браузер после завершения теста
        self.driver.quit()

    def test_book_list_display(self):
        # Переходим на главную страницу
        self.driver.get(self.live_server_url)

        # Проверяем, что книги отображаются на странице
        self.assertIn('1984', self.driver.page_source)
        self.assertIn('Джордж Оруэлл', self.driver.page_source)
        self.assertIn('10.99 руб.', self.driver.page_source)

        self.assertIn('Мастер и Маргарита', self.driver.page_source)
        self.assertIn('Михаил Булгаков', self.driver.page_source)
        self.assertIn('12.99 руб.', self.driver.page_source)
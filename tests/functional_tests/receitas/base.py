import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from receitas.utils.browser import make_chrome_browser


class RecipeBaseFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser('--headless')
        return super().setUp()
    
    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self,seconds=3):
        time.sleep(seconds)
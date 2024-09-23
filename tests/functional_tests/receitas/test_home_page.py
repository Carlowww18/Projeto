import pytest
from selenium.webdriver.common.by import By
from .base import RecipeBaseFunctionalTest

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_the_test(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('', body.text)
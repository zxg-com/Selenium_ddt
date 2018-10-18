



from src.common import Base_page
from appium.webdriver.common import mobileby

class initPage(Base_page.Base_page):
    by=mobileby.By
    skip_btn=(by.ID,'com.allin.social:id/kn')

    def click_skip(self):
        self.click_button(*self.skip_btn)
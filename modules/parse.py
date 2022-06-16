import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from modules.util import NormalizePhoneNumber


class GetCompanies:
    def __init__(self, browser, query):
        browser.implicitly_wait(15)

        action = ActionChains(browser)

        url = "https://yandex.ru/maps/213/moscow/"

        browser.get(url)

        input_field = browser.find_element_by_class_name("input__control")
        button = browser.find_element_by_class_name(
            "small-search-form-view__button")
        input_field.send_keys(query)
        button.click()
        try:
            inside = browser.find_element_by_class_name("_name_inside")

            inside.click()

            company_area = browser.find_element_by_class_name(
                "card-businesses-list__list"
            )
            links = company_area.find_elements_by_class_name(
                "search-snippet-view__link-overlay"
            )
            companies = []
            while True:
                previous_len = len(companies)
                action.move_to_element(links[-1]).perform()

                time.sleep(1)

                links = company_area.find_elements_by_class_name(
                    "search-snippet-view__link-overlay"
                )
                for link in links:
                    link_href = link.get_attribute("href")
                    if link_href not in companies:
                        companies.append(link_href)
                current_len = len(companies)

                if current_len == previous_len:
                    break

            self.results = companies

        except NoSuchElementException:
            print("Организации в здании отсутствуют!")
            self.results = []


class GetCompanyData:
    def __init__(self, browser, company_link):
        def reveal_phone():
            try:
                phone_div = browser.find_element_by_class_name("card-phones-view__more")
                phone_div.click()
            except NoSuchElementException:
                return False
            return True

        def get_name():
            return browser.find_element_by_tag_name("h1").text

        def get_type():
            try:
                features_div = browser.find_element_by_class_name(
                    "business-features-view"
                )
            except NoSuchElementException:
                return "Другое"

            btn_texts = []

            features = features_div.find_elements_by_class_name("button__text")

            for feature in features:
                btn_texts.append(feature.text)

            return btn_texts[0]

        def get_phone():
            phone_unformatted = browser.find_element_by_class_name(
                "orgpage-phones-view__phone-number"
            ).text
            phone_formatted = NormalizePhoneNumber(phone_unformatted).normalize
            return phone_formatted

        def get_website():
            try:
                return browser.find_element_by_class_name(
                    "business-urls-view__link"
                ).get_attribute("href")
            except NoSuchElementException:
                return None

        browser.implicitly_wait(2)

        browser.get(company_link)
        print(company_link)

        name = get_name()
        company_type = get_type()

        if reveal_phone() is True:
            phone = get_phone()
        else:
            phone = None

        website = get_website()

        print(name)

        if phone is not None:
            self.data = dict(
                link=company_link,
                name=name,
                type=company_type,
                phone=phone,
                website=website
            )
        else:
            self.data = None

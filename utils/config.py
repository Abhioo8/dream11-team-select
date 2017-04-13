import contextlib
import os
import time
from ConfigParser import ConfigParser
from StringIO import StringIO

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, \
    ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Config(object):
    """
    This has the configurations to get the xpath, driver instances
    etc...
    """

    def __init__(self):
        pass

    @staticmethod
    def load_xpath(path='utils/configs/xpath.properties'):
        """
        This gives the configparser object that can be used to
        manipulate with it's methods
        :param: path: str
        :return: configparser
        """
        config = StringIO()
        config.write('[dummysection]\n')  # add dummy section to avoid MissingSection exception
        config.write(open(path).read())
        config.seek(0, os.SEEK_SET)

        cp = ConfigParser()
        cp.readfp(config)
        return cp

    def get_xpath(self, key):
        """
        This gives the xpath corresponding to the given key
        :param: key: str
        :param: str
        """
        return self.load_xpath().get('dummysection', key)

    @staticmethod
    def get_driver_instance(driver="firefox"):
        """
        This function returns the driver instance
        :param driver:
        :return: webdriver
        """
        # user_agent = UserAgentRotator().get_user_agent()
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" \
                     "(KHTML, like Gecko) Ubuntu Chromium/56.0.2924.76 Chrome/56.0.2924.76 " \
                     "Safari/537.36"
        if "phantom" in driver:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = user_agent
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            return driver

        elif "chrome" in driver:
            options = webdriver.ChromeOptions()
            options.add_argument("--user-agent={0}".format(user_agent))
            options.add_extension("utils/ad_block_1.13.2.crx")
            driver = webdriver.Chrome(chrome_options=options)
            return driver

        # ################ Firefox #################################
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        driver = webdriver.Firefox(profile)
        return driver

    @staticmethod
    def click_element(driver, xpath):
        """
        This clicks the WebElement found by given xpath
        :param: driver: webdriver
        :param: xpath: str
        """
        try:
            WebDriverWait(driver, 30, poll_frequency=1).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            driver.find_element_by_xpath(xpath).click()
        except TimeoutException:
            time.sleep(5)
            driver.find_element_by_xpath(xpath).click()
        except NoSuchElementException:
            raise NoSuchElementException("Element not present with the given xpath")
        except StaleElementReferenceException:
            time.sleep(5)
            driver.find_element_by_xpath(xpath).click()
            Config.wait_for_page_load(driver)
        except ElementNotVisibleException:
            pass

    @staticmethod
    def send_keys(driver, xpath, keys):
        """
        This inputs keys into the WebElement found by given xpath
        :param: driver: webdriver
        :param: xpath: str
        :param: keys: str
        """
        try:
            WebDriverWait(driver, 30, poll_frequency=1).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            ele = driver.find_element_by_xpath(xpath)
            ele.clear()
            ele.send_keys(keys)
        except TimeoutException:
            time.sleep(5)
            ele = driver.find_element_by_xpath(xpath)
            ele.clear()
            ele.send_keys(keys)
        except NoSuchElementException:
            raise NoSuchElementException("Element not present with the given xpath")

    @staticmethod
    def wait_for_element(driver, xpath):
        """
        This wait for the element to be loaded
        :param: driver: webdriver
        :param: xpath: str
        :param: keys: str
        :return: WebElement
        """
        try:
            WebDriverWait(driver, 30, poll_frequency=1).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            return driver.find_element_by_xpath(xpath)
        except TimeoutException:
            time.sleep(5)
            return driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            raise NoSuchElementException("Element not present with the given xpath")

    @staticmethod
    def wait_for_element_inside_webelement(webelement, xpath):
        """
        This is to wait for the element inside WebElement
        :param: webelement: WebElement
        :param: driver: webdriver
        :param: xpath: str
        :return: WebElement
        """
        try:
            return webelement.find_element_by_xpath(xpath)
        except TimeoutException:
            time.sleep(5)
            return webelement.find_element_by_xpath(xpath)
        except NoSuchElementException:
            raise NoSuchElementException(
                "Element not present with the given xpath")
        except StaleElementReferenceException:
            time.sleep(5)
            ele = webelement.find_element_by_xpath(xpath)
            return ele

    @staticmethod
    def wait_for_elements(driver, xpath):
        """
        This is to wait for the multiple elements
        :param: driver: webdriver
        :param: xpath: str
        :param: keys: str
        :return: List[WebElement]
        """
        try:
            WebDriverWait(driver, 30, poll_frequency=1).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath)))
            list_ele = driver.find_elements_by_xpath(xpath)
            return list_ele
        except TimeoutException:
            raise TimeoutException("Timeout in finding the element")
        except NoSuchElementException:
            raise NoSuchElementException("Element not present with the given xpath")

    @staticmethod
    def wait_till_text_to_be_present(driver, xpath, text):
        """
        This is contains explicit waits that wait till the text
        present in the element found by given xpath
        :param driver: webdriver
        :param xpath: str
        :param text: str
        :return:
        """
        try:
            WebDriverWait(driver, 30, poll_frequency=1).until(EC.text_to_be_present_in_element(
                (By.XPATH, xpath), text
            ))
        except TimeoutException:
            time.sleep(5)
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            raise NoSuchElementException(
                "Element not present with the given xpath")
        except StaleElementReferenceException:
            time.sleep(5)
            driver.find_element_by_xpath(xpath)

    @staticmethod
    @contextlib.contextmanager
    def wait_till_page_load(driver, timeout=60):
        """
        A context manager that wait till the page loads completely
        :param driver: webdriver
        :param timeout: int
        :return: contextmanager
        """
        old_page = driver.find_element_by_tag_name('html')
        yield
        WebDriverWait(driver, timeout).until(EC.staleness_of(old_page))

    @staticmethod
    def wait_for_page_load(driver, timeout=60):
        """
        This ensures that the readyState of the document is complete
        which is a state in asp life cycle
        :param driver: webdriver
        :param timeout: int
        :return:
        """

        def page_has_loaded():
            page_state = driver.execute_script(
                'return document.readyState;'
            )
            return page_state == 'complete'

        def wait_for(condition_function, timeout):
            start_time = time.time()
            while time.time() < start_time + timeout:
                if condition_function():
                    return True
                else:
                    time.sleep(5)
            raise Exception(
                'Timeout in wait_for'
            )

        return wait_for(page_has_loaded, timeout)

    def click_element_by_javascript(self, driver, xpath):
        """
        This clicks the WebElement found by given xpath
        :param: driver: webdriver
        :param: xpath: str
        """
        try:
            WebDriverWait(driver, 30, poll_frequency=1).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            ele = driver.find_element_by_xpath(xpath)
            try:
                postback_url = ele.get_attribute('href').split(':')[1]
                driver.execute_script(postback_url)
            except AttributeError:
                self.click_element_by_javascript(driver, xpath)
        except TimeoutException:
            raise TimeoutException("Timeout in finding the element")
        except NoSuchElementException:
            raise NoSuchElementException(
                "Element not present with the given xpath")
        except StaleElementReferenceException:
            time.sleep(5)
            self.click_element_by_javascript(driver, xpath)

    def get_text_from_element(self, webelemet):
        text = webelemet.text
        if not text:
            text = webelemet.get_attribute('innerHTML')
        return text

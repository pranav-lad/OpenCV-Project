import json
import logging
import os
import sys
from time import sleep
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Browser:
    proxies = None
    driver = None
    display = None
    headless_mode = True
    perfomance_log = False

    def __init__(self, headless_mode=True, proxies=None, perfomance_log=False):
        """
        Initiation of the class
            :param self: 
            :param headless_mode=True: Are we going to use selenium without display?
            :param proxies={}: Proxies for the browser
            :param perfomance_log=False: Are we going to use perfomance log?
        """
        if proxies is not None:
            self.proxies = proxies
        self.headless_mode = headless_mode
        self.perfomance_log = perfomance_log

    def __del__(self):
        self.stop()

    def start(self):
        """
        Start the browser
            :param self: 
        """
        if not self.driver:
            logging.debug('Starting the browser')
            if 'darwin' in sys.platform:
                chrome_drive_path = 'drivers/mac/chromedriver'
            elif 'win' in sys.platform:
                chrome_drive_path = 'drivers/windows/chromedriver.exe'
            else:
                chrome_drive_path = 'drivers/linux/chromedriver'
            try:
                if self.headless_mode is False:
                    # suppose there is no display on linux machine, but we need it
                    if 'linux' in chrome_drive_path:
                        self.display = Display(visible=0, size=(1200, 600))
                        self.display.start()
                cd = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
                chrome_drive_path = '{0}/{1}'.format(cd, chrome_drive_path)
                options = webdriver.ChromeOptions()
                options.add_experimental_option('prefs', {'profile.managed_default_content_settings.images':2})
                if self.headless_mode:
                    options.add_argument('--headless')
                if self.proxies is not None:
                    options.add_argument('--proxy-server=%s' % self.proxies)
                options.add_argument('disable-infobars')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-extensions')
                if self.perfomance_log:
                    caps = DesiredCapabilities.CHROME
                    caps['loggingPrefs'] = {'performance': 'ALL'}
                    self.driver = webdriver.Chrome(chrome_drive_path, chrome_options=options, desired_capabilities=caps)
                else:
                    self.driver = webdriver.Chrome(chrome_drive_path, chrome_options=options)
            except:
                logging.error('Cannot start the browser', exc_info=True)
    
    def stop(self):
        """
        Stop the browser
            :param self: 
        """
        if self.driver is not None:
            try:
                logging.debug('Stopping the browser')
                self.driver.quit()
                if self.display is not None:
                    self.display.stop()
            except:
                logging.error('Cannot stop the browser', exc_info=True)
            self.driver = None

    def restart(self):
        """
        Restarting the browser
            :param self: 
        """
        self.stop()
        self.start()

    def get_page(self, url, pause_before_response=0):
        """
        Start the browser
            :param self: 
            :param url: Url
            :param pause_before_response=0: Wo wee need some pause before returning a page content? (sec.)
        """
        if not self.driver:
            self.start()
        try:
            self.driver.get(url)
            sleep(pause_before_response)
            return self.get_page_source()
        except:
            logging.error('Cannot get the page: {}'.format(url), exc_info=True)
            return ''

    def get_page_source(self):
        """
        Get the current page source
            :param self: 
        """
        try:
            return self.driver.page_source
        except:
            logging.error('Cannot get page source', exc_info=True)
            return ''

    def is_element_exists(self, xpath):
        """
        Check if the element exists
            :param self: 
            :param xpath: Xpath of the element to check
        """
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except:
            return False
    
    def wait_element(self, xpath, max_time=30):
        """
        Wait for the element
            :param self: 
            :param xpath: Xpath of the element to wait
            :param max_time=45: Max time to wait (sec.)
        """
        '''.'''
        i = 0
        while i < max_time:
            sleep(1)
            if self.is_element_exists(xpath):
                return True
        return False
    
    def click(self, xpath):
        """
        Click on the element
            :param self: 
            :param xpath: Xpath of the element to click
        """
        try:
            if self.is_element_exists(xpath):
                self.driver.find_element_by_xpath(xpath).click()
            else:
                logging.error('Element {} not found. Cannot click'.format(xpath))
        except:
            logging.error('Cannot click', exc_info=True)

    def send_keys(self, xpath, keys):
        """
        Send some keys to an element
            :param self: 
            :param xpath: Xpath of the element
            :param keys: Keys
        """
        try:
            if self.is_element_exists(xpath):
                self.driver.find_element_by_xpath(xpath).send_keys(keys)
            else:
                logging.error('Element {} not found. Cannot send keys'.format(xpath))
        except:
            logging.error('Cannot send keys', exc_info=True)
    
    def switch_to_frame(self, name):
        """
        Switch to a frame or to iframe
            :param self: 
            :param name: Frame element name
        """
        try:
            element = self.driver.find_element_by_xpath("//frame[@name='{0}']".format(name))
            self.driver.switch_to_frame(element)
        except:
            try:
                element = self.driver.find_element_by_xpath("//iframe[@name='{0}']".format(name))
                self.driver.switch_to_frame(element)
            except:
                logging.error('Cannot switch to frame/iframe {}'.format(name), exc_info=True)

    def scroll_down(self):
        """
        Scroll to the end of the page
            :param self: 
        """
        try:
            script = "window.scrollTo(0, document.body.scrollHeight);"
            self.driver.execute_script(script)
        except:
            logging.error('Cannot scroll down', exc_info=True)

    def save_screenshot_of_element(self, xpath, path='screenshot'):
        """
        Save screenshot of the element
            :param self: 
            :param xpath: Xpath of the element
            :param path: File path
        """
        try:
            from PIL import Image
            element = self.driver.find_element_by_xpath(xpath)
            location = element.location
            size = element.size
            self.driver.save_screenshot(path)
            im = Image.open(path)
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            im = im.crop((left, top, right, bottom))
            im.save(path)
        except:
            logging.error('Cannot save screenshot to {}'.format(path), exc_info=True)

    # CookiesLogic
    def save_cookies_to_file(self, cookies={}, name='cookies', current_cookies=False):
        """
        Save cookies dict to the file
            :param self: 
            :param cookies={}: Dict of cookies (or use current_cookies)
            :param name='cookies': File name to save
            :param current_cookies=False: Save cookies from currents session?
        """
        try:
            if current_cookies:
                cookies = self.get_session_cookies()
            cookies = json.dumps(cookies)
            with open('{}.cookies'.format(name), 'w') as the_file:
                the_file.write(cookies)
        except:
            logging.error('Cannot save cookies to file', exc_info=True)

    def get_session_cookies(self, text_mode=False):
        """
        Get cookies from the browser
            :param self:
            :param text_mode=False: Retrun cookies as text?
        """
        cookies_text = ''
        cookies_dict = {}
        try:
            for cookie in self.driver.get_cookies():
                name = cookie['name']
                value = cookie['value']
                if value == '""': value = ''
                cookies_dict[name] = value
                cookies_text += '{0}="{1}"; '.format(name, value)
            if text_mode:
                return cookies_text[:-2]
            return cookies_dict
        except:
            logging.error('Cannot get cookies', exc_info=True)
            if text_mode:
                return ''
            return {}

    def get_cookies_from_file(self, name='cookies'):
        """
        Return cookies dict from the file
            :param self: 
            :param name='cookies': File name to load
        """
        try:
            with open('{}.cookies'.format(name)) as the_file:
                cookies_text = the_file.read()
            try:
                cookies = json.loads(cookies_text)
            except:
                cookies = self.get_dict_cookies_from_text(cookies_text)
            return cookies
        except:
            logging.error('Cannot get cookies from file', exc_info=True)
            return {}

    def get_dict_cookies_from_text(self, cookies_text):
        """
        Returnt dict from cookies raw text
            :param self: 
            :param cookies_text: Raw cookies text, example: CONSENT=YES+UK.en+; SID=wgdombwvMd;
        """
        try:
            from http import cookies
            cookie = cookies.SimpleCookie()
            cookie.load(cookies_text)
            cookies = {}
            for key, morsel in cookie.items():
                cookies[key] = morsel.value
        except:
            logging.error('Cannot get cookies from raw text', exc_info=True)
            cookies = {}
        return cookies
    
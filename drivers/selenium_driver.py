import settings
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, SessionNotCreatedException, WebDriverException
from seleniumwire import webdriver as sww
from seleniumwire import undetected_chromedriver as swuc
import undetected_chromedriver as uc
from selenium.webdriver.chrome.webdriver import WebDriver
import random
import validators
from urllib import parse
from settings import PROXY_LIST


def call_selenium_driver(headless:bool=settings.USE_HEADLESS_SELENIUM, timeout:int=settings.CHROME_DRIVER_TIMEOUT,
                        no_image:bool=True, implicit_wait:float=None, log_level:int=1,
                        use_proxy:bool=False, random_proxy:bool=True,
                        disable_css:bool=settings.DISABLE_CSS_JS_SELENIUM, silent_mode=False) -> WebDriver|int|None:
    """Call selenium driver with many options. To use proxy server, provide proxy server ip address and port. With 'site_url' decide if proxy should used to call the website.
    NOTE: seleniumwire driver is slower than standard selenium webdriver. So this code only use it if there are proxies provided in the 'settings.PROXY_LIST'"""
    try:
        driver = None
        seleniumwire_options = None
        # Set undetected or standard driver option for selenium
        if settings.USE_SELENIUM_UNDETECTED:
            options = swuc.ChromeOptions()
        else:
            options = webdriver.ChromeOptions()
        # options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
        if headless:
            options.add_argument('headless')
        if no_image:
            # 2 following line both can disable image loading but first one is more common
            options.add_argument('--blink-settings=imagesEnabled=false')
            options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        options.add_argument('--ignore-certificate-errors-spki-list')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument('--disable-gpu')
        # Following 4 options are used to test if performance can get better
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-features=NetworkService")
        options.add_argument("--disable-features=VizDisplayCompositor")
        # Selenium log level
        
        options.add_argument(f"--log-level={log_level}")
        # Selenium silent mode
        if silent_mode:
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # Following 'prefs' dictionary used for disable css (supposly) and optimize the code
        # Pass the argument 1 to allow and 2 to block (We need javascript to be loaded so we set it to 1)
        if disable_css:
            prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2,
                                'plugins': 2, 'popups': 2, 'geolocation': 2,
                                'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                                'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                                'durable_storage': 2}}
            options.add_experimental_option(
                "prefs", prefs
            )
        else:
            # Atleast disable notifications
            options.add_experimental_option(
                "prefs", {"profile.default_content_setting_values.notifications": 2}
            )
        # Provide proxy server
        if use_proxy:
            if PROXY_LIST:
                if validators.url(site_url):
                    domain = parse.urlparse(site_url).netloc
                    site_url = domain.replace('www.', '')
                    print(f'USE PROXY FOR \'{site_url}\'')
                    # Pick a proxy connection randomly
                    if random_proxy:
                        proxy = random.choice(PROXY_LIST)
                    # Or pick the first proxy
                    else:
                        proxy = PROXY_LIST[0]
                    seleniumwire_options = {
                        'proxy': {
                            'http': f'http://{proxy["username"]}:{proxy["password"]}@{proxy["address"]}:{proxy["port"]}',
                            'verify_ssl': False,
                        },
                    }
        # Create Chrome driver
        if seleniumwire_options:
            if settings.USE_SELENIUM_UNDETECTED:
                driver = swuc.Chrome(options=options, seleniumwire_options=seleniumwire_options, use_subprocess=True)
            else:
                driver = sww.Chrome(options=options, seleniumwire_options=seleniumwire_options)
        else:
            if settings.USE_SELENIUM_UNDETECTED:
                driver = uc.Chrome(options=options, use_subprocess=True)
            else:
                driver = webdriver.Chrome(options=options)
        # logging.info(f'Chrome driver version: {driver.capabilities["browserVersion"]}')
        driver.set_page_load_timeout(timeout)
        # Set windows size
        driver.set_window_size(1600, 1000)
        if implicit_wait is not None:
            driver.implicitly_wait(implicit_wait)
        return driver
    except TimeoutException:
        print('Error in "driver.selenium_driver.call_selenium_driver": Chrome driver timeout')
        return -1
    except (WebDriverException, SessionNotCreatedException):
        print('Error in "driver.selenium_driver.call_selenium_driver": Chrome driver did not created')
        return 0
    except Exception as e:
        print(f'Error in "driver.selenium_driver.call_selenium_driver": {e.__str__()}')
        print('driver has not been created')
        return None

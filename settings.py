import _env


# ! database connection variables
# DB_USER = _env.DB_USER
# DB_PASSWORD = _env.DB_PASSWORD
# DB_NAME = _env.DB_NAME
# DB_HOST = _env.DB_HOST
# DB_PORT = _env.DB_PORT

# ! Selenium settings and Chrome Version (To be used in drivers and initialize chrome webdriver)
CHROME_DRIVER_TIMEOUT = _env.CHROME_DRIVER_TIMEOUT
GENERAL_IMPLICIT_WAIT = _env.GENERAL_IMPLICIT_WAIT

# * Proxy settings
PROXY_LIST = _env.PROXY_LIST

# Use Undetected selenium to bypass anti-bot processes (eg: cloudflare anti-bot plugin)
USE_SELENIUM_UNDETECTED = _env.USE_SELENIUM_UNDETECTED

# Using headless mode for selenium
USE_HEADLESS_SELENIUM = _env.USE_HEADLESS_SELENIUM
DISABLE_CSS_JS_SELENIUM = _env.DISABLE_CSS_JS_SELENIUM

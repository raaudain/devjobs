from sys import platform

if platform == "linux" or platform == "linux2":
    chrome = r"/usr/bin/chromedriver"
    firefox = r"/usr/bin/geckodriver"
elif platform == "darwin":
    chrome = r"/usr/local/bin/chromedriver"
    firefox = r"/usr/local/bin/firefox"

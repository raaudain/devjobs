from sys import platform

if platform == "linux" or platform == "linux2":
    chrome = r"/usr/bin/chromedriver"
elif platform == "darwin":
    chrome = r"/usr/local/bin/chromedriver"

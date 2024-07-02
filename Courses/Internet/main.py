from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.youtube.com/")
key = "mystring"
value = "Hellow world"
driver.execute_script(
    "window.localStorage.setItem(arguments[0], arguments[1])", key, value
)
driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

from selenium import webdriver

driver = webdriver.Firefox()
driver.get("https://www.youtube.com/")
key = "mystring"
value = "Hellow world"
# Взаимодействие с LocalStorage

driver.execute_script(
    "window.localStorage.setItem(arguments[0], arguments[1])", key, value
)
data = driver.execute_script(
    "return window.localStorage.getItem(arguments[0]);", key)
driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)
print(data, value, data == value)

# Взаимодействие с Cookie
driver.add_cookie({"name": key, "value": value})
cookie_data = driver.get_cookie(key)
driver.delete_cookie(key)

print(cookie_data, value, cookie_data.GET('value') == value)

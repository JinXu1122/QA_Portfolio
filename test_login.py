import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options

# 🌟 PROFESSIONAL UPGRADE: The Pytest Fixture
# This block runs automatically before and after EVERY test!
@pytest.fixture
def driver():
    # 1. Configure Chrome to hide annoying popups
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "safebrowsing.enabled": False
    })
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument("--headless") # Essential for CI/CD
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # 2. SETUP: Open browser and go to the site
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.saucedemo.com/")
    
    # 3. YIELD: This hands the ready-to-go browser to your test functions
    yield driver 
    
    # 4. TEARDOWN: After the test is done, this code runs to close the browser
    driver.quit()


# Notice how clean the tests are now! We just pass 'driver' into the parenthesis.
def test_successful_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    assert "inventory.html" in driver.current_url

def test_invalid_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()

    error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "Username and password do not match" in error_message

def test_empty_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("")
    driver.find_element(By.ID, "password").send_keys("")
    driver.find_element(By.ID, "login-button").click()

    error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    assert "Username is required" in error_message

def test_end_to_end_checkout(driver):
    # Login
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.ID, "inventory_container")))

    # Sort items
    sort_dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
    select = Select(sort_dropdown)
    select.select_by_value("lohi") 

    # Add to cart and checkout
    driver.find_element(By.CSS_SELECTOR, "button[data-test='add-to-cart-sauce-labs-onesie']").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()

    # Fill form
    driver.find_element(By.ID, "first-name").send_keys("Jin")
    driver.find_element(By.ID, "last-name").send_keys("Xu")
    driver.find_element(By.ID, "postal-code").send_keys("K2K 1E5")
    driver.find_element(By.ID, "continue").click()

    # Verify Total
    total_label_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))
    assert "Total: $8.63" in total_label_element.text

    # Finish
    driver.find_element(By.ID, "finish").click()
    success_message_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "complete-header")))
    assert success_message_element.text == "Thank you for your order!"
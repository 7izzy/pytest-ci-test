# 匯入 Selenium 所需模組
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# 定義登入函式：傳入帳號與密碼，回傳畫面上的訊息
def login(username, password,screenshot_name):
    # 啟動 Chrome 瀏覽器
    driver = webdriver.Chrome()
    
    # 開啟測試網站登入頁面
    driver.get("https://the-internet.herokuapp.com/login")
    
    # 輸入帳號與密碼，並點擊登入按鈕
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CLASS_NAME, "radius").click()

    # 等待 1 秒，讓訊息顯示出來
    time.sleep(1)

    # 擷取登入結果訊息（成功或錯誤提示）
    message = driver.find_element(By.ID, "flash").text

    # 截圖存檔
    os.makedirs("screenshots", exist_ok=True)
    driver.save_screenshot(f"screenshots/{screenshot_name}.png")

    # 關閉瀏覽器
    driver.quit()

    # 回傳訊息給測試用
    return message

# 測試案例 1：正確登入（期望成功）
def test_valid_login():
    result = login("tomsmith", "SuperSecretPassword!", "TC01_success")

    # Trigger CI
    assert "You logged into a secure area!" in result

# 測試案例 2：密碼錯誤（期望顯示密碼錯誤訊息）
def test_wrong_password():
    result = login("tomsmith", "wrongpassword", "TC02_wrong")
    assert "Your password is invalid!" in result

# 測試案例 3：帳密皆空白（期望顯示帳號錯誤訊息）
def test_blank_input():
    result = login("", "", "TC03_blank")
    assert "Your username is invalid!" in result

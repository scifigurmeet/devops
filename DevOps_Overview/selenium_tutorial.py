from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    # Create a new Chrome driver instance
    driver = webdriver.Chrome()
    
    try:
        # Navigate to Google
        driver.get("https://www.google.com")
        
        # Find the search box using name attribute
        search_box = driver.find_element(By.NAME, "q")
        
        # Type into the search box
        search_box.send_keys("LPU")
        
        # Press Enter
        search_box.send_keys(Keys.RETURN)
        
        # Wait for search results to load (explicit wait)
        wait = WebDriverWait(driver, 10)
        search_results = wait.until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        # Demonstrate different ways to find elements
        # Find multiple elements
        results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        print(f"Found {len(results)} search results")
        
        # Get the title of the page
        print(f"Page title: {driver.title}")
        
        # Take a screenshot
        driver.save_screenshot("lpu.png")
        
        # Pause to see the results
        time.sleep(3)
        
    finally:
        # Always close the browser
        driver.quit()

if __name__ == "__main__":
    main()

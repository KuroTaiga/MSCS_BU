from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
import base64
import urllib.request

def download_images(search_term, num_images):
    # Setup the Chrome WebDriver with the specified path
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/imghp")
    
    # Locate the search box, enter the search term, and hit enter
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)
    
    # Scroll to load more images
    for _ in range(num_images // 20):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    # Locate image elements
    image_elements = driver.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")
    
    # Create a directory for the images
    if not os.path.exists(search_term):
        os.makedirs(search_term)
    
    # Download the images
    count = 0
    for img in image_elements:
        print("here")
        if count >= num_images:
            break
        try:
            img_url = img.get_attribute("src")
            if not img_url:
                img_url = img.get_attribute("data-src")
            
            if img_url:
                if img_url.startswith('data:image'):
                    # Base64 encoded image
                    image_data = base64.b64decode(img_url.split(',')[1])
                    with open(f"{search_term}/{search_term}_{count + 1}.jpg", 'wb') as f:
                        f.write(image_data)
                else:
                    # Regular image URL
                    urllib.request.urlretrieve(img_url, f"{search_term}/{search_term}_{count + 1}.jpg")
                count += 1
        except Exception as e:
            print(f"Could not download image {count + 1}: {e}")
    
    driver.quit()

if __name__ == "__main__":
    #search_term = input("Enter the search term: ")
    #num_images = int(input("Enter the number of images to download: "))
    search_term = "dumbbell"
    num_images = 10
    download_images(search_term, num_images)

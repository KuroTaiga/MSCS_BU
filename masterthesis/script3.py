from selenium import webdriver
import time
import requests
import shutil
import os
import argparse

from selenium.webdriver.common.by import By
def save_img(inp,img,i, directory):
    try:
        filename = inp+str(i)+'.jpg'
        response = requests.get(img,stream=True)
        image_path = os.path.join(directory, filename)
        with open(image_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
    except Exception:
        pass


def find_urls(inp,url,driver, directory):
    driver.get(url)
    for _ in range(500):
        driver.execute_script("window.scrollBy(0,10000)")
        try:
            driver.find_elements(By.CSS_SELECTOR,'.mye4qd').click()
        except:
            continue
    for j, imgurl in enumerate(driver.find_element(By.XPATH,'//img[contains(@class,"YQ4gaf")]')):
        try:
            imgurl.click()
            img = driver.find_element_by_xpath('//body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img').get_attribute("src")
            save_img(inp,img,j, directory)
            time.sleep(1.5)
        except:
            pass
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scrape Google images')
    parser.add_argument('-s', '--search', default='dumbbell', type=str, help='search term')
    parser.add_argument('-d', '--directory', default='../Downloads/', type=str, help='save directory')
    args = parser.parse_args()
    driver = webdriver.Chrome()
    directory = args.directory
    inp = args.search
    if not os.path.isdir(directory):
        os.makedirs(directory)
    url = 'https://www.google.com/search?q='+str(inp)+'&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947'
    find_urls(inp,url,driver, directory)
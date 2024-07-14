# modified from git
# depending on what seach engine you use, you need to modify the search_url and the class names you are looking for
# do "right click->inspection" to see what class the search engine use
import os
import time
import requests
from selenium import webdriver 
from selenium.webdriver.common.by import By
def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 0.2):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

    # build the google query

    #search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    search_url = "https://duckduckgo.com/?q={q}&iax=images&ia=images"
    

# load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        #thumbnail_results = wd.find_elements(By.CSS_SELECTOR,"img.YQ4gaf")
        time.sleep(1) #longer sleep for images to load
        thumbnail_results = wd.find_elements(By.CLASS_NAME,"tile--img__img")
        number_results = len(thumbnail_results)

        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            #actual_images = wd.find_elements(By.CSS_SELECTOR,"img.YQ4gaf")
            actual_images = wd.find_elements(By.CLASS_NAME,"detail__media__img-highres")
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    #if (int(actual_image.get_attribute('height')) >= 640) and (int(actual_image.get_attribute('width'))>=640):
                    image_urls.add(actual_image.get_attribute('src'))
                    #else:
                    #    print("Image too small <640*640, ignoring")

            image_count = len(image_urls)

        if len(image_urls) >= max_links_to_fetch:
            print(f"Found: {len(image_urls)} image links, done!")
            break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(3)
            
        
        #load_more_button = wd.find_elements(By.CSS_SELECTOR,".mye4qd")
        #if load_more_button:
        #    wd.execute_script("document.querySelector('.mye4qd').click();")
        #    load_more_button.click()
        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path:str,url:str, counter):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")

def search_and_download(search_term: str, target_path='./images', number_images=10):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome() as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.25)

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1

if __name__ == "__main__":
    DRIVER_PATH = './chromedriver'
    search_term = 'gym band workout'
    # num of images you can pass it from here  by default it's 10 if you are not passing
    # can also change this into inputs:
    #search_term = input("Enter the search term: ")
    #num_images = int(input("Enter the number of images to download: "))
    # or arguments
    #parser = argparse.ArgumentParser(description='Scrape Google images')
    #parser.add_argument('-s', '--search', default='dumbbell', type=str, help='search term')
    #parser.add_argument('-d', '--directory', default='../Downloads/', type=str, help='save directory')
    number_images = 100
    search_and_download(search_term=search_term, number_images=number_images)
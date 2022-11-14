PATH = "C:\Program Files (x86)\chromedriver.exe"

import tkinter
from tkinter import *
from tkinter import ttk
from functools import partial

# GUI for the first window
root = Tk()
root.title('Amazon Scraper')
root.geometry("400x150")
content = ttk.Frame(root)
frame = ttk.Frame(content)
names = []
prices = []
ratings = []
n_ratings = []
links = []
# Amazon Scraper
def amazon_scraper():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait as wait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    global data_dict

    url = f"https://www.amazon.de/"
    options = Options()
    service = Service(executable_path=PATH)
    options.headless = True
    driver = webdriver.Chrome(options=options,service=service)
    name = user_product.get()
    pages = int(user_pages.get())

    side_pages = 0
    try:
        print("Entering the website ...")
        try:#Accepting the cookies
            driver.get(url)
            driver.find_element(By.XPATH,'//*[@id="sp-cc-accept"]').click()
        except:
            pass
        try:#Searching for the product
            time.sleep(1)
            search = driver.find_element(By.XPATH,'//*[@id="twotabsearchtextbox"]')
            time.sleep(1.1)
            search.send_keys(f"{name}")
            time.sleep(1)
            search.send_keys(Keys.RETURN)
            time.sleep(1.2)
        except:
            pass
        global names
        global prices
        global ratings
        global n_ratings
        global links

        while side_pages <= pages:
            print(f"Collecting all items on page {side_pages + 1} ... ")
            try:
                items = wait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))

                for item in items:
                    try:
                        name = item.find_element(By.XPATH,'.//span[@class="a-size-medium a-color-base a-text-normal"]').text
                        names.append(name)

                        price = item.find_element(By.XPATH,'.//span[@class="a-price-whole"]').text.replace(",",".")
                        prices.append(price)
                    except Exception as e:
                        prices.append("/")
                        pass
                    try:
                        rating = item.find_element(By.XPATH,'.//span[@class="a-icon-alt"]').get_attribute('textContent').replace(",",".")
                        ratings.append(rating)
                    except Exception as e:
                        ratings.append("/")
                        pass
                    try:
                        n_rating = item.find_element(By.XPATH,'.//span[@class="a-size-base s-underline-text"]').get_attribute('textContent')
                        n_ratings.append(n_rating)
                    except Exception as e:
                        n_ratings.append("/")
                        pass
                    try:
                        link = item.find_element(By.TAG_NAME,"a").get_attribute("href")
                        links.append(link)
                    except Exception as e:
                        print("Error finding the link")
                        pass
            except Exception as d:
                pass
            driver.find_element(By.XPATH,'.//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]').click()
            time.sleep(3)
            side_pages += 1
        driver.quit()
        print("Finished.")
    except Exception as e:
        pass
        time.sleep(2)
        driver.quit()

try:
    #entries
    user_product_value = tkinter.StringVar()
    user_product = ttk.Entry(content, textvariable=user_product_value)
    user_product_lbl = ttk.Label(content,text="Enter product name")
    user_page_value = tkinter.IntVar()
    user_pages = ttk.Entry(content,textvariable=user_page_value)
    user_pages_lbl = ttk.Label(content,text="Enter number of pages")

    #define clear-button
    def clear():
        names.clear()
        prices.clear()
        links.clear()
        ratings.clear()
        n_ratings.clear()

    #buttons
    search_button = ttk.Button(content, text="Search & Collect", command=partial(amazon_scraper))
    clear_button = ttk.Button(content, text="Clear All Data", command=partial(clear))
    exit_button = ttk.Button(content, text="Exit & View Data", command=root.destroy)

    #grid
    content.grid(column=0, row=0)
    frame.grid(column=0, row=0, columnspan=10, rowspan=10)
    search_button.grid(column=2, row=2, columnspan=2, padx=5)
    clear_button.grid(column=2,row=3,columnspan=2, padx=5)
    exit_button.grid(column=2, row=4, columnspan=2, padx=5)
    user_product.grid(column=0,row=0)
    user_product_lbl.grid(column=1,row=0)
    user_pages.grid(column=0,row=1)
    user_pages_lbl.grid(column=1,row=1)

    root.mainloop()

    #GUI for the second window
    #saving data as xlsx function
    def pd_saver():
        import pandas as pd
        data_dict = {
            "Product": names,
            "Price": prices,
            "Link": links,
            "Rating": ratings,
            "Ratings": n_ratings

        }
        df = pd.DataFrame(data_dict)
        df.to_excel(f"{save_as.get()}.xlsx")
        print("xlsx saved.")

    root2 = Tk()
    root2.title('Product Data')
    root2.geometry("800x300")
    generalFrame = Frame(root2)
    scrollbarFrame = Frame(root2)
    scrollbar = Scrollbar(scrollbarFrame)
    data_box = Listbox(scrollbarFrame, yscrollcommand=scrollbar.set)
    for item in range(len(names)):
        data_box.insert(END,names[item],prices[item],"\n")
    scrollbar.config(command=data_box.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    data_box.pack(fill=BOTH)
    scrollbarFrame.pack(fill=BOTH)
    generalFrame.pack()

    #buttons
    save_as_value = tkinter.StringVar()
    save_as = ttk.Entry(generalFrame, textvariable=user_product_value)
    save_as_lbl = ttk.Label(generalFrame, text="Save as:")
    save_as.pack()

    save_button = ttk.Button(generalFrame, text="Save as xlsx", command=partial(pd_saver))
    save_button.pack()

    exit_button2 = ttk.Button(generalFrame, text="Exit & Over", command=root2.destroy)
    exit_button2.pack()
    root2.mainloop()

except Exception as e:
    print(e)

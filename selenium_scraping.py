import os
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
#from chromeVersion import get_chrome_version
# os.environ['PATH'] += r"/Selenium drivers"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def initDriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.headless = True
    #ver = get_chrome_version()
    #driver_url = f"./driver/{ver[0:3]}.exe"
    driver_url = f"./chromedriver.exe"
    global driver
    driver = webdriver.Chrome(resource_path(
        driver_url), options=options)


def neighbour_construction(state, street, city, buildingNum, direction, dir_status):
    initDriver()
    cityURL = '-'.join(map(str, city))
    streetURL = '-'.join(map(str, street))
    url = f"https://www.neighborwho.com/{streetURL}-{cityURL}-{state}-addresses"
    driver.get(url)
    if dir_status == 1:
        compare_text1 = f"{buildingNum} {' '.join(map(str,street))} {direction[0]}"
        compare_text2 = f"{buildingNum} {direction[0]} {' '.join(map(str,street))}"
    else:
        compare_text1 = f"{buildingNum} {' '.join(map(str,street))}"
        compare_text2 = compare_text1
    while True:
        elements = driver.find_elements(By.CLASS_NAME, 'card-title')
        for item in elements:
            if item.text.upper() == compare_text1.upper() or item.text.upper() == compare_text2.upper():
                parent = item.find_element(By.XPATH, "..")
                upper_parent = parent.find_element(By.XPATH, "..")
                year_built = upper_parent.find_elements(By.XPATH, ".//*")
                for item in year_built:
                    new_list = item.text.split("\n")
                    for new_item in new_list:
                        if "Built in" in new_item:
                            value = new_item[9:]
                            print(f"NEIGHBOURWHO\t: {value}")

                            return

        next = driver.find_elements(By.CLASS_NAME, "next-arrow-on")
        if next:
            next[0].click()
            continue
        else:
            break

    print("NEIGHBOURWHO\t: Not found")
    return


def spokeo_connect():
    
    property_card = driver.find_elements(By.CLASS_NAME, 'summary-details')
    if len(property_card) > 0:
        property_list = property_card[0].text.split("\n")
        # print(property_list)
        for item in property_list:
            if item == "Year Built":
                index = property_list.index(item)
                year_constructed_spokeo = property_list[index+1]
                print(f"SPOKEO\t\t: {year_constructed_spokeo}")
                driver.quit()
                return 1
    return 0
    # property_card = driver.find_elements(By.CLASS_NAME, 'e3nj0sk0')
    # if len(property_card) > 0:
    #     year = property_card[0].text.split("\n")
    #     print(year)
    #     if year.upper == "YEAR BUILT":
    #         year_constructed_spokeo=driver.find_element(By.CLASS_NAME,'e4pkwgj0').text
    #         print(f"SPOEKO\t\t: {year_constructed_spokeo}")
    #         driver.quit()
    #         return 1
    # return 0


def spokeo_construction(state, street, city, buildingNum, direction, dir_status):

    for i in range(len(city)):
        city[i] = city[i].capitalize()
    for i in range(len(street)):
        street[i] = street[i].capitalize()
    city_url = '-'.join(map(str, city))
    street_url = '-'.join(map(str, street))
    if dir_status == 1:
        if direction[1] < 2:
            url1 = f"https://www.spokeo.com/{state}/{city_url}/{buildingNum}-{direction[0]}-{street_url}"
            url2 = f"https://www.spokeo.com/{state}/{city_url}/{buildingNum}-{street_url}-{direction[0]}"
        else:
            url2 = f"https://www.spokeo.com/{state}/{city_url}/{buildingNum}-{direction[0]}-{street_url}"
            url1 = f"https://www.spokeo.com/{state}/{city_url}/{buildingNum}-{street_url}-{direction[0]}"

    else:
        url1 = f"https://www.spokeo.com/{state}/{city_url}/{buildingNum}-{street_url}"
        url2 = url1

    driver.get(url1)
    if (spokeo_connect() == 1):
        return
    else:
        driver.quit()
    initDriver()
    driver.get(url2)
    if (spokeo_connect() == 1):
        return
    else:
        print("SPOEKO\t\t: Not found")
        driver.quit()


def been_verified(state, street, city, buildingNum, direction, dir_status):

    city_url = '-'.join(map(str, city))
    street_url = '-'.join(map(str, street))

    url = f"https://www.beenverified.com/property/{state}/{city_url}/{street_url}-residences/".lower()

    initDriver()

    driver.get(url)
    while True:
        property_card = driver.find_elements(By.CLASS_NAME, 'col-sm-5')
        if (len(property_card) == 0):
            property_card = driver.find_elements(By.CLASS_NAME, 'col-sm-6')

        if dir_status == 1:
            compare_text1 = f"{buildingNum} {' '.join(map(str,street))} {direction[0]}"
            compare_text2 = f"{buildingNum} {direction[0]} {' '.join(map(str,street))}"
        else:
            compare_text1 = f"{buildingNum} {' '.join(map(str,street))}"
            compare_text2 = compare_text1

        if property_card:
            for item in property_card:
                item_contents = item.text.split('\n')
                if (item_contents[0].upper() == compare_text1 or item_contents[0].upper() == compare_text2):
                    for new_item in item_contents:
                        if "Year Built" in new_item:
                            year_built = new_item[-4:]
                            print(f"BEEN VERIFIED\t: {year_built}")
                            driver.quit()
                            return
        next = driver.find_elements(By.CLASS_NAME, 'page-link')
        new_page = 0
        if next:
            for item in next:
                if item.text == "Next":
                    new_page = 1
                    item.click()

            if new_page == 1:
                continue
            else:
                break
        else:
            break

    print("BEEN VERIFIED\t: Not found")
    driver.quit()
    return


def propertyShark(input_address):

    initDriver()
    url ="https://www.propertyshark.com/mason/"
    driver.get(url)

    
    search_bar =driver.find_element(By.ID,'search_token_address')
    search_bar.send_keys(input_address)
    time.sleep(3)
    try:
        autocomp = driver.find_elements(By.CLASS_NAME,'autocomplete-property')
        autocomp[0].click()
    except:
        print("PROPERTY SHARK  : Not Found")
        driver.quit()
        return 0
   
    try:
        year_data= driver.find_element(By.XPATH,'//*[@id="nationwide/property_details_content"]/div/div[2]/table/tbody/tr[5]/td[1]')
        year=driver.find_element(By.XPATH,'//*[@id="nationwide/property_details_content"]/div/div[2]/table/tbody/tr[5]/td[2]').text
        print(f"PROPERTY SHARK  : {year}")
        driver.quit()
        return 1
    except:
        print("PROPERTY SHARK  : Not Found")
        driver.quit()
        return 0


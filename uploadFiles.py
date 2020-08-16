from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import re
import time
import os

def main():
    #get file names to upload
    path = ".\\"
    unformatted_names = getFileNames(path)
    formatted_names = formatNames(unformatted_names)
    upload(formatted_names, unformatted_names, path)


def getFileNames(path):
    file_names = []
    for file in os.listdir(path):
        file_names.append(file)
    return file_names

def formatNames(file_names):
    #name can't contain dots, quotes, or any other special character
    file_names = [i.encode("utf-8") for i in file_names]
    file_names = [str(i).replace('b\'', "").replace('\'', "").replace('\\', "").replace('\"', "").replace(',', "").replace('.jpg', "").replace("!", "") for i in file_names]

    #remove all dots but last
    file_names = [removeDots(i) for i in file_names]
    return file_names

def removeDots(name):
    s = name.split('.')
    return str("".join(s))


def upload(formatted_names, unformatted_names, path):
    email = 'test@gmail.com'
    password = 'test_pass'
    dimension = '260'

    driver = webdriver.Chrome(executable_path='C://WebDriver/bin/chromedriver')
    # Go to your page url
    driver.get('https://developer.vuforia.com/vui/auth/login')

    #put in credentials to login
    driver.implicitly_wait(10)
    input_email = driver.find_element_by_id('login_email').send_keys(email)
    input_pass = driver.find_element_by_id('login_password').send_keys(password)
    button_login = driver.find_element_by_id('login').click()

    #choose project
    driver.implicitly_wait(10)
    button_target = driver.find_element_by_id('targetManager')
    button_target.click()

    # driver.implicitly_wait(10)
    button_project = driver.find_element_by_class_name('ui-table-tbody')
    button_project.click()

    # #loop multiple times for each image file
    for i in range(len(unformatted_names)):
            print(formatted_names[i], unformatted_names[i])
            #find the window for adding targets
            modal_window = driver.find_element_by_xpath("//*[@id='addDeviceTargetUserView']")
            actions = ActionChains(driver)
            actions.click(modal_window).perform()
            time.sleep(4)

            dimension = driver.find_element_by_id('targetDimension')
            actions.send_keys_to_element(dimension, dimension).perform()
            actions.reset_actions()
            time.sleep(2)

            button_upload = driver.find_element_by_id('targetImgFile')
            name = path + '\\' + unformatted_names[i]
            button_upload.send_keys(name);
            time.sleep(4)

            name_action = ActionChains(driver)
            file_name = driver.find_element_by_id('targetName')
            file_name.clear()

            name_action.send_keys_to_element(file_name, formatted_names[i]).perform()
            name_action.reset_actions()
            time.sleep(3)

            add_action = ActionChains(driver)
            button_add = driver.find_element_by_id('AddDeviceTargetBtn')
            add_action.click(button_add).perform()
            add_action.reset_actions()

            time.sleep(10)


if __name__=="__main__":
    main()

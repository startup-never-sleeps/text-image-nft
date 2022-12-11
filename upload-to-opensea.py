from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import json
import time

path        = './nfts/'
path_images = path + 'images/'
path_meta   = path + 'metadata/'
image_extension = '.jpg'
json_extension  = '.json'

TIMEOUT = 30
PING    = 5

opensea = 'https://testnets.opensea.io'

options = Options()
options.add_argument("--disable-infobars")
options.add_argument("--enable-file-cookies")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_extension('./metamask-ext/extension_10_22_2_0.crx')

print("Enter collection name:")
collection = input()

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
browser.get(opensea + '/collection/' + collection + '/assets/create')

def wait_any_element_to_have_text(xpath, text, wait_time=TIMEOUT):
    secs_passed = 0
    while secs_passed < wait_time:
        elements = browser.find_elements(By.XPATH, xpath)
        for element in elements:
            if element.text == text:
                return element
        
        time.sleep(PING)
        secs_passed += PING

def center_and_click(element):
    script = """
        var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        var elementTop = arguments[0].getBoundingClientRect().top;
        window.scrollBy(0, elementTop-(viewPortHeight / 2));
        """

    browser.execute_script(script, element)
    element.click()
    return element

def write_text(element, text):
    script = """
        var element = arguments[0], txt = arguments[1];
        element.value = txt;
        element.innerHTML = txt;
        element.dispatchEvent(new Event('change'));
        """

    text = text.replace("\\n", "\n")
    browser.execute_script(script, element, text)
    element.send_keys(" " + Keys.BACKSPACE)

def read_token_info(token):
    data = []
    with open(path_meta + str(token) + json_extension, "r") as jsonfile:
        try:
            data = json.load(jsonfile)
        except:
            data = []
    
    token_name        = data['name']
    token_description = data['description']
    token_properties  = data['attributes']
    
    return (token_name, token_description, token_properties)

def mint_token(token):
    # Add media
    media = browser.find_element(By.ID, "media")
    browser.execute_script("arguments[0].style.display = 'block';", media)
    media.send_keys(path_images + str(token) + image_extension)

    # Read token's metadata
    token_info = read_token_info(token)
    token_name        = token_info[0]
    token_description = token_info[1]
    
    # Add name
    name = browser.find_element(By.ID, "name")
    write_text(name, token_name)
    
    # Add description
    description = browser.find_element(By.ID, "description")
    write_text(description, token_description)
    
    # Create
    create = browser.find_element(By.XPATH, "//button[text()='Create']")
    center_and_click(create)
    time.sleep(PING)
    
    #And wait for confirmation
    minted = wait_any_element_to_have_text("//h4", 'You created ' + token_name + '!')
    
    return (minted is not None)

def main():
    print("At this point you need to open a new tab and log into MetaMask to import your wallet."
          "Once you do that, go back to the OpenSea tab and connect MetaMask wallet to your account.")
    print("Press any key after connecting the wallet")
    input()
    time.sleep(PING)
    mint_token('1') # TODO: use image name

main()

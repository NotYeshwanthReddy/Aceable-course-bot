import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from prompts import question_prompt
# Load environment variables
load_dotenv()

# Access email and password from .env file
email_id = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Initialize WebDriver (use ChromeDriver as an example)
service = Service()  # Update with the path to your ChromeDriver
options = webdriver.ChromeOptions()

# Optional: Add any additional options (e.g., headless mode)
# options.add_argument('--headless')

# Start the WebDriver
driver = webdriver.Chrome(service=service, options=options)


def login():
    # Wait until the email input field is present
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/section/section/main/div/div[1]/main/form[1]/div[1]/div[1]/input'))
    )

    # Find the email input field and enter the email
    email_input = driver.find_element(By.XPATH, '/html/body/div/section/section/main/div/div[1]/main/form[1]/div[1]/div[1]/input')
    email_input.send_keys(email_id)

    # Find the password input field and enter the password
    password_input = driver.find_element(By.XPATH, '/html/body/div/section/section/main/div/div[1]/main/form[1]/div[2]/div[1]/input')
    password_input.send_keys(password)

    # Submit the form
    password_input.send_keys(Keys.RETURN)
    

def click_optional_buttons():
    # optional button 1
    # Click the specified button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/section/section/main/div/main/div[1]/div/div[1]/div[1]/div/div[3]/button'))
    )
    button = driver.find_element(By.XPATH, '/html/body/div/section/section/main/div/main/div[1]/div/div[1]/div[1]/div/div[3]/button')
    button.click()
    # optional button 2
    # Click the got it button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/section[1]/div[2]/div/button'))
    )
    button = driver.find_element(By.XPATH, '/html/body/div/div[1]/section[1]/div[2]/div/button')
    button.click()
    # optional button 3
    # Click the got it button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/section[2]/div[1]/div/button'))
    )
    button = driver.find_element(By.XPATH, '/html/body/div/div[1]/section[2]/div[1]/div/button')
    button.click()

def check_question_section():
    # Check if the specific section exists
    try:
        section = driver.find_element(By.XPATH, '/html/body/div/section/section/main/main/article/div')
        print("The Question section exists on the page.")
        # Extract and print the HTML content of the section
        question_section_html = section.get_attribute('outerHTML')
        print("Extracted HTML content:", question_section_html)
        return question_section_html
    except:
        print("The Question  section does not exist on the page.")
        return None

def answer_question(prompt):
    # answer_button_Xpath = get_answer(prompt)
    answer_button_Xpath = '/html/body/div/section/section/main/main/article/div/ul/li[3]/button'
    try:
        answer_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, answer_button_Xpath))
        )
        answer_button.click()
        print("Clicked on the answer button.")
    except Exception as e:
        print(f"An error occurred while clicking the submit button: {e}")

try:
    # Open the URL
    driver.get("https://app.aceable.com/user/signin")

    login()

    # Wait for the page to load after login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    while True:
        
        click_optional_buttons()

        question_section_html = check_question_section()
        if question_section_html!=None:
            prompt = question_prompt.format(question_section_html=question_section_html)
            print("User interference required")
            time.sleep(3)

        # Wait for the timer countdown to finish and click the button
        try:
            timer_element = driver.find_element(By.XPATH, '/html/body/div/section/section/main/main/nav/div/div[3]/button/span[1]/div')
            try:
                timer_text = timer_element.text

                # Parse the timer text into seconds
                if ":" in timer_text:
                    minutes, seconds = map(int, timer_text.split(":"))
                    wait_time = minutes * 60 + seconds
                else:
                    wait_time = int(timer_text)

                # Wait for the specified time
                print(f"Waiting for {wait_time} seconds for the timer to reach 00:00.")
                time.sleep(wait_time)
                timer_button.click()
            except:
                print("Timer not found, just clicking next button")
                # Click the button
                timer_button = driver.find_element(By.XPATH, '/html/body/div/section/section/main/main/nav/div/div[3]/button')
                timer_button.click()

        except Exception as e:
            print(f"An error occurred while waiting for the timer or clicking the next button: {e}")


finally:
    # Quit the driver
    driver.quit()

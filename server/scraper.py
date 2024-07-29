import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, make_response, request, jsonify
from flask_restful import Resource, Api
import requests

class Scraper(Resource):
    def post(self):
        data = request.json
        url = data.get('url')
        username = data.get('username')
        password = data.get('password')
        class_name = data.get('class_name')
        button_class = data.get('button_class', None)
        webhook_url = data.get('webhook_url', None)

        if not all([url, username, password, class_name]):
            return make_response(jsonify({"error": "Missing required parameters"}), 400)

        try:
            scraped_data = self.scrape_website(url, username, password, class_name, button_class, webhook_url)
            return make_response(jsonify({"scraped_data": scraped_data}), 200)
        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)

    def scrape_website(self, url, username, password, class_name, button_class=None, webhook_url=None):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Optional: start maximized

        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        scraped_data = []

        try:
            # Navigate to the login page
            login_url = "https://balancedcomfort.sera.tech/admins/login"  # Fixed login URL
            driver.get(login_url)

            # Find and fill in login form fields
            email_field = driver.find_element(By.ID, "admin_email")
            password_field = driver.find_element(By.ID, "admin_password")

            email_field.send_keys(username)
            password_field.send_keys(password)

            # Submit the login form
            login_button = driver.find_element(By.NAME, "commit")
            login_button.click()

            # Wait for the URL to change after login
            WebDriverWait(driver, 10).until(EC.url_contains("https://balancedcomfort.sera.tech/"))

            # Navigate to the target URL
            driver.get(url)

            # Click on any additional button if needed
            if button_class:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, button_class))
                )
                button.click()

            # Wait for the presence of the elements with the specified class name
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
            )

            # Collect data from the found elements
            for element in elements:
                scraped_data.append(element.text)

        finally:
            # Close the WebDriver session
            driver.quit()

        # Post data to webhook if URL is provided
        if webhook_url:
            requests.post(webhook_url, json={'data': scraped_data})

        return scraped_data
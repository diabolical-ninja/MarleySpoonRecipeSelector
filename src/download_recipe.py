import json
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from recipe_parser import extract_recipe_info


def create_selenium_instance():
    """Instantiates a Selenium Chrome WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def download_rendered_pages_from_urls(driver, urls, output_dir="rendered_recipe_pages"):
    """
    Iterates over a list of URLs and downloads the *rendered* page source.

    Args:
        driver (webdriver.Chrome): Selenium WebDriver instance.
        urls (list): List of URLs to download.
        output_dir (str): Directory to save the downloaded pages.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, url in enumerate(urls):
        if url:
            try:
                driver.get(url)
                # Wait for a specific element to be present, indicating the page is loaded
                # Adjust the element and timeout as needed for the target websites.
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.ID, "dish_detail")
                    )  # or some other specific element
                )
                sleep(2)
                page_source = driver.page_source
                filename = os.path.join(output_dir, f"rendered_recipe_{i+1}.html")
                with open(filename, "w", encoding="utf-8") as outfile:
                    outfile.write(page_source)
                print(f"Downloaded rendered: {url} to {filename}")

                # Extract recipe information
                recipe_info = extract_recipe_info(page_source)
                recipe_info["url"] = url

                # Save recipe information to a JSON file
                json_filename = os.path.join(output_dir, f"recipe_info_{i+1}.json")
                with open(json_filename, "w", encoding="utf-8") as json_file:
                    json.dump(recipe_info, json_file, indent=4)

            except Exception as e:
                print(f"Error downloading {url}: {e}")


def read_urls_from_file(file_path):
    """Reads URLs from a text file and returns them as a list."""
    urls = []
    try:
        with open(file_path, "r") as f:
            for url in f:
                urls.append(url.strip())
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
    return urls


if __name__ == "__main__":
    # Example usage:
    file_path = "recipe_urls.txt"
    urls = read_urls_from_file(file_path)

    if urls:
        driver = create_selenium_instance()
        try:
            download_rendered_pages_from_urls(driver, urls)
        finally:
            driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
from bs4 import BeautifulSoup
import csv

# Function to log in to LinkedIn
def login_to_linkedin(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()

    time.sleep(5)

# Function to search for profiles
def search_profiles(driver, query):
    search_box = driver.find_element(By.XPATH, "//input[@aria-label='Search']")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)

# Function to click on "See all people results"
def click_see_all_results(driver):
    try:
        # Wait for the "See all people results" link to appear and click it
        see_all_button = driver.find_element(By.XPATH, "//a[contains(@class, 'UCscCatRDSWOVGPsBHtBFxutMeBcJczyetPkw') and contains(text(), 'See all people results')]")
        see_all_button.click()
        time.sleep(5)
        print('- Clicked on "See all people results"')
    except NoSuchElementException:
        print('- "See all people results" link not found')

def scrape_profiles(driver, pages_to_scrape):
    profiles_data = []

    for page in range(pages_to_scrape):
        try:
            time.sleep(5)  # Allow the page to load
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all profile containers
            profiles = soup.find_all('div', class_='AmpDiXyOZbcHbsDjaxRkciolonfpPJM lQpaEfiiuWhEvrHFgaSBvUcdQpubtGTUtdxYI pt3 pb3 t-12 t-black--light')
            
            if not profiles:
                print('- No profiles found on this page')
                break

            print(f"- Found {len(profiles)} profiles on page {page + 1}")

            for profile in profiles:
                try:
                    # Extract name
                    name_element = profile.find('a', class_='UCscCatRDSWOVGPsBHtBFxutMeBcJczyetPkw')
                    # Extract profile information
                    profile_element = profile.find('div', class_='xUVCcEVPuWMIxGCkoqhxScRxbhzxjiMCCQ t-14 t-black t-normal')

                    if name_element and profile_element:
                        name = name_element.get_text(strip=True)
                        profile_info = profile_element.get_text(strip=True)

                        print(f'- Found profile: {name} | {profile_info}')
                        profiles_data.append({
                            'Name': name,
                            'Profile': profile_info
                        })
                    else:
                        print('- Skipping a profile due to missing data')
                except AttributeError:
                    print('- Skipping a profile due to missing data')

            # Click "Next" to navigate to the next page
            try:
                # Locate the "Next" button using its class and text
                next_button = driver.find_element(By.XPATH, "//button[span[text()='Next']]")
                next_button.click()
                time.sleep(5)  # Wait for the next page to load
                print('- Moving to the next page...')
            except NoSuchElementException:
                print('- No more pages available or unable to locate Next button')
        except Exception as e:
            print(f'- Error during scraping: {e}')
            break

    return profiles_data




import os

# Function to save data to a CSV file
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Ensure that the fieldnames match the dictionary keys
        fieldnames = ['Name', 'Profile']  # Make sure 'Profile' is used here instead of 'Profile Info'
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header and data rows
        writer.writeheader()
        writer.writerows(data)
        
    print(f'- Data saved to {filename}')



# Main function
def main():
    username = input("Enter your LinkedIn username: ")
    password = input("Enter your LinkedIn password: ")
    search_query = 'IIT'
    pages_to_scrape = int(input("Enter the number of pages to scrape: "))

    # Set up Selenium WebDriver (ensure the driver is in your PATH)
    driver = webdriver.Chrome()

    try:
        # Log in to LinkedIn
        login_to_linkedin(driver, username, password)

        # Search for profiles
        search_profiles(driver, search_query)

        # Click on "See all people results"
        click_see_all_results(driver)

        # Scrape profiles
        print(f'- Starting to scrape {pages_to_scrape} pages of profiles...')
        profiles_data = scrape_profiles(driver, pages_to_scrape)

        # Save the scraped data to a CSV file
        save_to_csv(profiles_data, '../Output/profiles.csv')

    except Exception as e:
        print(f'Error: {e}')

    finally:
        # Close the WebDriver
        driver.quit()
        print('- WebDriver closed')


if __name__ == "__main__":
    main()

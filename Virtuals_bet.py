import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

VISUALS_SITE = "https://realnaps.com/choosy_vfl.php"
SPORTY_BET = "https://www.sportybet.com/ng/m/virtual"


#
#
# TACKLING ERRORS

class countdown_stabilized:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        initial_value = element.text
        time.sleep(4)
        final_value = driver.find_element(*self.locator).text
        return initial_value == final_value


# ==================== ALL FUNCTIONS ==================== #

#
#

# ==================== GETTING BET VALUE ================ #

def get_bet_value():
    def get_team_name(element_id, max_retries=10):
        retries = 0
        while retries < max_retries:
            try:
                team_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, element_id)))
                team_name = team_element.text
                if team_name == "loading" or team_name == "":
                    retries += 1
                    print(f"Retrying... Attempt {retries}/{max_retries}")
                    time.sleep(5)  # Adjust the sleep interval as needed
                else:
                    return team_name
            except Exception as e:
                retries += 1
                print(f"Retrying... Attempt {retries}/{max_retries}")
                time.sleep(5)  # Adjust the sleep interval as needed

        return None

    # Usage
    hm1 = get_team_name("hm1")
    aw1 = get_team_name("aw1")
    hm2 = get_team_name("hm2")
    aw2 = get_team_name("aw2")
    hm3 = get_team_name("hm3")
    aw3 = get_team_name("aw3")

    if hm1 and aw1:
        print("Value without loading in the div element:\n", hm1, aw1)
    else:
        print("Failed to retrieve team names")


#
#

# ================== CHECKING BET STATUS ================ #
def check_bet_status():
    countdown_locator = (By.CLASS_NAME, "col.text-center.betStatus")

    try:
        while True:
            try:
                WebDriverWait(driver, 100).until(countdown_stabilized(countdown_locator))
            except TimeoutException as e:
                print("Timeout occurred. Retrying...")
                # Perform any necessary cleanup here if needed
                continue  # Retry the WebDriverWait

            # Get the final value when the countdown timer has stabilized
            final_value = driver.find_element(*countdown_locator).text
            get_bet_value()
            break  # Break out of the loop if successful

    except Exception as e:
        close_button = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "close"))
        )
        close_button.click()
        get_bet_value()


# ===================== CLICK NIGERIA =================== #
def click_nigeria():
    nigeria_logo = driver.find_element(By.ID, "Nigeria")
    nigeria_logo.click()


#
#

# ============ LOCATE SCHEDULED VIRTUALS ================== #
def locate_scheduled_virtuals():
    image_element = driver.find_element(By.XPATH, '//img[@src="https://realnaps.com/signal/premium/images/sportybet'
                                                  '-england.png"]')
    image_element.click()


#
#
def check_virtuals():
    try:
        # Wait for the element to be clickable and then click it
        xpath = "//div[contains(@class, 'grid-left playlist-descripction') and text()=' England League ']"
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()

    except Exception as e:
        print(f"Error: {e}")

# ================ WAIT FUNCTION ====================#
def wait(time_amount):
    time.sleep(time_amount)


#
#

# ============================ OPEN CHROME ======================= #
driver = webdriver.Chrome()

#
#

# =================== GO TO REALNAPS.COM SITE ==================== #
MAX_RETRIES = 3
retry_count = 0

while retry_count < MAX_RETRIES:
    try:
        driver.get(VISUALS_SITE)
        break  # If successful, exit the loop
    except TimeoutException:
        print(f"TimeoutException occurred. Retrying... (Attempt {retry_count + 1} of {MAX_RETRIES})")
        retry_count += 1

#
#

wait(5)

# ==================== CLICK NIGERIA ================== #
click_nigeria()

wait(4)

# ============== LOCATE SCHEDULED VIRTUALS ============ #
locate_scheduled_virtuals()

wait(10)

# ============== ALLOWING THE WEBPAGE TO LOAD TO GET WEB VALUES =========== #
WebDriverWait(driver, 20)
check_bet_status()
wait(1)

# # ========================= GO TO NEW TAB ============================= #
driver.execute_script("window.open('', '_blank');")
driver.switch_to.window(driver.window_handles[1])
driver.get(SPORTY_BET)

WebDriverWait(driver, 120)

check_virtuals()

wait(40)

# TACKLE ERRORS


# class countdown_stabilized:
#     def __init__(self, locator):
#         self.locator = locator
#
#     def __call__(self, driver):
#         element = driver.find_element(*self.locator)
#         initial_value = element.text
#         time.sleep(4)
#         final_value = driver.find_element(*self.locator).text
#         return initial_value == final_value
#
#
# def click_nigeria():
#     nigeria_logo = driver.find_element(By.ID, "Nigeria")
#     nigeria_logo.click()
#
#
# def locate_scheduled_virtuals():
#     image_element = driver.find_element(By.XPATH, '//img[@src="https://realnaps.com/signal/premium/images/sportybet'
#                                                   '-england.png"]')
#     image_element.click()
#
#
# def get_bet_value():
#     try:
#         # Wait for the element to be present and retrieve its text
#         hm1_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "hm1")))
#         hm1 = hm1_element.text
#
#         aw1_element = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID, "aw1")))
#         aw1 = aw1_element.text
#
#         hm2_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "hm2")))
#         hm2 = hm2_element.text
#
#         aw2_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "aw2")))
#         aw2 = aw2_element.text
#
#         hm3_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "hm3")))
#         hm3 = hm3_element.text
#
#         aw3_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "aw3")))
#         aw3 = aw3_element.text
#
#         if hm1 != "loading":
#             wait(1)
#             if hm1 == "":
#                 wait(10)
#             print("Value without loading in the div element:\n", hm1, aw1)
#         else:
#             if hm1 == "" or hm1 == "loading":
#                 WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.ID, "loading-overlay")))
#                 wait(10)
#             wait(10)
#             print("Value with loading in the div element:", hm1)
#
#     except Exception as e:
#         print(f"Error message occurred", e)
#
#     finally:
#         wait(1)
#
#
# def check_bet_status():
#     bet_status = driver.find_element(By.CSS_SELECTOR, '.col.text-center.betStatus')
#     bet_value = bet_status.text
#
#     # Use regular expression to check if the value is numeric
#
#     if bet_value.replace(':', '').isdigit():
#         try:
#             # Wait until the countdown timer stabilizes (stops changing)
#             countdown_locator = (By.CLASS_NAME, "col.text-center.betStatus")
#             WebDriverWait(driver, 100).until(countdown_stabilized(countdown_locator))
#
#             # Get the final value when the countdown timer has stabilized
#             final_value = driver.find_element(*countdown_locator).text
#             get_bet_value()
#
#         except Exception as e:
#             close_button = WebDriverWait(driver, 60).until(
#                 EC.element_to_be_clickable((By.CLASS_NAME, "close"))
#             )
#             close_button.click()
#             get_bet_value()
#
#         finally:
#             wait(1)
#     else:
#         get_bet_value()
#
#
# def login_sporty_bet():
#     input_number = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Mobile Number"]')
#     wait(1)
#     input_number.send_keys("7034282805")
#
#     wait(1)
#     input_password = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]')
#     wait(1)
#     input_password.send_keys("Chukwudum1@")
#
# login_button = driver.find_element(By.XPATH, '//span[@data-cms-key="log_in" and @data-cms-page="common_functions"]')
#
#     login_button.click()
#     driver.switch_to.default_content()
#     wait(60)
#
#
# # #playlist_13163 > li > div > div.gr-col.content-left.list-group-item--text > div > div
# # //*[@id="playlist_13163"]/a
# # //*[@id="game_league"]/a
#
# def check_virtuals():
#     wait(5)
#     css_selector = '.gr-col.content-left.list-group-item--text div.grid-left.playlist-descripction'
#     click_wait = WebDriverWait(driver, 60)
#     england_element = click_wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
#     print("?")
#     england_element.click()
#
#
# def wait(time_amount):
#     time.sleep(time_amount)
#
#
# #
# #
#
# # =============== GO TO CHROME ================= #
# driver = webdriver.Chrome()
# # =========== WAIT =========== #
#
#
# wait(1)
#
# # ====================== GO TO THE VISUALS_SITE ===================== #
#
# driver.get(VISUALS_SITE)
#
# # =========== WAIT =========== #
#
# wait(2)
#
# # ================ CLICK COUNTRY ================== #
#
# click_nigeria()
#
# # =========== WAIT =========== #
#
# wait(2)
#
# # ======== click on the scheduled_visual ======== #
#
# locate_scheduled_virtuals()
#
# # =========== WAIT =========== #
#
# wait(1)
#
# # ============ GET THE REQUIRED DATA ============= #
#
# check_bet_status()
#
# # =========== WAIT =========== #
#
# wait(1)
#
# # ========================= GO TO NEW TAB ============================= #
# driver.execute_script("window.open('', '_blank');")
# driver.switch_to.window(driver.window_handles[1])
# driver.get(SPORTY_BET)
#
# wait(5)
# check_virtuals()
# wait(15)
# # 234 7034282805
# # Chukwudum1@
#

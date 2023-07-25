from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def login(driver, username, password):
    username_input = driver.find_element_by_xpath(
        '//input[contains(@aria-label,"Phone number, username, or email")]'
    )
    password_input = driver.find_element_by_xpath(
        '//input[contains(@aria-label,"Password")]'
    )

    username_input.send_keys(username)
    password_input.send_keys(password)

    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    print("login Successful")
    # Handle any additional steps after login if needed
    try:
        time.sleep(2)
        dialog = driver.find_element_by_xpath(
            "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]"
        )
        dialog.click()
        print("notifications turned off")
    except:
        pass


def search_user(driver, username):
    search_tag = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a/div"
    )
    search_tag.click()
    search_input = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/input"
    )

    search_input.send_keys(username)

    time.sleep(5)
    search_result = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]"
    )
    search_result.click()


def collect_user_data(driver):
    try:
        name_element = driver.find_element_by_xpath(
            "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/div[1]/span"
        )
    except:
        name_element = None
        print("no name given")
        pass
    try:
        bio_element = driver.find_element_by_xpath(
            "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/div[3]/h1"
        )
    except:
        bio_element = None
        print("no bio Given")
        pass
    posts_element = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span"
    )
    try:
        name = name_element.text
        nameS.append(name)
        bio = bio_element.text
        bioS.append(bio)
    except:
        name = name_element
        bio = bio_element
        pass
    posts = int(posts_element.text.replace(",", ""))
    return name, bio, posts


def collect_post_data(driver):

    # Click the first post
    first_post = driver.find_element_by_xpath("//article/div[1]/div/div[1]/div[1]")
    first_post.click()

    for _ in range(posts):
        # Collect caption
        try:
            caption_element = driver.find_element_by_xpath(
                "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/h1"
            )
            caption = caption_element.text
            captionS.append(caption)
        except:
            caption = None
            print("no caption offered")

        # Collect comments
        comment_elements = driver.find_elements_by_xpath(
            "//ul[contains(@class,'_a9ym')]/div/li"
        )
        for comment_element in comment_elements:
            comment_text = comment_element.find_element_by_tag_name("span")
            comment_text.text
            commentsS.append(comment_text.text)
            try:
                moreComments = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/li/div/button"
                )
                moreComments.click()
                print("more buttons clicked")
            except:
                pass

        # Move to the next post
        sc = driver.find_element_by_tag_name("body")
        sc.send_keys(Keys.ARROW_RIGHT)

    return


# data Variables

nameS = []
bioS = []
captionS = []
commentsS = []


# Main program
username = "romeoclientandjohn@gmail.com"
password = "Irene123."
search_username = input("Enter the name of the person to search ")

options = Options()
options.add_argument("--headless")


driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
try:
    driver.get("https://www.instagram.com")
    driver.implicitly_wait(5)

    login(driver, username, password)

    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.aOOlW.HoLwm"))
        ).click()
    except:
        pass

    search_user(driver, search_username)

    name, bio, posts = collect_user_data(driver)

    posts = posts if posts else 0  # Handle case when posts are not available

    collect_post_data(driver)

    # create csv file
    data = []
    max_length = max(len(nameS), len(bioS), len(captionS), len(commentsS))

    for i in range(max_length):
        row = [
            nameS[i] if i < len(nameS) else "",
            bioS[i] if i < len(bioS) else "",
            captionS[i] if i < len(captionS) else "",
            commentsS[i] if i < len(commentsS) else "",
        ]
        data.append(row)

    with open("data.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Bio", "Captions", "Comments"])
        writer.writerows(data)

finally:
    driver.quit()

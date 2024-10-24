# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# import time
# import pandas as pd
# from utils_consts import *
# import os 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from xpath import *



# chrome_options = webdriver.ChromeOptions()
# # Enable headless mode
# chrome_options.add_argument("--headless=new")
# # Set user-agent
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
# # Additional options
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# # Set the window size to full-screen (1920x1080 or adjust as needed)
# #chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_argument("--window-size=1920x1080")
# chrome_options.add_argument('--disable-gpu')
# driver = webdriver.Chrome(options=chrome_options)
# # No need for driver.maximize_window() in headless mode as we have set the window size
# driver.maximize_window()


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from xpath import *
from utils_consts import *
import time


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--log-level=1")

# # chrome_options.binary_location= 'new_chromedriver'
# driver = webdriver.Chrome(options=chrome_options)
# driver.maximize_window()

def post_process_results(term, tenders, term_tenders):
    if not term_tenders:
        print(f"No results found for term: {term}")
        return

    records = []
    for key, values in tenders.items():
        for value in values:
            record = {'key': key}
            for i, v in enumerate(value):
                record[f'value_{i+1}'] = v
            records.append(record)

    df = pd.DataFrame(records)
    df.columns = [
        "search_term", "publish_date", "competition_type", "subject", "stakeholder", 
        "details", "main_activity", "time_left", "reference_number", "questions_deadline", 
        "proposal_deadline", "proposal_start_date", "useless_text", 
        "competition_documents_cost", "link"
    ]
    
    df = df.drop(columns=["details", "useless_text"])
    df['publish_date'] = df['publish_date'].str.replace('تاريخ النشر :', '')
    df["publish_date"] = pd.to_datetime(df["publish_date"])
    df['main_activity'] = df['main_activity'].str.replace('النشاط الأساسي', '')
    df['reference_number'] = df['reference_number'].str.replace('الرقم المرجعي', '')
    df['questions_deadline'] = df['questions_deadline'].str.replace('اخر موعد لإستلام الاستفسارات', '')
    df['proposal_deadline'] = df['proposal_deadline'].str.replace('آخر موعد لتقديم العروض', '')
    df['proposal_start_date'] = df['proposal_start_date'].str.replace('تاريخ ووقت فتح العروض', '')

    df.to_csv(f"tenders_{term}.csv", index=False, encoding='utf-8-sig')
    return df

def get_tenders_from_page(term_tenders,driver):
    parent_tender_divs = driver.find_element(By.XPATH, '//*[@id="cardsresult"]/div[1]')
    child_tender_divs = parent_tender_divs.find_elements(By.CLASS_NAME, "row")
    links = parent_tender_divs.find_elements(By.XPATH,"//a[contains(text(), 'التفاصيل')]")
    links_arr = [el.get_property("href") for el in links]
    
    filtered_child_divs = []
    for div in child_tender_divs:
        if 'الرقم المرجعي' in div.text and 'تاريخ النشر' in div.text:
            filtered_child_divs.append(div)
    i = 0
    for div in filtered_child_divs:
        el = div.text.split('\n')
        el.append(links_arr[i])
        term_tenders.append(el)
        if 'تاريخ ووقت فتح العروض' not in div.text:
            el.insert(-3, "N/A")            
        i += 1
        
def start_parsing(term, tenders, term_tenders,driver):
    current_page = 1
    try:
        pages_elements = driver.find_element(By.XPATH, '//*[@id="cardsresult"]/div[2]/div/nav/ul')
    except Exception as e:
        print(f"No pagination found, either no tenders or a single page for term: {term}")
        get_tenders_from_page(term_tenders,driver)  
        if term_tenders:  
            tenders[term] = term_tenders
            post_process_results(term, tenders, term_tenders)
        else:
            print(f"No tenders found for term: {term}")
        return

    pages = [int(el) for el in pages_elements.text.split('\n') if el.isdigit()]
    pages_passed = {0}
    print(f"Parsing results for term: {term}")

    while len(pages) > 0:
        print("Current page: ", current_page)
        pages_passed.add(current_page)
        print('--')
        print("Pages detected", pages)
        
        if current_page in pages:
            pages_elements = driver.find_element(By.XPATH, '//*[@id="cardsresult"]/div[2]/div/nav/ul')
            buttons = pages_elements.find_elements(By.TAG_NAME, 'a')
            
            for button in buttons:
                if int(button.text) == current_page:
                    print(button.text)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(4)
                    button.click()
                    print(current_page, " clicked")
                    time.sleep(4)
                    pages_elements = driver.find_element(By.XPATH, '//*[@id="cardsresult"]/div[2]/div/nav/ul')
                    pages = [int(el) for el in pages_elements.text.split('\n') if el.isdigit()]
        
        get_tenders_from_page(term_tenders,driver)
        pages = set(pages) - pages_passed
        print("pages: ", pages)
        current_page += 1

    if term_tenders:  
        tenders[term] = term_tenders
        post_process_results(term, tenders, term_tenders)
    else:
        print(f"No tenders found for term: {term}")

    return

# def setup_search(term, tenders, term_tenders, main_activityy):
#     print("getting etimad website..")
#     website_url = "https://tenders.etimad.sa/Tender/AllTendersForVisitor?PageNumber=1"
#     driver.get(website_url)
#     print("got etimad website successfully!!!")
#     # expand search
#     search_button = driver.find_element(By.XPATH, "//*[@id='searchBtnColaps']")  # Replace 'button_id' with the actual ID or XPath of the button
#     search_button.click()

#     # click choose tender status
#     driver.execute_script("window.scrollBy(0, 500);")
#     time.sleep(4)
#     status_button = driver.find_element(By.XPATH,"//*[@id='basicInfo']/div/div[2]/div/div/button")                        
#     status_button.click()

#     # choose active tenders
#     driver.execute_script("window.scrollBy(0, 50);")
#     time.sleep(4)
#     span_element = driver.find_element(By.XPATH,'//*[@id="basicInfo"]/div/div[2]/div/div/div/ul/li[2]/a')                                                                     
#     span_element.click()

#     driver.execute_script("window.scrollBy(0, 175);")
#     time.sleep(4)
#     main_activity = driver.find_element(By.XPATH, '//*[@id="basicInfo"]/div/div[4]/div/div/button')
#     main_activity.click()

    
#     # type اتص to filter results
#     input_element = driver.find_element(By.XPATH, '//*[@id="basicInfo"]/div/div[4]/div/div/div/div/input')
#     input_element.clear()
#     input_element.send_keys(str(main_activityy))

#     option_xpath = get_xpath_for_option(main_activityy)
#     if option_xpath != "Option not found in the dropdown list.":
#         # Choose the selected option
#         selected_option_element = driver.find_element(By.XPATH, option_xpath)
#         selected_option_element.click()
#     else:
#         print("Error: Selected option not found in the dropdown list.")
#         return
    

#     driver.execute_script("window.scrollBy(0, 50);")

#     input_element = driver.find_element(By.XPATH, '//*[@id="txtMultipleSearch"]')
#     input_element.clear()
#     input_element.send_keys(term)

#     # finally hit search
#     driver.execute_script("window.scrollBy(0, 35);")
#     final_search_button = driver.find_element(By.XPATH,'//*[@id="searchBtn"]') 
#     final_search_button.click()
#     time.sleep(4)
#     res = start_parsing(str(term), tenders, term_tenders)
#     # print("~~",res)
#     if res == 'NoSuchElementException':
#         return
#     else:
#         tenders[term] = term_tenders
#         post_process_results(term, tenders, term_tenders)
def setup_search(term, tenders, term_tenders, main_activityy):
    # Each request gets its own WebDriver instance
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    try:
        print("getting etimad website..")
        website_url = "https://tenders.etimad.sa/Tender/AllTendersForVisitor?PageNumber=1"
        driver.get(website_url)
        print("got etimad website successfully!!!")
        
        # expand search
        search_button = driver.find_element(By.XPATH, "//*[@id='searchBtnColaps']")
        search_button.click()

        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(4)
        status_button = driver.find_element(By.XPATH,"//*[@id='basicInfo']/div/div[2]/div/div/button")                        
        status_button.click()

        driver.execute_script("window.scrollBy(0, 50);")
        time.sleep(4)
        span_element = driver.find_element(By.XPATH,'//*[@id="basicInfo"]/div/div[2]/div/div/div/ul/li[2]/a')                                                                     
        span_element.click()

        driver.execute_script("window.scrollBy(0, 175);")
        time.sleep(4)
        main_activity = driver.find_element(By.XPATH, '//*[@id="basicInfo"]/div/div[4]/div/div/button')
        main_activity.click()

        input_element = driver.find_element(By.XPATH, '//*[@id="basicInfo"]/div/div[4]/div/div/div/div/input')
        input_element.clear()
        input_element.send_keys(str(main_activityy))

        option_xpath = get_xpath_for_option(main_activityy)
        if option_xpath != "Option not found in the dropdown list.":
            selected_option_element = driver.find_element(By.XPATH, option_xpath)
            selected_option_element.click()
        else:
            print("Error: Selected option not found in the dropdown list.")
            return

        driver.execute_script("window.scrollBy(0, 50);")
        input_element = driver.find_element(By.XPATH, '//*[@id="txtMultipleSearch"]')
        input_element.clear()
        input_element.send_keys(term)

        driver.execute_script("window.scrollBy(0, 35);")
        final_search_button = driver.find_element(By.XPATH,'//*[@id="searchBtn"]') 
        final_search_button.click()
        time.sleep(4)

        start_parsing(str(term), tenders, term_tenders, driver)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

def get_terms_files(keywords, main_activity):
    for term in keywords:
        print("term: ", term)
        term = term.strip()
        if term:
            tenders = {}
            term_tenders = []
            setup_search(str(term), tenders, term_tenders, str(main_activity))


def agg_files():
    directory = os.getcwd()
    dfs = []

    # Loop through files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            # Read the CSV file into a DataFrame and append to the list
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            dfs.append(df)

    # If no CSV files found, return early
    if not dfs:
        print("No CSV files found.")
        return

    # Concatenate all DataFrames into one
    combined_df = pd.concat(dfs, axis=0, ignore_index=True)
    
    print("length of the dataframe before filtering: ", len(combined_df))


    # Remove duplicates and invalid entries
    combined_df = combined_df.drop_duplicates(subset=["reference_number"])
    combined_df = combined_df[combined_df["search_term"] != "search_term"]
    combined_df = combined_df.sort_values(by=['publish_date', 'stakeholder', 'subject'])
    
    # Filter out rows based on excluded patterns
    pattern = '|'.join(to_exclude)
    filtered_df = combined_df[~combined_df['subject'].str.contains(pattern, na=False)]
    
    print("length of the dataframe after filtering: ", len(filtered_df))

    # Save the filtered results to both CSV and Excel
    today_date = pd.to_datetime('today').strftime('%Y-%m-%d')
    filtered_csv = f"tenders_{today_date}_filtered.csv"
    filtered_excel = f"tenders_{today_date}_filtered.xlsx"
    
    filtered_df.to_csv(filtered_csv, index=False, encoding='utf-8-sig')
    filtered_df.to_excel(filtered_excel, index=False)
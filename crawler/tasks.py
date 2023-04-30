from __future__ import absolute_import
import pymongo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import requests
import json
import random
import datetime
from lxml import html

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

#from crawler.start_celery import app
CPANEL_IP = 'http://3.130.9.101'

def check_if_ip_blocked(page_source):
    """
    This check if the ip is blocked or not
    :param page_source:
    :return:
    """
    doc = html.fromstring(page_source)
    title = doc.xpath("//title/text()")
    text = '404 Forbidden'
    if title:
        if text in title[0]:
            return True
    return False


def start_driver():
    """
    This function start  driver with relevent settings
    :return:
    """
    SELENIUM_DRIVER_PATH = "/home/sree/PEM/chromedriver"
    # SELENIUM_DRIVER_PATH = "/home/jithin/Project/KredibleCrawler/chrome_driver/chromedriver_linux"
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1420,1080')
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(SELENIUM_DRIVER_PATH,chrome_options=chrome_options)
    print("Chrome driver initalized")
    return driver


def check_exists_by_xpath(driver, xpath):
    """
    This function check if xpath exist
    :param driver:
    :param xpath:
    :return:
    """
    try:
        driver.find_element("xpath",xpath)
    except NoSuchElementException:
        return False
    return True




def get_all_cin():
    """
    This function get all CIN in database.
    :return:
    """
    cin_list = requests.get(url=CPANEL_IP + '/api/mca_info/cinList')
    cin_list = json.loads(cin_list.json())
    cin = []
    for i in cin_list:
        cin.append(i.get("company_cin"))
    return cin

#@app.task()
def searching_cin(SELENIUM_GRID_IP, cin,company_name, data_push):
    """
    This function search for cin in MCA website
    :param cin:
    :param data_push:
    :return:
    """
    #driver = start_driver()
    res=False
    try:
        driver = start_driver()
        #driver = start_driver_new(SELENIUM_GRID_IP)
        main_url = 'https://www.mca.gov.in/mcafoportal/viewPublicDocumentsFilter.do'   
        #driver.get('https://www.google.com/')
        driver.get(main_url)
        if check_if_ip_blocked(driver.page_source):
            raise Exception('Ip Blocked')
        time.sleep(random.randint(8, 12))
        ckecks = driver.find_element("xpath",'//input[@id="cinChk"]')
        ckecks.click()
        time.sleep(random.randint(0, 2))
        cin_input = driver.find_element("xpath",'//input[@id="cinFDetails"]')
        time.sleep(random.randint(0, 2))
        cin_input.send_keys(cin)
        time.sleep(random.randint(3, 8))
        driver.find_element("xpath",'//input[@id="viewDocuments_0"]').click()
        time.sleep(random.randint(0, 9))
        if check_exists_by_xpath(driver, '//a[@class="dashboardlinks"]'):
            res = go_to_detailed_page(cin, company_name,driver, data_push)
        else:
            res = False
            print("No details found")
        driver.quit()
    except Exception as ex:
        print("Exception : ", ex)
        driver.quit()

    if res:
        with open('cin_sucess.txt',"a") as f:
          f.write("\n"+str(cin))
    else:
       with open('cin_failure.txt',"a") as f:
          f.write("\n"+str(cin))


    return res


def start_driver_new(SELENIUM_GRID_IP):
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    #chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Remote("http://" + SELENIUM_GRID_IP + ":4444/wd/hub", options=chrome_options)
    print("Driver initated ...")
    return driver


def process_text(text):
    """
    This function cleans the text.
    :param text:
    :return:
    """
    if type(text) == list:
        text = text[0]
    text = text.replace("\n", "")
    text = text.replace("\t", "")
    return text


def get_year():
    """
    This function return current year
    :return:
    """
    return str(datetime.datetime.now().year)


def close_popup(driver):
    """
    This function close the pop up.
    :param driver:
    :return:
    """
    if check_exists_by_xpath(driver, '//a[@id="msgboxclose"]'):
        driver.find_element("xpath",'//a[@id="msgboxclose"]').click()


def get_annual_finance(driver):
    """
    This function return current year annual finance data.
    :param driver:
    :return:
    """
    time.sleep(random.randint(1, 3))
    driver.find_element("xpath","//select[@name='categoryName']/option[text()='Annual Returns and Balance Sheet eForms']").click()
    time.sleep(random.randint(1, 3))
    xpath_str = "//select[@name='finacialYear']/option[text()='" + get_year()  + "']"
    driver.find_element("xpath",xpath_str).click()
    time.sleep(random.randint(1, 3))
    driver.find_element("xpath","//input[@id='viewCategoryDetails_0']").click()
    time.sleep(random.randint(0, 9))
    finance_response, finance_doc_status = parse_doc(driver)
    return finance_response, finance_doc_status


def get_eform(driver):
    """
    This function return current year eform data.
    :param driver:
    :return:
    """
    time.sleep(random.randint(1, 3))
    driver.find_element("xpath","//select[@name='categoryName']/option[text()='Other eForm Documents']").click()
    time.sleep(random.randint(1, 3))
    xpath_str = "//select[@name='finacialYear']/option[text()='" + get_year() + "']"
    driver.find_element("xpath",xpath_str).click()
    time.sleep(random.randint(1, 3))
    driver.find_element("xpath","//input[@id='viewCategoryDetails_0']").click()
    time.sleep(random.randint(0, 9))
    eform_response, eform_doc_status = parse_doc(driver)
    return eform_response, eform_doc_status


def get_other_attachments(driver):
    """
    This function return current year other attachments data.
    :param driver:
    :return:
    """
    time.sleep(random.randint(1, 3))
    driver.find_element("xpath","//select[@name='categoryName']/option[text()='Other Attachments']").click()
    time.sleep(random.randint(1, 3))
    xpath_str = "//select[@name='finacialYear']/option[text()='" + get_year() + "']"
    driver.find_element("xpath",xpath_str).click()
    time.sleep(random.randint(1, 3))
    driver.find_element("xpath","//input[@id='viewCategoryDetails_0']").click()
    time.sleep(random.randint(0, 9))
    other_attachments_response, other_attachments_a_doc_status = parse_doc(driver)
    return other_attachments_response, other_attachments_a_doc_status


def parse_doc(driver):
    """
    This function parse table data .
    :param driver:
    :return:
    """
    try:
        doc = html.fromstring(driver.page_source)
        rows = doc.xpath("//table[@id='results']/tbody/tr/td")
        if not rows:
            close_popup(driver)
            return 'No documents are available for the selected category', False
        row_count = 0
        respose = ""
        for row in rows:
            text = row.xpath('./text()')
            respose = respose + process_text(text) + " :"
            row_count = row_count + 1
            if row_count % 2 == 0:
                respose = respose[:-1]
                respose = respose + "<br>"
        return respose, True
    except Exception as e:
        print("Exception in Fetching Data:" + str(e))
    close_popup(driver)
    return 'No documents are available for the selected category', False


def save_to_api(cin, data):
    """
    This function save the crawled data to database
    :param cin:
    :param data:
    :return:
    """
    url = CPANEL_IP + "/api/mca_info/cinMarked/"
    payload = "cinNumer=" + cin + "&doc_present=" + str(data.get("finance").get("present")) + "&doc_information=" + str(
        data.get("finance").get("response")) + \
              "&other_eform_documents_present=" + str(
        data.get("eform").get("present")) + "&other_eform_documents_information=" + str(
        data.get("eform").get("response"))
    #       + \
    #       "&other_attachment_documents_present=" + str(
    # data.get("attachments").get("present")) + "&other_attachment_documents_information=" + str(
    # data.get("attachments").get("response"))

    headers = {
        'content-type': "application/x-www-form-urlencoded",
    }
    r = requests.post(url, data=payload, headers=headers)
    print(r.status_code)
    print(cin)
    if r.status_code == 200:
        return True
    else:
        return False

def clean_finance_upload_data(data):
    data = data.strip()
    processed_data = {}
    items = data.split("<br>")
    if items:
        for item in items:
            if len(item) > 1:
                year = item.split(":")[-1]
                attachment = item.split(":")[0]
                processed_data.update({year.strip(): attachment.strip()})
    return processed_data

def save_to_mongodb(cin, company_name,data,type):
    """
    This function save the crawled data to database
    :param cin:
    :param data:
    :return:
    """
    try:
        new_finance_flag = False
        data = clean_finance_upload_data(data)
        if list(data.keys())[0] == 'No documents are available for the selected category':
            return False
        connection = pymongo.MongoClient('mongodb://crawler_admin:PassKred12@18.116.5.193:27017/crawler')
        database = connection["crawler"]
        collection = database["mca_dev"]
        query = {"cin": cin}
        get_old_data = collection.find_one(query)
        if get_old_data:
            old_type_data = get_old_data.get(type)
            if old_type_data:
                #collection.delete_one(query)
                for k, v in data.items():
                    if old_type_data.get(k) is None:
                        new_finance_flag = True
                        #send alert
                        alert_flag = send_mail("Alert ! : MCA "+type+" Data added " + company_name,
                                               "There is a new "+type+" data Added in MCA website: " + v)
                        print("Email Alert Send") if alert_flag else None
            else:
                #collection.delete_one(query)
                alert_flag = send_mail("Alert ! : MCA " + type + " Data added " + company_name,
                                       "There is a new " + type + " data Added in MCA website: " + ','.join(
                                           list(data.values())))
                print("Email Alert Send") if alert_flag else None
            data_to_save = get_old_data
        else:
            data_to_save = {}
            new_finance_flag = True
            alert_flag = send_mail("Alert ! : MCA " + type + " Data added " + company_name,
                                   "There is a new " + type + " data Added in MCA website: " + ','.join(list(data.values())))
            print("Email Alert Send") if alert_flag else None
        data_to_save.update({"cin": cin, type: data})
        # print("DATA:",data_to_save)
        #collection.insert_one(data_to_save)
    except Exception as ex:
        print("EX:", ex)
        return False
    return  new_finance_flag


def send_mail(subject, message):
    with open('config/google.json', "r") as f:
        email_details = json.load(f)
    email = email_details.get("gmail").get("username")
    password = email_details.get("gmail").get("password")
    with open('config/alert.json', "r") as f:
        alert_to = json.load(f)
    send_to_email = alert_to.get("gmail") # for whom
    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = ", ".join(send_to_email)
    msg["Subject"] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, send_to_email, text)
    server.quit()
    return True

def go_to_detailed_page(cin,company_name, driver, data_push):
    """
    This function go to the detailed page.
    :param cin:
    :param driver:
    :param data_push:
    :return:
    """
    driver.find_element("xpath",'//a[@class="dashboardlinks"]').click()
    if check_if_ip_blocked(driver.page_source):
        raise Exception('Ip Blocked')
    time.sleep(random.randint(0, 9))
    finance_response, finance_doc_status = get_annual_finance(driver)
    new_fileupload_flag = save_to_mongodb(cin, company_name,finance_response,"finance")
    print("FINANCE NEW FILE :",new_fileupload_flag)
    eform_response, eform_doc_status = get_eform(driver)
    new_fileupload_flag = save_to_mongodb(cin, company_name,eform_response, "eform")
    print("EFORM NEW FILE :",new_fileupload_flag)
    data = {
        "finance": {"present": finance_doc_status, "response": finance_response},
        "eform": {"present": eform_doc_status, "response": eform_response},
        # "attachments": {"present": other_attachments_a_doc_status, "response": other_attachments_response},
    }
    if data_push:
        res = save_to_api(cin, data)
    return res



#searching_cin('SELENIUM_GRID_IP', 'U01409PN2017PTC172439', True)
# searching_cin('SELENIUM_GRID_IP', 'U74140HR2015FTC055568', True)
# searching_cin('SELENIUM_GRID_IP', 'U52202TG2020PTC139550','CHIFU AGRITECH PRIVATE LIMITED', False)
searching_cin('SELENIUM_GRID_IP', 'U80903DL2012PTC236595','CHIFU AGRITECH PRIVATE LIMITED', False)
#add company name in task run

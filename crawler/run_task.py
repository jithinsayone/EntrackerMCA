from crawler.tasks import searching_cin
import time
import json
import psutil
import datetime
import requests

CPANEL_IP = 'http://3.130.9.101'


def get_all_cin():
    """
    This function get all CIN in database.
    :return:
    """
    cin_list = requests.get(url=CPANEL_IP + '/api/mca_info/cinList')
    cin_list = json.loads(cin_list.json())
    cin = []
    for i in cin_list:
        cin.append([i.get("company_cin"), i.get("company_name")])
    return cin


def get_error_cin():
    """
    This function get all CIN in database.
    :return:
    """
    cin_list = requests.get(url=CPANEL_IP + '/api/mca_info/ErrorcinList')
    cin_list = json.loads(cin_list.json())
    cin = []
    for i in cin_list:
        cin.append([i.get("company_cin"), i.get("company_name")])
    return cin


def check_time():
    hour = int(datetime.datetime.now().time().strftime('%H'))
    if hour >= 17:
        return True
    else:
        return False


def wait_loop():
    while True:
        print("sleeping to free memory ...")
        time.sleep(120)
        if psutil.virtual_memory().percent < 40.0:
            break


def run_crawler(cins, run_loop):
    roatate_count = 0

    while True:
        for cin in cins:
            print("index count:", cins.index(cin))
            actual_cin = str(cin[0].strip())
            company_name = str(cin[1].strip())
            searching_cin.apply_async(args=['18.116.5.193', actual_cin, company_name, True],
                                      queue='mca_crawler',
                                      routing_key='mca_crawler.website'
                                      )
            #print("next")
            if psutil.virtual_memory().percent > 90.0:
                print("Memory Threshold ....")
                wait_loop()
            if cins.index(cin) % 13 == 0 and cins.index(cin) != 0:
                time.sleep(8)
        if not run_loop:
            break
        print("Waiting for Next loop ...")
        print("TIME: ", datetime.datetime.now())
        if check_time():
            print("Done For the Day ...")
            break
        time.sleep(1200)
        roatate_count = roatate_count + 1
        if roatate_count % 2 != 0:
            print("Swtiching CINS to Error ...")
            cins = get_error_cin()
        else:
            print("Switching CINS to Normal")
            cins = get_all_cin()


if __name__ == '__main__':
    choice = int(input("ENTER Choice \n 1. Daily Run \n 2. Error CIN Crawl \n - "))
    if choice == 1:
        cins = get_all_cin()
        # cins = list(set(cins))
        run_crawler(cins, True)
    else:
        cins = get_error_cin()
        # cins = list(set(cins))
        run_crawler(cins, False)

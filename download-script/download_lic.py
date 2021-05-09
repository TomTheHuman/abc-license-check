import os
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

def get_report( report):
    '''This function checks for the presence of, downloads, and renames the status requested report from ABC'''


    # Declare report data - Index 0: data file name, Index 1: report URL
    report_data = {'status changes': ['report_status_changes.csv', 'status-changes'], 'issued licenses': ['report_issued_licenses.csv', 'issued-licenses'], 'new applications': ['report_new_applications.csv', 'new-applications']}

    # Delete existing report
    if path.exists(data_path + report_data[report][0]):
        os.remove(data_path + report_data[report][0])

    # Get status changes report
    browser.get('https://www.abc.ca.gov/licensing/licensing-reports/' + report_data[report][1])

    # Locate and click download button
    try:
        python_button = browser.find_element(By.XPATH, '//span[text()="Download Report (CSV)"]')
        python_button.click()
    except:
        print(f'CSV report not available for {report}')

    # Rename and move file
    if path.exists(download_path + 'CA-ABC-LicenseReport.csv'):
        os.rename(download_path + 'CA-ABC-LicenseReport.csv', data_path + report_data[report][0])

def get_browser():
    # Declare Firefox profile
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", download_path)

    # Need to figure out why prompt still appears
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk" , "text/csv")
    profile.set_preference("browser.helperApps.neverAsk.openFile" , "text/csv")
    profile.set_preference("browser.helperApps.alwaysAsk.force", False);

    return webdriver.Firefox(firefox_profile=profile)

if __name__ == '__main__':
    
    # Declare path variables
    download_path = '/home/tomthehuman/Desktop/dev/abc-license-check/download-script/download/'
    data_path = '/home/tomthehuman/Desktop/dev/abc-license-check/download-script/data/'


    browser = get_browser()

    # Handle reports
    get_report('status changes')
    get_report('issued licenses')
    get_report('new applications')


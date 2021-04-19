from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


if __name__ == '__main__':
    
    profile = webdriver.FirefoxProfile()
    profile.set_preference("broswer.download.folderList", 2)
    profile.set_preference("broswer.download.manager.showWhenStarting", False)
    profile.set_preference("broswer.download.dir", '/home/tomthehuman/Desktop/dev/abc-license-check/download-script/data/')

    # Need to figure out why prompt still appears
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk" , "")
    profile.set_preference("browser.helperApps.neverAsk.openFile" , "")
    profile.set_preference("browser.helperApps.alwaysAsk.force", False);


    browser = webdriver.Firefox(firefox_profile=profile)
    browser.get('https://www.abc.ca.gov/licensing/licensing-reports/status-changes/')

    # click radio button
    python_button = browser.find_element(By.XPATH, '//span[text()="Download Report (CSV)"]')
    python_button.click()
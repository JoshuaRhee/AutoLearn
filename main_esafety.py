import chromedriver_autoinstaller
import easygui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def solve_ox_quiz():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "quiz-type-1-o"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "quiz-type-1-submit"))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next"))).click()

def solve_test():
    for i, quiz in enumerate(driver.find_element(By.ID,"quiz-type-2").find_elements(By.XPATH, '*')):
        driver.find_element(By.ID,"quiz-type-2").find_elements(By.XPATH, '*')[i].click()
    driver.find_element(By.CLASS_NAME, "next").click()

def pass_summary():
    driver.find_element(By.CLASS_NAME, "next").click()
    
if __name__ == '__main__':
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    driver.get('http://kriss.esafetykorea.or.kr/')
    
    flag_login_again = True
    while(flag_login_again):
        id = easygui.enterbox('접속 아이디(사번)를 입력해주세요.','[AutoLearn] developed by. JHR')
        if id:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mb_id"))).clear()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mb_id"))).send_keys(id)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mb_pw"))).clear()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mb_pw"))).send_keys(id)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-btn"))).click()
            try:
                driver.switch_to.alert.accept()
            except:
                flag_login_again = False
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-controls"))).find_elements(By.XPATH, "//button")[2].click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-gray-gd"))).click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "period-one")))
                for i, period in enumerate(driver.find_elements(By.CLASS_NAME, "period-one")):
                    if not "완료" in period.text:
                        period.find_element(By.CLASS_NAME,"lecture_view_btn").click()
                        driver.switch_to.window(driver.window_handles[-1])
                        try:
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "confirm-open"))).click()
                        except:
                            driver.find_element(By.ID,"play-pause").click()
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "volume-control"))).click()
                        while(True):
                            if bool(driver.find_elements(By.ID,"quiz-type-1")):
                                solve_ox_quiz()
                                time.sleep(1)
                            elif bool(driver.find_elements(By.ID,"quiz-type-2")):
                                solve_test()
                                time.sleep(1)
                            elif bool(driver.find_elements(By.ID,"quiz-type-3")):
                                pass_summary()
                                time.sleep(1)
                            elif bool(driver.find_elements(By.ID,"period-move")):
                                driver.find_element(By.ID,"period-move").click()
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "volume-control"))).click()
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "play-pause"))).click()
                            elif bool(driver.find_elements(By.ID,"player-exit")):
                                driver.find_element(By.ID,"player-exit").click()
                                break
                            else:
                                time.sleep(5)
        else:
            break
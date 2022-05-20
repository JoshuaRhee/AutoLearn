from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
import easygui

# BEFORE RUNNING: Check and change the directory of your chrome web browser in 'run_chrome.bat'.
    
# Set custom time delay options
dt = 1 # 일반 클릭 후 대기 시간
dt_mid = 5 # 학습창 윈도우 대기 시간
dt_long = 20 # 페이지 당 체류 시간 (총 수강 시간 및 진도율에 영향)

# Remote chrome setting
is_chrome_running = easygui.ynbox('이미 본 프로그램을 통해 크롬이 열려 있습니까?','', ('네', '아니오'))
if not is_chrome_running:
    easygui.msgbox('웹사이트에 직접 로그인 한 후 학습 창을 여시면 자동으로 진행됩니다.')
    os.system('run_chrome.bat')
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "drivers\chromedriver.exe" # Your Chrome Driver path
driver = webdriver.Chrome(chrome_driver, options=chrome_options)

# Move to the KIRD website
if not is_chrome_running:
    driver.get('http://kriss.safelearn.co.kr/')

wait_for_lecture = True
while wait_for_lecture:
    # Wait and select the lecture window
    i = 0
    while True:
        driver.switch_to.window(driver.window_handles[i])
        if '학습창' in driver.title:
            print('학습창 윈도우를 발견했습니다.')
            break
        else:
            i += 1        
            if i > len(driver.window_handles)-1:
                i = 0
                time.sleep(dt_mid)
        print('학습창 윈도우를 기다리고 있습니다.')

    #driver.find_element(By.XPATH,'/html/frameset/frame[2]')
    driver.switch_to.frame('frame_body')

    flag_end = False
    while not flag_end:
        try: # Show control box
            box_ctrl = driver.find_element(By.ID,'controlBox')
            driver.execute_script("arguments[0].style.display = 'block';", box_ctrl)
            time.sleep(dt)
            
        except: # No control box = Quiz time
            try:
                driver.switch_to.frame('QuizIframe')
                driver.find_element(By.XPATH,"//ul[@class='Quiz_list']/li/img").click()
                time.sleep(dt)
                driver.find_element(By.XPATH,"//li[@id='btnCheckAnswer']/img").click()
                time.sleep(dt)
                driver.switch_to.parent_frame()
            except: # Last quiz time
                try:
                    driver.find_element(By.XPATH,"//div[@class='start']/img").click()
                    time.sleep(dt)
                    while True:
                        driver.find_element(By.XPATH,"//ul[@class='Quiz_list']/li").click()
                        time.sleep(dt)
                        driver.find_element(By.XPATH,"//li[@id='btnCheckAnswer']/img").click()
                        time.sleep(dt)
                        try:
                            driver.find_element(By.XPATH,"//li[@id='btnNextQuiz']/img").click()
                            time.sleep(dt)
                            continue
                        except:
                            try:
                                driver.find_element(By.XPATH,"//li[@id='btnEndQuiz']/img").click()
                                time.sleep(dt)
                            except:
                                continue
                        driver.switch_to.parent_frame()
                        btn_next = driver.find_element(By.ID,'btn_nextPage')
                        btn_next.click()
                        break
                    driver.switch_to.parent_frame()
                except: # The last page
                    flag_end = True
                

        # Go to the next page
        try:
            btn_next = driver.find_element(By.ID,'btn_nextPage')
            btn_next.click()
            win_alert = driver.switch_to.alert # This line raises an error when there is no alert(=Succeeded to go next.)
            if win_alert.text == '마지막 페이지입니다.':
                win_alert.accept()
                flag_end = True
                break
            else:
                print(win_alert.text)
                win_alert.accept()
            time.sleep(dt_long)
        except:
            pass
            
    print('강의가 종료되었습니다.')
    driver.close()
    wait_for_lecture = easygui.ynbox('다른 강의를 들으시겠습니까?','',('다른 학습창을 위해 대기', '프로그램 종료'))

driver.quit()
import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
import datetime
import math
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from log import set_logger
logger = set_logger(__name__)


LOG_FILE_PATH = "./log/log_{datetime}.log"
EXP_CSV_PATH="./exp_list_{search_keyword}_{datetime}.csv"
log_file_path=LOG_FILE_PATH.format(datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
MYNAVI_SEARCH_URL = "https://tenshoku.mynavi.jp/list/kw{keyword}/pg{page}/?jobsearchType=14&searchType=18"

### Chromeを起動する関数
def set_driver(use_headless: bool=False):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if use_headless:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(ChromeDriverManager().install(), options=options)

### ログファイルおよびコンソール出力
def log(txt):
    now=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    logStr = '[%s: %s] %s' % ('log',now , txt)
    # ログ出力
    with open(log_file_path, 'a', encoding='utf-8_sig') as f:
        f.write(logStr + '\n')
    print(logStr)

def find_table_target_word(th_elms, td_elms, target:str):
    # tableのthからtargetの文字列を探し一致する行のtdを返す
    for th_elm,td_elm in zip(th_elms,td_elms):
        if th_elm.text == target:
            return td_elm.text

def fetch_searched_page_num(keyword: str):
    driver = set_driver(use_headless=True)
    driver.get(MYNAVI_SEARCH_URL.format(keyword=keyword, page=1))
    return math.ceil(int(driver.find_element_by_class_name("result__num em").text) / 50)

def run(keyword,page,thread_num,run_at):
    start = time.time()
    driver = set_driver(use_headless=True)
    try:
        driver.get(MYNAVI_SEARCH_URL.format(keyword=keyword,page=page))
        name_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__name")
        copy_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .cassetteRecruit__copy")
        status_list = driver.find_elements_by_css_selector(".cassetteRecruit__heading .labelEmploymentStatus")
        table_list = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition") # 初年度年収
        df = pd.DataFrame()
        for name,copy,status,table in zip(name_list,copy_list,status_list,table_list):
            try:
                first_fee = find_table_target_word(table.find_elements_by_class_name('tableCondition__head'),table.find_elements_by_class_name('tableCondition__body'),'初年度年収')
                df = df.append({
                        '会社名':name.text,
                        'キャッチコピー':copy.text,
                        '肩書':status.text,
                        '初年度年収':first_fee
                    },ignore_index=True)
                logger.info(f'[thread{thread_num + 1}]:成功しました{name.text}')
            except Exception as e:
                logger.error(f'[thread{thread_num + 1}]:{name.text} / {e}')
        header = False if os.path.exists(EXP_CSV_PATH.format(search_keyword=keyword,datetime=run_at))else True
        df.to_csv(EXP_CSV_PATH.format(search_keyword=keyword,datetime=run_at),mode='a',index=False,header=header,encoding='utf-8')
    except Exception as e:
        logger.error(f'[thread{thread_num + 1}]:失敗しました{e}')
    finally:
        driver.quit()
        logger.info(f'[thread{thread_num + 1}]time(s):{time.time()-start}')
    
        
                


            


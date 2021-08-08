from main2 import fetch_searched_page_num, run
import time
import threading
from datetime import datetime
from log import set_logger
logger = set_logger(__name__)

def main(keyword):
    start = time.time()
    run_at = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    thread_list = []
    page_num = fetch_searched_page_num(keyword)
    page_num_list = list(range(page_num))
    count = 1
    for id in page_num_list:
        t = threading.Thread(target=run,args=[keyword,count,id,run_at])
        t.start()
        thread_list.append(t)
        count += 1
    for thread in thread_list:
        thread.join()
    print('終了しました。')
    logger.info(f"time(s): {time.time() - start} | page:{page_num}")

if __name__ == "__main__":
    main("SE")
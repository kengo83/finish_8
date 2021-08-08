import threading
import time

def for_text():
    for i in range(10):
        print('forループ:'+ str(i) + '回目')
        time.sleep(1)

def another():
    for i in range(10):
        print('forループ頑張って！')
        time.sleep(1)

t1 = threading.Thread(target=for_text)
t2 = threading.Thread(target=another)

t1.start()
t2.start()
t1.join()
t2.join()
print('よく頑張りました')


    




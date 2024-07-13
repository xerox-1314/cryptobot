import schedule
import time
def test(name):
    print(name)
schedule.every().second.do(test, 'hi')
while True:
    schedule.run_pending()
    time.sleep(1)
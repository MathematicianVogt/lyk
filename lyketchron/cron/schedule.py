from plan import Plan
from os import getcwd

WORKING_DIR = getcwd() + '/../'
cron = Plan("lyket_ingestion_cron")

cron.script('LyketJob.py', every='5.minutes', path=WORKING_DIR)

if __name__ == '__main__':
    try:
        cron.run('update')
    except:
        cron.run('write')

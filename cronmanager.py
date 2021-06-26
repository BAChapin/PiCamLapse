#!/usr/bin/python3

from global_variables import GeneralSettings
from solarnoon import get_time
from crontab import CronTab
from datetime import time

if __name__ == "__main__":
    this_path = "{}/PiCamLapse/cronmanager.py".format(GeneralSettings.base_path)
    main_path = "{}/PiCamLapse/main.py".format(GeneralSettings.base_path)
    this_comment = "cronmanager"
    main_comment = "picamlapse"
    this_time = time(0,5)
    main_time = get_time()

    cron = CronTab(user="pi")

    for job in cron:
        if job.comment == this_comment:
            break
    else:
        this_job = cron.new(command=this_path, comment=this_comment)
        this_job.setall(this_time)
        print("Creating 'this_job'...")

    if this_time < main_time:
        for job in cron:
            if job.comment == main_comment:
                cron.remove(job)
        
        main_job = cron.new(command=main_path, comment=main_comment)
        main_job.setall(main_time)
        print("Creating 'main_job'...")

    cron.write()
    print("Adding jobs to crontab...")

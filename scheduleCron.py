from crontab import CronTab

cron = CronTab(user=True)
job = cron.new(command='python3 ~/PycharmProjects/gunicorn_project/pars_each_link.py')  # >> ~/PycharmProjects/gunicorn_project/tmp/api_logs 2>&1
job.hour.every(2)

cron.write()

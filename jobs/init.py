import datetime, pytz
#
from jobs.quote import post

def sched(h, m, s) -> datetime.datetime:
  return datetime.time(
    hour=h, minute=m, second=s,
    tzinfo=pytz.timezone('America/Santiago')
  )

def send_jobs(job_queue) -> None:
  job_queue.run_daily(
    post,
    name='Daily Quote',
    time=sched(7, 45, 0),
    days=(0, 1, 2, 3, 4, 5, 6)
  )

  job_queue.run_daily(
    post,
    name='Daily Quote',
    time=sched(11, 45, 0),
    days=(0, 1, 2, 3, 4, 5, 6)
  )

  job_queue.run_daily(
    post,
    name='Daily Quote',
    time=sched(15, 45, 0),
    days=(0, 1, 2, 3, 4, 5, 6)
  )

  job_queue.run_daily(
    post,
    name='Daily Quote',
    time=sched(19, 45, 0),
    days=(0, 1, 2, 3, 4, 5, 6)
  )

  job_queue.run_daily(
    post,
    name='Daily Quote',
    time=sched(21, 45, 0),
    days=(0, 1, 2, 3, 4, 5, 6)
  )

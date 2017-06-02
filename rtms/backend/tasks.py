from datetime import datetime
import json

from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from celery import shared_task

from backend.models import Plan


@shared_task(ignore_result=True)
def run_task(**kwargs):
    print '1111111'
    return str(kwargs)+'1'


def cook_plan(plan_id):
    plan = Plan.objects.get(pk=plan_id)
    if plan.flag == 'A':
        run_task.delay(**{'plan_id': plan_id})
    else:
        if plan.flag == 'B':
            execute = datetime.strptime(plan.execute_time, '%H:%M')
            kwargs = {'crontab': CrontabSchedule.objects.get_or_create(minute=execute.minute, hour=execute.hour)[0],
                      'enabled': plan.switch,
                      'interval': None,
                      'kwargs': json.dumps({'plan_id': plan_id})
                      }
        elif plan.flag == 'C':
            kwargs = {'interval': IntervalSchedule.objects.get_or_create(every=plan.frikcy, period='minutes')[0],
                      'enabled': plan.switch,
                      'crontab': None,
                      'kwargs': json.dumps({'plan_id': plan_id})
                     }
        if not plan.period:
            # print 'asqwqwq'
            # print run_task.name
            # print type(run_task.name)
            plan.period = PeriodicTask.objects.update_or_create(name=plan.name, task=run_task.name, defaults=kwargs)
        else:
            plan.period.delete()
            plan.period = PeriodicTask.objects.create(name=plan.name, task=run_task.name, **kwargs)
        plan.save()






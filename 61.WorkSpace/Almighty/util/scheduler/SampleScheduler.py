import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


class JobLauncher:

    _sched = None

    def __init__(self):
        JobLauncher._sched = BackgroundScheduler()
        JobLauncher._sched.start()

    def __str__(self):
        return "JobLauncher"

    def run(self, job, request_params):
        job.job_params.update(request_params)
        return self.run_job(job)

    def stop(self, job):
        JobLauncher._sched.remove_job(job.name)

    def shutdown(self):
        if JobLauncher._sched.running():
            logger.debug('Scheduler is shutting down.')
            JobLauncher._sched.shutdown()
        else:
            logger.warn("Cannot shutdown scheduler because scheduler is not running at the moment. please check scheduler status.")

    def run_job(self, job):
        if JobLauncher._sched.get_job(job.name) is None:
            if job.schedule_type == "cron":
                logger.debug(job)
                _job_trigger_params = JobTriggerParameterBuilder.build_cron_type_params(job.job_trigger_params)
                _job = JobLauncher._sched.add_job(job.execute, job.schedule_type, id=job.name, args=job.job_params.items(),
                                                  year=_job_trigger_params['year'], month=_job_trigger_params['month'], day=_job_trigger_params['day'],
                                                  hour=_job_trigger_params['hour'], minute=_job_trigger_params['minute'], second=_job_trigger_params['second'])
                return True

        return False


class JobTriggerParameterBuilder:

    @staticmethod
    def build_cron_type_params(params):
        params.setdefault("year", "*")
        params.setdefault("month", "*")
        params.setdefault("day", "*")
        params.setdefault("hour", "*")
        params.setdefault("minute", "*")
        params.setdefault("second", "*")
        return params



class CommonJob:

    def __str__(self):
        return "Job Infos : {name : %s, schedule_type : %s, job_trigger_params : %s, job_params : %s}" % (self.name, self.schedule_type, self.job_trigger_params, self.job_params)

    @property
    def name(self):
        return self._name

    @property
    def schedule_type(self):
        return self._schedule_type

    @property
    def job_trigger_params(self):
        return self._job_trigger_params

    @property
    def job_params(self):
        return self._job_params

    def execute(self, *args, **kwargs):
        pass


class JobLauncherHolder:

    _launcher = None

    @staticmethod
    def getInstance():
        if not JobLauncherHolder._launcher:
            JobLauncherHolder._launcher = JobLauncher()

        return JobLauncherHolder._launcher
import logging

from django.http import JsonResponse
from schedule.CommonScheduler import *

logger = logging.getLogger(__name__)


def start_job(request, job_name, mode):
    if request.method == "GET":
        if mode == "start":
            logger.debug(request.GET)
            launcher = JobLauncherHolder.getInstance()
            if launcher.run(job_dict[job_name], request.GET):
                result = get_result("success", "mode is %s" % mode)
            else:
                result = get_result("success", "fail to run job because of job's already started")
        elif mode == "stop":
            launcher = JobLauncherHolder.getInstance()
            launcher.stop(job_dict[job_name])
            result = get_result("success", "mode is %s" % mode)
        else:
            logger.warn(“¹미정의 mode(%s) 입니다." % mode)
            result = get_result("fail", “정의되지 않은 Job Mode(%s) 입니다." % mode)
    else:
        result = get_result("fail", “지원하지 않는 방식입니다. GET 방식을 이용하세요.")

    return JsonResponse(result, safe=False)


def shutdown_job_launcher(request):
    launcher = JobLauncherHolder.getInstance()
    launcher.shutdown()
    result = {"flag":"success", "msg":"job_launcher stoped"}

    return JsonResponse(result, safe=False)


def get_result(flag, message):
    return {
        "flag" : flag,
        "message" : message
    }


출처: https://tomining.tistory.com/138 [마이너의 일상]

출처: https://tomining.tistory.com/138 [마이너의 일상]
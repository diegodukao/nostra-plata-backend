# coding: utf-8
from unipath import Path

from fabric.api import env, task

import app
import server


@task
def go():
    env.site = 'nostraplata.mobilidade.fm'
    env.hosts = [env.site]
    env.environment = 'staging'
    env.app_name = 'nostra-plata'
    env.RELEASES = Path('/opt').child(env.app_name, 'releases')
    env.GIT_URI = 'git@github.com:diegodukao/nostra-plata-backend.git'

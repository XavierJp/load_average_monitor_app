from django.core.management.base import BaseCommand
import subprocess
import os.path

SITE_ROOT = os.path.abspath(os.path.dirname(__name__))

class Command(BaseCommand):

    help = 'set cron for update_uptime'

    def escape_path(self, s):
        return s.replace("(","\(").replace(")","\)").replace(" ","\ ")

    def handle(self, *args, **options):
        command = "crontab -l | { cat; echo '* * * * * python "+self.escape_path(SITE_ROOT)+"/manage.py update_data';} | crontab"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        process.wait()
        print "crontab correctly updated"
        print process.returncode



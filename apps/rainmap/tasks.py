import datetime
import glob
import shutil
import subprocess
from os import chdir, devnull, unlink
from os.path import isdir, isfile

import celery.log
import celery.utils
from celery.task import task


@task(ignore_result=True)
def purge_data(asset_path, owner_id):
    logger = celery.utils.log.LoggingProxy(celery.log.get_default_logger())
    logger.write("PURGE For User %s | Path: %s" % (owner_id, asset_path))
    if isdir(asset_path):
        shutil.rmtree(asset_path, False, None)
    else:
        for f in glob.glob(asset_path + "*"):
            try:
                unlink(f)
            except:
                pass


@task(ignore_result=True)
def run_scan(name_base, workdir, scan_id, owner_id, result_id, cmd):
    logger = celery.utils.log.LoggingProxy(celery.log.get_default_logger())
    chdir(workdir)
    logger.write("BEGIN Scan %s | User %s\ncmd: %s" % (scan_id, owner_id, cmd))
    status_nmap = subprocess.call(["nmap"] + cmd.split(), stdout=open(devnull))
    logger.write("END Scan %s | User %s\nstatus: %d" % (scan_id, owner_id, status_nmap))

    finished_ok = (status_nmap == 0)
    # try to save output. even for errors, we might see what happened
    if isfile(name_base + ".xml"):
        logger.write("XSLT Scan %s | User %s" % (scan_id, owner_id))
        status_xslt = subprocess.call(["xsltproc", name_base + ".xml", "-o",
            name_base + ".html"])
        # html and xml are the most important outputs, so we only track those
        if status_xslt == 0:
            output = name_base + ".html"
        else:
            output = name_base + ".xml"
    else:
        output = None
        finished_ok = False # well, no output *is* an error

    process_result.delay(result_id, finished_ok, output)


@task(ignore_result=True)
def process_result(result_id, finished_ok, output):
    from django.contrib.sites.models import Site
    from django.core.urlresolvers import reverse
    from django.template.loader import render_to_string

    from apps.rainmap.models import ScanResult

    result = ScanResult.objects.get(id=result_id)
    scan = result.for_scan

    result.finished_ok = finished_ok
    if output:
        result.output = output

    result.finished_on = datetime.datetime.now()
    result.save()

    if scan.owner.userprofile.mail_results_all or (
        scan.owner.userprofile.mail_results_err and not result.finished_ok):

        if result.output:
            link = 'http://%s%s' % (Site.objects.get_current().domain,
                reverse('core_result_view', args=[result_id]))
        else:
            link = None

        profile_link = 'http://%s%s' % (Site.objects.get_current().domain,
            reverse('user_profile'))

        ctx_dict = {
            'link': link,
            'scan_name': scan.name,
            'profile_link': profile_link,
        }

        if result.finished_ok and scan.owner.userprofile.mail_results_all:
            subj = render_to_string('rainmap/email_results_subject_success.txt',
                ctx_dict)
            body = render_to_string('rainmap/email_results_success.txt', ctx_dict)
        else:
            subj = render_to_string('rainmap/email_results_subject_error.txt',
                ctx_dict)
            body = render_to_string('rainmap/email_results_error.txt', ctx_dict)

        subj = ''.join(subj.splitlines())

        result.for_scan.owner.email_user(subj, body, 'scanbot@rainmap.org')

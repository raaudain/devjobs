import random
import logging
import sys
from datetime import datetime
sys.path.insert(0, ".")
from server.job_boards.helpers import CreateJson
from server.job_boards import *


logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} {levelname:<8} {message}",
    style="{",
    filename="../../../devjobs.log",
    filemode="a"
)

create_json = CreateJson()

def main():
    f = open("server/data/params/craigslist.txt", "r")
    locations = [location.strip() for location in f]
    f.close()

    w = open("server/data/params/workable.txt", "r")
    work = [l.strip() for l in w]
    random.shuffle(work)
    w.close()

    g = open("server/data/params/greenhouse_io.txt", "r")
    green = [l.strip() for l in g]
    g.close()

    # w_half = len(work)//2
    # workable1 = work[:w_half]
    # workable2 = work[w_half:]

    # m = open(f"server/data/params/miami.txt", "r")
    # miamis = [miami.strip() for miami in m]
    # m.close()
    print("=> Scanning job boards")
    start = datetime.now()
    # bloomberg.main()
    crew.main()
    usajobs.main()
    workable.get_url(work[::5])
    diversifytech.main()
    polymer.main()
    # indeed.main()
    # tiktok.main()
    recruitee.main()
    # target.main()
    nbc.main()
    # nocsok.main()
    workable.get_url(work[1::5])
    smartrecruiters.main()
    breezyhr.main()
    greenhouse_io.get_url(green[::2])
    craigslist.get_url(locations)
    jobvite.main()
    bamboohr.main()
    eightfold.main()
    jazzhr.main()
    clearcompany.main()
    workable.get_url(work[2::5])
    comeet.main()
    craigslist.get_url_it(locations)
    greenhouse_io.get_url(green[1::2])
    lever_co.main()
    ashbyhq.main()
    recruiterbox.main()
    nintendo.main()
    vuejobs.main()
    hireart.main()
    amazon.main()
    craigslist.get_url_web(locations)
    workable.get_url(work[3::5])
    twitter.main()
    key_values.main()
    workwithindies.main()
    weworkremotely.main()
    fullstackjob.main()
    remote_co.main()
    remoteok.main()
    craigslist.get_url_network(locations)
    # workaline.main()
    workable.get_url(work[4::5])
    dailyremote.main()
    bootup.main()
    builtin.main()
    create_json.create_temp_file()
    create_json.create_file()
    # try:
    #     CreateJson.create_file()
    # except Exception as e:
    #     logging.debug("Exception occured: ", e, exc_info=True)
    print("=> Done")
    print("=> Total time: " + str(datetime.now() - start))

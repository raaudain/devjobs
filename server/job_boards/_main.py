import random
from .modules.classes import Create_JSON
from . import comeet
from . import clearcompany
from . import eightfold
from . import craigslist
from . import greenhouse_io
# from . import bloomberg
from . import bamboohr
from . import lever_co
from . import workaline
from . import workable
from . import key_values
from . import remote_co
from . import remoteok
from . import weworkremotely
from . import builtin
from . import dailyremote
from . import hireart
# from . import stackoverflow
# from . import dice
# from . import zillow
from . import usajobs
from . import amazon
from . import smartrecruiters
from . import nocsok
from . import workwithindies
from . import ashbyhq
from . import nintendo
from . import jazzhr
from . import breezyhr
from . import target
from . import twitter
from . import tiktok
from . import vuejobs
from . import jobvite
from . import recruiterbox
from . import nbc
from . import fullstackjob
from . import wrk
from . import indeed
from . import diversifytech
# from . import craigslist_gigs
from .modules import create_temp_json
# from .modules import create_main_json
from datetime import datetime, timedelta
import sys, os


def main():
    f = open(f"./data/params/craigslist.txt", "r")
    locations = [location.strip() for location in f]
    f.close()

    w = open(f"./data/params/workable.txt", "r")
    work = [l.strip() for l in w]
    random.shuffle(work)
    w.close()

    g = open(f"./data/params/greenhouse_io.txt", "r")
    green = [l.strip() for l in g]
    g.close()

    # w_half = len(work)//2
    # workable1 = work[:w_half] 
    # workable2 = work[w_half:]

    # m = open(f"./data/params/miami.txt", "r")
    # miamis = [miami.strip() for miami in m]
    # m.close()

    print("=> Scanning job boards")
    start = datetime.now()
    # bloomberg.main()
    diversifytech.main()
    wrk.main()
    indeed.main()
    tiktok.main()
    target.main()
    workable.get_url(work[::3])
    # craigslist_gigs.main()
    nbc.main()
    nocsok.main()
    smartrecruiters.main()
    greenhouse_io.get_url(green[::2])
    craigslist.get_url(locations)
    jobvite.main()
    breezyhr.main()
    bamboohr.main()
    eightfold.main()
    jazzhr.main()
    ashbyhq.main()
    clearcompany.main()
    # craigslist.get_url_miami(miamis)
    comeet.main()
    craigslist.get_url_it(locations)
    workable.get_url(work[1::3])
    greenhouse_io.get_url(green[1::2])
    lever_co.main()
    # craigslist.get_url_miami_it(miamis)
    recruiterbox.main()
    nintendo.main()
    vuejobs.main()
    hireart.main()
    # craigslist.get_url_miami_network(miamis)
    amazon.main()
    craigslist.get_url_web(locations)
    twitter.main()
    usajobs.main()
    key_values.main()
    # zillow.main()
    workwithindies.main()
    weworkremotely.main()
    fullstackjob.main()
    workaline.main()
    remote_co.main()
    remoteok.main()
    craigslist.get_url_network(locations)
    workable.get_url(work[2::3])
    dailyremote.main()
    # stackoverflow.main()
    # dice.main()
    builtin.main()
    create_temp_json.createJSON(create_temp_json.data)
    # create_main_json.createJSON()
    # Create_JSON.create_temp_file(Create_JSON.data)
    Create_JSON.create_file()
    print("=> Done")
    print("=> Total time: " + str(datetime.now() - start))


# main()
# sys.exit(0)

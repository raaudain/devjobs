import random
import logging
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
from . import usajobs
from . import amazon
from . import smartrecruiters
# from . import nocsok
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
from datetime import datetime
from .modules.classes import Create_JSON


logging.basicConfig(
    level=logging.DEBUG,
    format="{asctime} {levelname:<8} {message}",
    style="{",
    filename="error.log",
    filemode="w"
)


def main():
    f = open("./data/params/craigslist.txt", "r")
    locations = [location.strip() for location in f]
    f.close()

    w = open("./data/params/workable.txt", "r")
    work = [l.strip() for l in w]
    random.shuffle(work)
    w.close()

    g = open("./data/params/greenhouse_io.txt", "r")
    green = [l.strip() for l in g]
    g.close()

    # w_half = len(work)//2
    # workable1 = work[:w_half]
    # workable2 = work[w_half:]

    # m = open(f"./data/params/miami.txt", "r")
    # miamis = [miami.strip() for miami in m]
    # m.close()
    try:
        print("=> Scanning job boards")
        start = datetime.now()
        # bloomberg.main()
        workable.get_url(work[::5])
        diversifytech.main()
        wrk.main()
        indeed.main()
        tiktok.main()
        target.main()
        nbc.main()
        # nocsok.main()
        workable.get_url(work[1::5])
        smartrecruiters.main()
        greenhouse_io.get_url(green[::2])
        craigslist.get_url(locations)
        jobvite.main()
        breezyhr.main()
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
        usajobs.main()
        key_values.main()
        workwithindies.main()
        weworkremotely.main()
        fullstackjob.main()
        workaline.main()
        remote_co.main()
        remoteok.main()
        craigslist.get_url_network(locations)
        workable.get_url(work[4::5])
        dailyremote.main()
        builtin.main()
        Create_JSON.create_temp_file(Create_JSON.data)
        # Create_JSON.create_file()
    except Exception as e:
        logging.debug("Exception occured: ", exc_info=True)
    print("=> Done")
    print("=> Total time: " + str(datetime.now() - start))

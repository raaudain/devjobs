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
# from . import clickup
from . import workable
# from . import instacart
from . import key_values
from . import remote_co
from . import remoteok
from . import weworkremotely
from . import builtin
# from . import dailyremote
from . import hireart
# from . import stackoverflow
# from . import dice
from . import zillow
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
from .modules import create_temp_json
from .modules import create_main_json
from datetime import datetime, timedelta
import sys, os


def main():
    f = open(f"./data/params/craigslist.txt", "r")
    locations = [location.strip() for location in f]
    f.close()

    # m = open(f"./data/params/miami.txt", "r")
    # miamis = [miami.strip() for miami in m]
    # m.close()

    print("=> Scanning job boards")
    start = datetime.now()
    # bloomberg.main()
    comeet.main()
    jobvite.main()
    workable.main()
    target.main()
    eightfold.main()
    clearcompany.main()
    smartrecruiters.main()
    bamboohr.main()
    craigslist.get_url(locations)
    nintendo.main()
    greenhouse_io.main()
    # craigslist.get_url_miami(miamis)
    lever_co.main()
    nbc.main()
    craigslist.get_url_it(locations)
    ashbyhq.main()
    breezyhr.main()
    # craigslist.get_url_miami_it(miamis)
    recruiterbox.main()
    vuejobs.main()
    craigslist.get_url_network(locations)
    hireart.main()
    tiktok.main()
    # craigslist.get_url_miami_network(miamis)
    amazon.main()
    twitter.main()
    jazzhr.main()
    usajobs.main()
    key_values.main()
    zillow.main()
    remoteok.main()
    remote_co.main()
    # clickup.main()
    # instacart.main()
    nocsok.main()
    workwithindies.main()
    weworkremotely.main()
    workaline.main()
    # dailyremote.main()
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
# import craigslist_gigs
from . import craigslist
from . import greenhouse_io
from . import bloomberg
from . import lever_co
from . import workaline
from . import clickup
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
    print("=> Scanning job boards")
    start = datetime.now()
    # bloomberg.main()
    ashbyhq.main()
    breezyhr.main()
    craigslist.main()
    lever_co.main()
    nbc.main()
    recruiterbox.main()
    jobvite.main()
    vuejobs.main()
    hireart.main()
    target.main()
    tiktok.main()
    greenhouse_io.main()
    workable.main()
    amazon.main()
    twitter.main()
    smartrecruiters.main()
    jazzhr.main()
    nintendo.main()
    usajobs.main()
    key_values.main()
    zillow.main()
    clickup.main()
    # instacart.main()
    nocsok.main()
    remote_co.main()
    remoteok.main()
    workwithindies.main()
    weworkremotely.main()
    workaline.main()
    # dailyremote.main()
    # stackoverflow.main()
    # dice.main()
    builtin.main()
    create_temp_json.createJSON(create_temp_json.data)
    create_main_json.createJSON()
    print("=> Done")
    print("=> Total time: " + str(datetime.now() - start))

# main()
# gitPush()


# sys.exit(0)
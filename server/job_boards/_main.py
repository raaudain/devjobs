# import craigslist_gigs
from . import craigslist_jobs
from . import crunchyroll
from . import blend 
from . import key_values
from . import protege
from . import nocsok
from . import remote_co
from . import remoteok
from . import weworkremotely
from .modules import create_temp_json
from .modules import create_main_json
# from server.job_boards import modules
# from . import *
import sys


def main():
    print("=> Scanning job boards")
    # craigslist_gigs.main()
    blend.main()
    # craigslist_jobs.main()
    crunchyroll.main()
    key_values.main()
    nocsok.main()
    protege.main()
    remote_co.main()
    remoteok.main()
    weworkremotely.main()
    create_temp_json.createJSON(create_temp_json.data)
    create_main_json.createJSON()
    print("=> Done")

# main()

# sys.exit(0)
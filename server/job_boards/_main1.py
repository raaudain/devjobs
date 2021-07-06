# import craigslist_gigs
from multiprocessing import Pool
from git import Repo
# from . import craigslist_jobs
# from . import greenhouse_io
# from . import bloomberg
# from . import lever_co
# from . import clickup
# from . import workable
# from . import instacart
# from . import key_values
# from . import nocsok
# from . import remote_co
# from . import remoteok
# from . import weworkremotely
# from . import builtin
# from . import dailyremote
# from . import hireart
# from . import stackoverflow
# from . import dice
from . import workwithindies
from . import workline
from . import zillow
from . import usajobs
from .modules import create_temp_json
from .modules import create_main_json
from datetime import datetime, timedelta
import sys, os


def gitPush():
    pathToRepo = f"{os.getcwd()}/.git"
    commitMessage = "Update json"

    try:
        repo = Repo(pathToRepo)
        repo.git.add(update=True)
        repo.index.commit(commitMessage)
        origin = repo.remote(name="origin")
        origin.push()
        print("=> Pushed to GitHub")
    except:
        print("=> Failed to push to GitHub") 

sites = (
    # hireart.main(),
    # workable.main(),
    # lever_co.main(),
    # bloomberg.main(),
    # dailyremote.main(),
    # dice.main(),
    # # craigslist_jobs.main(),
    # builtin.main(),
    # greenhouse_io.main(),
    # stackoverflow.main(),
    # key_values.main(),
    # clickup.main(),
    # instacart.main(),
    # nocsok.main(),
    # remote_co.main(),
    # remoteok.main(),
    # weworkremotely.main(),
    # "workline.py",
    "zillow.py",
    # "usajobs.py",
    "workwithindies.py",
)

create = ("create_temp_json.createJSON(create_temp_json.data)",
    "create_main_json.createJSON()")

def main1(process):
    os.system(f"python3 {process}")
    # print("=> Scanning job boards")
    # # start = None
    
    # for site in sites:
    #     # time = datetime.now()
    #     site
    #     # start += datetime.now(timedelta(minutes=time))


    # create_temp_json.createJSON(create_temp_json.data)
    # create_main_json.createJSON()
    # # gitPush()
    # print("=> Done")
    # print("=> Total time: " + str(datetime.now() - start))

pool = Pool(processes=4)                                                        
pool.map(main1, sites)  

# main()
# gitPush()


# sys.exit(0)
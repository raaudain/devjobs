# import craigslist_gigs
from git import Repo
from . import craigslist_jobs
from . import greenhouse_io
from . import lever_co
from . import workline
from . import clickup
from . import workable
from . import instacart
from . import key_values
from . import nocsok
from . import remote_co
from . import remoteok
from . import weworkremotely
from . import builtin
from . import workwithindies
from . import dailyremote
from . import hireart
from . import stackoverflow
from . import dice
from . import zillow
from . import usajobs
from .modules import create_temp_json
from .modules import create_main_json
from datetime import datetime
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

sites = [
    workline.main(),
    lever_co.main(),
    dailyremote.main(),
    workable.main(),
    dice.main(),
    craigslist_jobs.main(),
    builtin.main(),
    usajobs.main(),
    greenhouse_io.main(),
    stackoverflow.main(),
    key_values.main(),
    zillow.main(),
    hireart.main(),
    clickup.main(),
    instacart.main(),
    nocsok.main(),
    remote_co.main(),
    remoteok.main(),
    weworkremotely.main(),
    workwithindies.main(),
]

def main():
    print("=> Scanning job boards")
    start = datetime.now()
    
    for site in sites: site
        


    # dice.main()
    # craigslist_jobs.main()
    # builtin.main()
    # usajobs.main()
    # lever_co.main()
    # workable.main()
    # greenhouse_io.main()
    # stackoverflow.main()
    # key_values.main()
    # zillow.main()
    # hireart.main()
    # clickup.main()
    # instacart.main()
    # nocsok.main()
    # remote_co.main()
    # remoteok.main()
    # weworkremotely.main()
    # workwithindies.main()



    create_temp_json.createJSON(create_temp_json.data)
    create_main_json.createJSON()
    # gitPush()
    print("=> Done")
    print("=> Total time: " + str(datetime.now() - start))

# main()
# gitPush()


# sys.exit(0)
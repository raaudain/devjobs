# import craigslist_gigs
from git import Repo
from . import craigslist_jobs
# from . import crunchyroll
from . import blend 
from . import gitlab
from . import github
from . import key_values
from . import protege
from . import nocsok
from . import remote_co
from . import remoteok
from . import weworkremotely
from . import builtin
from . import workwithindies
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

def main():
    print("=> Scanning job boards")
    start = datetime.now()
    # craigslist_gigs.main()
    blend.main()
    builtin.main()
    craigslist_jobs.main()
    github.main()
    gitlab.main()
    key_values.main()
    nocsok.main()
    protege.main()
    # crunchyroll.main()
    remote_co.main()
    remoteok.main()
    weworkremotely.main()
    workwithindies.main()
    create_temp_json.createJSON(create_temp_json.data)
    create_main_json.createJSON()
    gitPush()
    print("=> Done")
    print("=> Total time: " + str(datetime.now()-start))

# main()
# gitPush()


# sys.exit(0)
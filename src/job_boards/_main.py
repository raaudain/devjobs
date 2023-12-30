import random
import sys
from datetime import datetime
sys.path.insert(0, ".")
from src.job_boards.helpers import CreateJson
from src.job_boards import amazon, ashbyhq, bamboohr, breezyhr, builtin, clearcompany, comeet, crew, dailyremote, diversifytech, eightfold, fullstackjob, greenhouse_io, hireart, jazzhr, jobvite, key_values, lever_co, nbc,nintendo, nocsok, polymer, recruitee, recruiterbox, remote_co, remoteok, smartrecruiters, twitter, upstack, usajobs, weworkremotely, workable, workwithindies, craigslist, target


def main():
    create_json = CreateJson()

    f = open("src/data/params/craigslist.txt", "r")
    locations = [location.strip() for location in f]
    f.close()

    w = open("src/data/params/workable.txt", "r")
    work = [l.strip() for l in w]
    random.shuffle(work)
    w.close()

    g = open("src/data/params/greenhouse_io.txt", "r")
    green = [l.strip() for l in g]
    g.close()

    # w_half = len(work)//2
    # workable1 = work[:w_half]
    # workable2 = work[w_half:]

    # m = open(f"src/data/params/miami.txt", "r")
    # miamis = [miami.strip() for miami in m]
    # m.close()
    print("=> Scanning job boards")
    start = datetime.now()
    lever_co.main()
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
    # bamboohr.main()
    eightfold.main()
    # jazzhr.main()
    # clearcompany.main()
    workable.get_url(work[2::5])
    # comeet.main()
    craigslist.get_url_it(locations)
    greenhouse_io.get_url(green[1::2])
    ashbyhq.main()
    recruiterbox.main()
    nintendo.main()
    # vuejobs.main()
    hireart.main()
    amazon.main()
    craigslist.get_url_web(locations)
    workable.get_url(work[3::5])
    # twitter.main()
    key_values.main()
    workwithindies.main()
    weworkremotely.main()
    fullstackjob.main()
    remote_co.main()
    remoteok.main()
    craigslist.get_url_network(locations)
    workable.get_url(work[4::5])
    dailyremote.main()
    builtin.main()
    create_json.create_temp_file()
    create_json.create_file()

    print("=> Done")
    print("=> Total time: " + str(datetime.now() - start))


if __name__ == "__main__":
    main()
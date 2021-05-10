import craigslist_gigs
import craigslist_jobs
import key_values
import nocsok
import remote_co
import remoteok
import weworkremotely
import modules.create_temp_json as create_temp_json
import modules.create_main_json as create_main_json
import sys


def main():
    craigslist_gigs.main()
    craigslist_jobs.main()
    key_values.main()
    nocsok.main()
    remote_co.main()
    remoteok.main()
    weworkremotely.main()
    create_temp_json.createJSON(create_temp_json.data)
    create_main_json.createJSON()

main()

sys.exit(0)
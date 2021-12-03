#! /usr/local/anaconda3/envs/devjobs/bin/python

from job_boards import _main
import sys, asyncio

asyncio.run(_main.main())

sys.exit(0)
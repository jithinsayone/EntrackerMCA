#!/bin/bash
echo "Starting the Crawler ..."

#script to activate the virtualenv python
source ENV/crawler/bin/activate

#update the script to only take option 1
python3 -m crawler.run_task

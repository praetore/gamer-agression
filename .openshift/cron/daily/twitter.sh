#!/bin/sh
cd $OPENSHIFT_REPO_DIR/cron

if [ ! -x ./daily.py ];
then
    chmod +x daily.py;
fi

./daily.py
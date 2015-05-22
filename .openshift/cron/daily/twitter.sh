#!/bin/sh
cd $OPENSHIFT_HOMEDIR/cron

if [ ! -x ./daily.py ];
then
    chmod +x daily.py;
fi

./daily.py
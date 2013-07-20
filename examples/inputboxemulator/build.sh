#!/bin/sh
# you will need to read the top level README, and run boostrap.py
# in order to make pyjsbuild

options="$*"
#if [ -z $options ] ; then options="-O";fi
../../bin/pyjsbuild --print-statements $options inputbox

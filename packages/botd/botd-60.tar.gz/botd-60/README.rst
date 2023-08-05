NAME
====

**BOTD** - 24/7 channel daemon

SYNOPSIS
========

botctl \<cmd\> \[options\] \[key=value\] \[key==value\] 

DESCRIPTION
===========

**BOTD** is a IRC bot that can run as a  background
daemon for 24/7 a day presence in a IRC channel. You can use it to
display RSS feeds, act as a UDP to IRC gateway, program your own
commands for it and have it log objects on disk to search them. 

**BOTD** an attempt to achieve OS level integration of bot technology directly
into the operating system. A solid, non hackable bot version, that can offer
"display in your irc channel" functionality to the unix programmer. BOTD
runs on both BSD and Linux, is placed in the Public Domain, and, one day,
will be the thing you cannot do without ;]

INSTALL
=======

| sudo pip3 install botd && sudo systemctl enable botd -\\-now

| * default channel/server is #botd on localhost

CONFIGURATION
==============

| botctl cfg server=\<server\> channel=\<channel\> nick=\<nick\> 

| botctl cfg users=True
| botctl met \<userhost\>

| botctl pwd \<nickservnick\> \<nickservpass\>
| botctl cfg password=\<outputfrompwd\>

| botctl rss \<url\>

FILES
=====

| bin/botctl
| bin/botd
| man/man8/botd.8.gz
| man/man8/botctl.8.gz
| lib/systemd/system/botd.service
| etc/rc.d/botd

COPYRIGHT
=========

**BOTD** is placed in the Public Domain, no Copyright, no LICENSE.

AUTHOR
======

Bart Thate 

SEE ALSO
========

https://pypi.org/project/botd

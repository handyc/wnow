#!/usr/local/bin/python3
import curses
import datetime
import traceback
from curses import wrapper
import time

import sys
import os

from zoneinfo import ZoneInfo
from pytz import reference

# zonelist is a user editable list of time zones to display
# comment / uncomment

zonelist = [ 
             ["Pacific/Honolulu", "Honolulu"],
             ["America/Anchorage", "Anchorage"],
             ["US/Pacific", "Seattle"],
             ["US/Mountain", "Denver"],
             ["US/Central", "Springfield"],
             ["US/Eastern", "Buffalo"],
             ["America/Toronto", "Ottawa"],
             ["Canada/Atlantic", "Antigonish"],
             #["America/Sao_Paulo", "Sao Paulo"],
             ["UTC", "UTC"],
             ["Europe/London", "London"],
             ["Europe/Amsterdam", "Leiden"],
             ["Europe/Berlin", "Ochtrup"],
             ["Asia/Jerusalem", "Jerusalem"],
             ["Europe/Moscow", "Moscow"],
             ["Asia/Tehran", "Tehran"],
             ["Asia/Kolkata", "Delhi"],
             ["Asia/Kathmandu", "Kathmandu"],
             ["Asia/Bangkok", "Bangkok"],
             ["Asia/Shanghai", "Guangzhou"],
             ["Australia/Perth", "Perth"],
             ["Asia/Tokyo", "Tokyo"],
             ["Australia/Sydney", "Sydney"],
             #["Australia/Sydney", "Sydney"],
             ["Pacific/Auckland", "Auckland"], 
             ]

zoneorigin = 10 % len(zonelist)
zonedestination = 18 % len(zonelist)

arglen = len(sys.argv)

zonelight = {}
zonelight[0] = int(zoneorigin)
zonelight[1] = int(zonedestination)

## get lights

for element in range(1, arglen):
    zonelight[element-1] = int(sys.argv[element]) % len(zonelist)

## compute dislay offset

offdist = len(zonelist)/2
offset = int(offdist - zonelight[0])

## compute new light positions

clocklight = {}
for light in range(0, len(zonelight)):
   clocklight[light]=(zonelight[light] + offset) % len(zonelist)

# calculate zone display

zone = {}
for z in range(0, len(zonelist)):
   zone[z] = zonelist[(z - offset) % (len(zonelist))]

def schermo(scr, *args):
 try:
  ch = ''
  stdscr = curses.initscr()
  curses.cbreak()
  curses.start_color()
  #curses.use_default_colors()

  curses.use_default_colors()
  for i in range(1, curses.COLORS):
      curses.init_pair(i, i, -1);

  curses.init_pair(1, curses.COLOR_YELLOW, -1)
  curses.init_pair(2, curses.COLOR_CYAN, -1)
  curses.init_pair(3, curses.COLOR_GREEN, -1)

  curses.init_pair(4, curses.COLOR_BLUE, -1)
  curses.init_pair(5, curses.COLOR_YELLOW, -1)
  #curses.init_pair(6, curses.COLOR_RED, -1)
  #curses.init_pair(7, curses.COLOR_RED, -1)

  curses.curs_set(0)

  stdscr.timeout(100)
  while ch != ord('q'):
   for x in range(0,(len(zone))):
      os.environ["TZ"] = zone[x][0]
      localtime = reference.LocalTimezone()
 
      if x in clocklight.values():
         #vx = clocklight.values().index(x)
         vx = [ k for k, v in clocklight.items() if v == x ][0] + 5
         stdscr.addstr(x, 0, f'{str(zone[x][1]): <15} {datetime.datetime.now(tz=ZoneInfo(zone[x][0])).strftime("%a %d %b %Y %H:%M:%S %Z"): <30} {datetime.datetime.now(tz=ZoneInfo(zone[x][0])).strftime(" (UTC%z)"): >0}',  curses.color_pair(vx))
         #stdscr.addstr(x, 60, f'{"<----abcdefgh---"}', curses.color_pair(5))
      else:
         stdscr.addstr(x, 0, f'{str(zone[x][1]): <15} {datetime.datetime.now(tz=ZoneInfo(zone[x][0])).strftime("%a %d %b %Y %H:%M:%S %Z"): <30} {datetime.datetime.now(tz=ZoneInfo(zone[x][0])).strftime(" (UTC%z)"): >0}',  curses.color_pair(3))
         #stdscr.addstr(x, 60, f'{"_._#_#_|_o_&_|_#"}', curses.color_pair(4))

   #stdscr.addstr(x, 60, f'{"_._#_#_|_o_&_|_#"}', curses.color_pair(4))
   #stdscr.addstr(x, 50, f'{"a"}', curses.A_NORMAL)

   stdscr.clrtobot()
   ch = stdscr.getch()

 except:
  traceback.print_exc()
 finally:
  curses.endwin()

curses.wrapper(schermo)

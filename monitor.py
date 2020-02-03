#TP note Python Burkard Yannick
import curses
import time
import os
from math import *


def nblignes():
    fic = open('/proc/stat', 'r')
    stat = fic.read()
    nbligne=stat.count("cpu")
    return nbligne


def infoproc():
    fic = os.popen("cat /proc/cpuinfo | grep -i \"^model name\" | awk -F\": \" '{print $2}' | head -1 | sed 's/ \+/ /g'")
    proc = fic.read()
    return proc

def listvalcpu(ligne):
    with open('/proc/stat', 'r') as fichier:
        cpu = fichier.readlines()
        val = []
        # places toutes les valeurs dans un tableau
        for i in cpu[ligne].split(' '):
            if i != '':
                val.append(i)
        return (val)


stdscr = curses.initscr()
stdscr.nodelay(True)
curses.noecho()
sort = "c"
nbligne=nblignes()
tval = []

#recuperation des valeurs une premiere fois
for nb in range(0, nbligne):
    tval.append(listvalcpu(nb))

try:
  while True:

    for nb in range(0,nbligne):
        #recuperation des valeurs precedente
        val2 = tval[nb]
        tval[nb] = listvalcpu(nb)
        val=tval[nb]
        try:
            stdscr.addstr(0, 0, infoproc(), curses.A_BOLD)
            # Calcul avec user, nice, system, idle pour avoir l'utilisation du cpu
            utilisation = (int(val2[1]) - int(val[1])) + (int(val2[2]) - int(val[2])) + (int(val2[3]) - int(val[3]))
            total = utilisation + (int(val2[4]) - int(val[4]))
            percent = (100 * utilisation) / total
            stdscr.addstr(nb+1, 0, 'Usage '+val2[0]+':')
            stdscr.addstr(nb+1, 43, '%s   ' % abs(round(percent)))
            stdscr.addstr(nb+1, 46, '%')
            #grap de barre
            barre = int(abs(floor(percent/5)))
            stdscr.addstr(nb+1, 19, '[')
            for i in range(0,barre):
                stdscr.addstr(nb+1, 20+i, '#')
            for j in range(barre,20):
                stdscr.addstr(nb+1, 20+j, '-')
            stdscr.addstr(nb+1, 40, ']')
        except ZeroDivisionError: #pour la premiere divison
            pass

    #recup des commandes utilisateur
    ch = stdscr.getch()

    if ch != -1:
      if chr(ch) == 'q':
        break
      if chr(ch) == "c":
        sort = "c"
      if chr(ch) == "m":
        sort = "m"
      if chr(ch) == "t":
        sort = "t"

    stdscr.addstr(nbligne + 1, 0, '-----------------------------------------------', curses.A_BOLD)
    stdscr.addstr(nbligne + 2, 0, 'Process Monitor :', curses.A_BOLD)
    stdscr.addstr(nbligne + 3, 0, 'Sort by : cpu (c), mem (m), time (t)', curses.A_BOLD)
    stdscr.addstr(nbligne + 4, 0, 'Current : ' + sort, curses.A_BOLD)

    #info processus
    if sort == "m":
        cmd = os.popen("ps -eo user,pid,cmd,%cpu,%mem,time --sort=-%mem | head")
    elif sort == "t":
        cmd = os.popen("ps -eo user,pid,cmd,%cpu,%mem,time --sort=-time| head")
    else:
        cmd = os.popen("ps -eo user,pid,cmd,%cpu,%mem,time --sort=-%cpu | head")

    res = cmd.read()
    stdscr.addstr(nbligne+5, 0, res+"     " )

    time.sleep(.5)
finally:
  curses.endwin()


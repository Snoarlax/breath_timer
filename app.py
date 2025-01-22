#!/usr/bin/env python3
import os
import gi
import time
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from playsound import playsound

APPINDICATOR_ID = 'breath_timer'
INTERVAL = 10
BREATH_DURATION = 4
OUT_ICON=os.path.dirname(os.path.realpath(__file__))+"/exhale.svg"
IN_ICON=os.path.dirname(os.path.realpath(__file__))+"/breathe.svg"
SOUND_ENABLED = True

def breathe_sound():
    playsound_args = (os.path.dirname(os.path.realpath(__file__))+"/sound.mp3",)
    sound_thread = threading.Thread(target=playsound, args=playsound_args)
    sound_thread.daemon = True
    sound_thread.start()

def breathe_in():
    print("Breathe in")
    if SOUND_ENABLED:
        breathe_sound()
    indicator.set_icon(IN_ICON)

def breathe_out():
    print("Breathe out")
    indicator.set_icon(OUT_ICON)

def breathe_loop():
    while True:
        breathe_in()
        time.sleep(BREATH_DURATION)
        breathe_out()
        time.sleep(INTERVAL-BREATH_DURATION)

def quit_app(_):
    print("Quitting...")
    gtk.main_quit()

def toggle_sound(_):
    global SOUND_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED
    toggle_sound_menu.set_label("Sound Enabled" if SOUND_ENABLED else "Sound Disabled")
    print(f'Toggle sound: Now {SOUND_ENABLED}')

def get_menu():
    menu = gtk.Menu()
    quit_menu = gtk.MenuItem(label="Quit")
    quit_menu.connect('activate', quit_app)
    menu.append(quit_menu)

    global toggle_sound_menu
    toggle_sound_menu = gtk.MenuItem(label="Sound Enabled")
    toggle_sound_menu.connect("activate", toggle_sound)
    menu.append(toggle_sound_menu)

    menu.show_all()
    return menu

def main():
    global indicator 
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, OUT_ICON, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(get_menu())

    breathing_thread = threading.Thread(target=breathe_loop)
    breathing_thread.daemon = True
    breathing_thread.start()

    gtk.main()

if __name__ == "__main__":
    main()

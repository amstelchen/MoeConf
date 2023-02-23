#!/usr/bin/env python3

import sys
import os
import shutil
import platform
import tkinter as tk
from tkinter import messagebox
import urllib.request
from pathlib import Path
import subprocess
import logging
# from gi.repository import Gio

APP_NAME = "Moebuntu-Configurator"
VERSION = "0.1.0"
AUTHOR = "Copyright (C) 2023, by Michael John"
DESC = "A Tk frontend for MoeMoebuntu Setting Helper 2 (Moebuntu-SetupHelperScript2)"
GithubLink = "https://github.com/amstelchen/MoeConf"

# ====== COLORS ======
COL_BLACK = "\x1b[30;01m"
COL_RED = "\x1b[31;01m"
COL_GREEN = "\x1b[32;01m"
COL_YELLOW = "\x1b[33;01m"
COL_MAGENTA = "\x1b[35;01m"
COL_CYAN = "\x1b[36;01m"
COL_WHITE = "\x1b[37;01m"
COL_BLUE = "\x1b[34;01m"
COL_RESET = "\x1b[39;49;00m"

Repo = "Moebuntu-kawaiiUbuntu-ToysOriginal"
BaseUrl = "https://github.com/mifjpn/" + Repo + "/raw/22.04Lts/"
# ====== theme urls ======
ThemePink = BaseUrl + "themes/Moe-Pink16.tar.xz"
ThemeBlue = BaseUrl + "themes/Moe-Blue16.tar.xz"
ThemeGreen = BaseUrl + "themes/Moe-Green16.tar.xz"
ThemeBlueGreen = BaseUrl + "themes/Moe-BlueGreen16.tar.xz"
ThemeNavy = BaseUrl + "themes/Moe-Navy16.tar.xz"
ThemeOrange = BaseUrl + "themes/Moe-Orange16.tar.xz"
ThemePurple = BaseUrl + "themes/Moe-Purple16.tar.xz"
ThemeRed = BaseUrl + "themes/Moe-Red16.tar.xz"
ThemeYellow = BaseUrl + "themes/Moe-Yellow16.tar.xz"
# ====== login default picture(png) URL ======
LoginDefaltPicture = BaseUrl + "themes/login-default.png"
# ====== Sound URL ======
Soundiori = BaseUrl + "sound/Moesound_iori.tar.gz"
Soundmaid_iori = BaseUrl + "sound/Moesound_maid_iori.tar.gz"
SoundSF_iori = BaseUrl + "sound/Moesound_SF_iori.tar.gz"
SoundMGd = BaseUrl + "sound/Moesound_MGd.tar.gz"
# ====== MoeIcon variable ====
MoeIconUrl = BaseUrl + "icons/MoePinkIcons_201117.tar.xz"
SYSIconDir = "/usr/share/icons"
DefaultIconName = "Yaru"
# ====== Plymouth Theme ======
MoePlymouthURL = BaseUrl + "plymouth/mmspinner.tar.xz"
MoePlymouthDirName = "mmspinner"
PlymothThemePath = "/usr/share/plymouth/themes"
MoePlymouthBackGroundFile = PlymothThemePath + "/mmspinner/background-tile.png"
MoeAlternativesPath = "/usr/share/plymouth/themes/mmspinner/mmspinner.plymouth"
DetaultAlternativesPath = "/usr/share/plymouth/themes/bgrt/bgrt.plymouth"
PlymouthDefaultPngUrl = BaseUrl + "plymouth/plymouth-default.png"

extman = ['Please follow these steps to enable User Themes on Ubuntu:',
          '1. Search for "User Themes" in the "Browse" tab.',
          '2. Click the "Install" button to install.',
          '3. Go to the "Installed" tab and activate the Extension'
          'by setting the switch on the header to "ON" (to the right).',
          'If there is no switch in the header and there is a switch '
          'in "use extention", please turn it "ON" (slide to the right).',
          '4. Turn on the switch to the right of "User Themes".']


def show_info():
    pretty_name = platform.freedesktop_os_release()['PRETTY_NAME']
    messagebox.showinfo(
        title=APP_NAME,
        message=f"{APP_NAME} {VERSION}\n{AUTHOR}\n"
                f"{GithubLink}\n\n"
                f"{DESC}\n\n"
                f"OS Version: {pretty_name}\n"
                f"Python version: {sys.version.split()[0]}\n")


def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    # win.withdraw()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def run_script(s):
    logging.info(s)
    try:
        result = subprocess.run(s, capture_output=True, shell=True, check=True)
        logging.info(result.stdout.decode("utf-8"))
    except subprocess.CalledProcessError as e:
        logging.info(e)


def set_theme(Theme):
    path = "/tmp/" + Theme.split("/")[-1]
    if not os.path.exists(path):
        local_filename, headers = \
            urllib.request.urlretrieve(Theme, filename=path)
        run_script("sudo tar Jxfv " + path + " -C " + "/usr/share/themes/")
    logging.info(" unpack $ThemeFileName=")
    logging.info(" copy to system theme folder")
    # change theme gsetting
    logging.info(" change theme gsettings")
    ThemeName = Path(Theme.split("/")[-1]).with_suffix('').stem
    run_script("gsettings set org.gnome.desktop.interface gtk-theme " + ThemeName)
    run_script("gsettings set org.gnome.shell.extensions.user-theme name " + ThemeName)

    # key = "org.gnome.desktop.interface"
    # settings = Gio.Settings.new(key)
    # settings = Gio.Settings.set_string("gtk-theme", ThemeName)
    # settings.set_string("app-shortcuts", "enabled")


def set_icons(Iconset):
    path = "/tmp/" + Iconset.split("/")[-1]
    if not os.path.exists(path):
        logging.info(" download $MoeIconFileName")
        local_filename, headers = urllib.request.urlretrieve(Iconset, filename=path)
        logging.info(" unpack $MoeIconFileName")
        run_script("sudo tar Jxfv " + path + " -C " + "/usr/share/icons/ > /dev/null 2> /dev/null")
    # MoeIconName = Path(Iconset.split("/")[-1]).with_suffix('').stem
    MoeIconName = "MoePinkIcons"
    run_script("gsettings set org.gnome.desktop.interface icon-theme " + MoeIconName)


def set_boot():
    path = "/tmp/" + MoePlymouthURL.split("/")[-1]
    if not os.path.exists(path):
        logging.info(" download $MoePlymouthFileName ")
        local_filename, headers = urllib.request.urlretrieve(MoePlymouthURL, filename=path)
        logging.info(" unpack $MoePlymouthFileName")
        run_script("sudo tar Jxfv " + path + " -C " + PlymothThemePath + " > /dev/null 2> /dev/null")
    logging.info(" set plymouth altanative")
    logging.info("  install alternative default.plymouth $MoeAlternativesPath")
    run_script("sudo update-alternatives --install /usr/share/plymouth/themes/default.plymouth default.plymouth " +
               MoeAlternativesPath + " 20 >/dev/null 2>/dev/null")
    logging.info("  set altanatives default.plymouth $MoeAlternativesPath")
    run_script("sudo update-alternatives --set default.plymouth " + MoeAlternativesPath + " >/dev/null 2>/dev/null")


def def_boot():
    logging.info(" remove $MoePlymouthDirName")
    # run_script("sudo rm -rf "+ PlymothThemePath + "/" + MoePlymouthDirName)
    logging.info(" remove alternatives $MoeAlternativesPath")
    run_script("sudo update-alternatives --remove default.plymouth " + MoeAlternativesPath + " >/dev/null 2>/dev/null")
    logging.info(" set alternatives $DetaultAlternativesPath")
    run_script("sudo update-alternatives --set default.plymouth " + DetaultAlternativesPath + " >/dev/null 2>/dev/null")


def set_login():
    path = "/tmp/" + MoePlymouthBackGroundFile.split("/")[-1]
    logging.info(" download default login picture")
    local_filename, headers = urllib.request.urlretrieve(PlymouthDefaultPngUrl, filename=path)
    logging.info(" set default plymouth picture")
    run_script("sudo cp " + path + " " + MoePlymouthBackGroundFile)
    run_script("sudo update-initramfs -u -k all")


def loginsound(action=None, SoundUrl=None):
    if action == "install":
        path = "/tmp/" + SoundUrl.split("/")[-1]
        logging.info(" download $SoundFileName")
        local_filename, headers = urllib.request.urlretrieve(SoundUrl, filename=path)
        logging.info(" unpack $SoundFileName")
        run_script("sudo tar -xf " + path + " -C /usr/share/sounds/ > /dev/null 2> /dev/null")
        logging.info(" copy to system theme folder")

        # run_script("mkdir -p ~/.config/autostart")
        os.makedirs(os.path.expanduser("~/.config/autostart"), exist_ok=True)
        # run_script("cp login-sound.desktop ~/.config/autostart")
        print(shutil.copy2("scripts/login-sound.desktop", os.path.expanduser("~/.config/autostart")))
    if action == "remove":
        # run_script("rm ~/.config/autostart/login-sound.desktop")
        os.unlink(os.path.expanduser("~/.config/autostart/login-sound.desktop"))


def firefox2deb():
    logging.info("TBD")


def firefox2snap():
    logging.info("TBD")


def action(s):
    logging.info("Action:" + s)
    if s == "base setting (do first!)":
        run_script("sudo apt-get -y install gnome-shell-extension-manager")
        messagebox.showinfo(title=APP_NAME, message="\n\n".join(extman))

    if s == "set theme Pink":
        set_theme(ThemePink)
    if s == "set theme Blue":
        set_theme(ThemeBlue)
    if s == "set theme Green":
        set_theme(ThemeGreen)
    if s == "set theme BlueGreen":
        set_theme(ThemeBlueGreen)
    if s == "set theme Navy":
        set_theme(ThemeNavy)
    if s == "set theme Orange":
        set_theme(ThemeOrange)
    if s == "set theme Purple":
        set_theme(ThemePurple)
    if s == "set theme Yellow":
        set_theme(ThemeYellow)
    if s == "set theme Red":
        set_theme(ThemeRed)

    if s == "remove Moe-theme":
        logging.info("=Set theme to default(Yaru)=")
        run_script("gsettings set org.gnome.desktop.interface gtk-theme Yaru")
        run_script("gsettings set org.gnome.shell.extensions.user-theme name Yaru")
        logging.info("Done")

    if s == "set Moe-Pink-Icons":
        set_icons(MoeIconUrl)

    if s == "remove Moe-Pink-Icons":
        run_script("gsettings set org.gnome.desktop.interface icon-theme " + DefaultIconName)

    if s == "set Moe-spinner plymouth":
        set_boot()
        set_login()

    if s == "remove Moe-spinner plymouth":
        def_boot()

    if s == "set Moe Wallpaper":
        #run_script("/bin/bash wallmanager install ;")
        logging.info("TBD")

    if s == "remove Moe Wallpaper":
        #run_script("/bin/bash wallmanager remove ;")
        logging.info("TBD")

    if s == "firefox to deb package":
        firefox2deb()

    if s == "firefox to snap package":
        firefox2snap()

    if s == "set Moesound_iori":
        loginsound("install", Soundiori)
    if s == "set Moesound_maid_iori":
        loginsound("install", Soundmaid_iori)
    if s == "set Moesound_SF_iori":
        loginsound("install", SoundSF_iori)
    if s == "set Moesound_MGd":
        loginsound("install", SoundMGd)
    if s == "remove Moesound":
        loginsound("remove")

    if s == "About":
        show_info()
    if s == "Quit":
        sys.exit()


def menu():
    # if os.environ["USER"] != "root":
    # print("Please run as root.")
    # sys.exit()

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    win = tk.Tk()
    win.title(APP_NAME)

    # content = tk.Frame(win)
    # frame = tk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
    # win.geometry("500x480")
    # win.eval('tk::PlaceWindow . center')

    options = [
        'base setting (do first!)',
        'set theme Pink',
        'set theme Blue',
        'set theme Green',
        'set theme BlueGreen',
        'set theme Navy',
        'set theme Orange',
        'set theme Purple',
        'set theme Red',
        'set theme Yellow',
        'remove Moe-theme',
        'set Moe-Pink-Icons',
        'remove Moe-Pink-Icons',
        'set Moe-spinner plymouth',
        'remove Moe-spinner plymouth',
        'set Moe Wallpaper',
        'remove Moe Wallpaper',
        'firefox to deb package',
        'firefox to snap package',
        'set Moesound_iori',
        'set Moesound_maid_iori',
        'set Moesound_SF_iori',
        'set Moesound_MGd',
        'remove Moesound',
    ]

    options2 = [
        'About',
        'Quit'
    ]

    btn = []
    btn2 = []
    for option in range(len(options)):
        btn.append(tk.Button(win, text=options[option],
                   command=lambda c=option: action(btn[c].cget("text")), width=30, height=2))
        btn[option].grid(row=option // 2, column=option % 2 + 1, padx=5, pady=5)

    for option2 in range(len(options2)):
        btn2.append(tk.Button(win, text=options2[option2],
                    command=lambda c=option2: action(btn2[c].cget("text")), width=30, height=2))
        btn2[option2].grid(row=13 + option2 // 2, column=option2 % 2 + 1, padx=5, pady=5)

    center(win)
    win.mainloop()


# def main():
menu()

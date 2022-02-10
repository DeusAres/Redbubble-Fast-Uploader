import json
import os
import sys
import threading
from base64 import b64decode
from io import BytesIO
from random import uniform
from time import sleep

import PySimpleGUI as sg
from PIL import Image

import layout
import redbubbleCopyWork as rcw
from classes import *

sg.LOOK_AND_FEEL_TABLE["DarkPoker"] = {
    "BACKGROUND": "#252525",
    "TEXT": "#FFFFFF",
    "INPUT": "#af0404",
    "TEXT_INPUT": "#FFFFFF",
    "SCROLL": "#af0404",
    "BUTTON": ("#FFFFFF", "#252525"),
    "BORDER": 1,
    "SLIDER_DEPTH": 0,
    "PROGRESS_DEPTH": 0,
    "COLOR_LIST": ["#252525", "#414141", "#af0404", "#ff0000"],
    "PROGRESS": ("# D1826B", "# CC8019"),
}
sg.theme("DarkPoker")


def login():
    login = sg.Window(
        "Login",
        [
            [sg.Text("Username"), sg.Push(), sg.Input("", key="Username")],
            [
                sg.Text("Password"),
                sg.Push(),
                sg.Input("", password_char="*", key="Password"),
            ],
            [sg.Push(), sg.Button("Login")],
        ],
    )

    while True:
        event, values = login.read()

        if event == sg.WINDOW_CLOSED or event == "Quit":
            login.close()
            sys.exit()

        if event == "Login":
            driver = rcw.bot(
                values["Username"].strip("\n").strip(" "),
                values["Password"].strip("\n").strip(" "),
            )
            if driver.logged:
                break

    login.close()

def openPlaceholder():
    placeholder = "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"
    return BytesIO(b64decode(placeholder)).getvalue()

def work(ctitle="", ctags="", cdesc="", vtitle="", vtags="", vdesc=""):

    window = sg.Window("Redbubble upload", layout.create(ctitle, ctags, cdesc, vtitle, vtags, vdesc))

    # List of custom class entry (filename, preview, (x,y) 4 graph)
    listboxFiles = [] 

    # List of lists for displaying tasks
    queue = []

    # Keeper of the current task
    _index = index(0)

    # Useless, lazy me should remove it
    placeholder = openPlaceholder()

    # CHANGES STATUS OF CURRENT TASK
    def updateStatus(message):
        queue[_index.s][4] = message
        window["QUEUE"].Update(queue)
        window.refresh()

    # CHANGES PREVIEW ON GRAPH
    def clearAndSetPrev(pIndex):
        try:
            window['PREVIEW'].erase()
            theFile = listboxFiles[pIndex]
            window['PREVIEW'].draw_image(data=theFile.preview, location = theFile.xy)
        except:
            window['PREVIEW'].erase()
        window.refresh()

    # FORMAT TEXTBOXES DATAS
    def stripChar(data):
        return values[data].strip("\n").strip(" ").strip(",")

    # PARSING PRODUCT DATAS FOR UPLOAD OR EXPORT SETTINGS
    def parseDict(values):
        prod_data = {}
        for prod in values.keys():
            if 'prod_' in str(prod):
                each = prod.replace('prod_', '')
                prod_data[each] = {
                    'enabled' : values['prod_'+ each], 
                    'type' : values['type_'+ each]}
        return prod_data

    # TREADING THE PREVIEW LOADING
    def threadPreview():
        if listboxFiles:
            i = 0
            realLen = len(listboxFiles)
            while i < len(listboxFiles):

                # Acquiring a lock to prevent listbox modification
                # during saving the preview
                prevLock.acquire()

                # If changes have been made update index
                if len(listboxFiles) != realLen:
                    i = i - (realLen - len(listboxFiles))
                    realLen = len(listboxFiles)
                
                # Crop PNGs, resize and save to memory
                image = Image.open(listboxFiles[i].file).convert('RGBA')
                tupla = image.getbbox()
                image = image.crop(tupla)
                w, h = image.size
                s = layout.GSIZE*100 / max(w,h) / 100
                image.thumbnail((w*s, h*s))
                with BytesIO() as output:
                    image.save(output, format="PNG")
                    listboxFiles[i].updatePrev(output.getvalue(), (layout.GSIZE//2 - image.size[0]//2, layout.GSIZE//2 - image.size[1]//2))

                # TODO DELETE IF NOT NEEEDED FOR SHOWING
                try:
                    if i == window['LIST'].get_indexes()[0]:
                        clearAndSetPrev(i)
                except Exception as e:
                    print(e)

                i+=1
                    
                # Release the lock for changes
                prevLock.release()

    # THREADING THE UPLOAD (LOOPED)
    def upload():
        while True:
            try:
                # Waiting for pause or stop, updating task status
                status.wait()
                _stop.wait()
                updateStatus("Working")

                # Send data to selenium to upload the new copy with pause and stop objects
                rcw.driver.copy_thread(rcw.file(*queue[index][:5]), status, _stop)

                updateStatus("Cleared")
                _index.add()
                sleep(uniform(10, 20))

            # Stopping because of user or no more entries
            except Exit as e:
                # Changing button to Start and 
                # enabling if stopped
                # disabling if no more entries
                # disabling stop button and exiting thread
                window["SPR"].Update("Start")
                if str(e) == "Stopped":
                    window["SPR"].Update(disabled=False)
                elif str(e) == "All clear":
                    window["SPR"].Update(disabled=True)
                window["STOP"].Update(disabled=True)
                window.refresh()
                sys.exit()

            # Must admit, if gui buttons are spammed to much between 
            # Start/Pause/Resume and Stop IDK what happens
            except Exception as e:
                window["SPR"].Update('You are doing something terrible')
                window["STOP"].Update(disabled=True)
                sys.exit()

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Quit":
            break

        # CHANGING LISTBOX AND PREVIEWS
        if event == "IMAGES" and values["IMAGES"] != "":

            # Update listbox
            listboxFiles = []
            for path in os.listdir(values["IMAGES"]):
                full_path = os.path.join(values["IMAGES"], path)
                if os.path.isfile(full_path):
                    listboxFiles.append(entry(full_path))

            # Setting Listbox to first entry
            window["LIST"].Update([each.file for each in listboxFiles], set_to_index=0)

            # Load placeholder and eventually deletes previous
            window['PREVIEW'].erase()
            window['PREVIEW'].draw_image(data=placeholder)

            # Threading the image to bytes for previewing so non-blocking
            prevLock = threading.Lock()
            threadPrew = threading.Thread(target=threadPreview, daemon=True)
            threadPrew.start()

        # ADDING AND REMOVING FROM LISTBOX
        if event in ["Add", "Remove"]:

            # ADDING
            if event == "Add":
                # Checking that all datas are set before sending to queue
                if all([each != "" for each in [
                    "CTAGS","CDESC","CTITLE","VTAGS","VDESC","VTITLE"]]):
                    title = stripChar("CTITLE").replace("@text", stripChar("VTITLE"))
                    tags = stripChar("CTAGS") + ", " + stripChar("VTAGS")
                    desc = stripChar("CDESC").replace("@text", stripChar("VDESC"))

                    # Adding if listbox file is selected
                    if values["LIST"]:

                        # Enable start
                        window["SPR"].Update(disabled=False)
                        
                        # Append new entry to queue and update max index
                        # Entry is composed by
                        # File, title, desc, tags, products data, status
                        queue.append([values["LIST"][0], title, desc, tags, parseDict(values), "Pending"])
                        window['VTITLE'].Update('')
                        window['VDESC'].Update('')
                        window['VTAGS'].Update('')
                        window["QUEUE"].Update(queue)
                        window.refresh()
                        _index.update(len(queue))

                        # Remove from listbox waiting the thread
                        while prevLock.locked():
                            sleep(1)
                        toPop = window["LIST"].get_indexes()
                        listboxFiles.pop(toPop[0])

            # REMOVING
            if event == 'Remove':
                if values["LIST"]:
                    # Different from adding because it's possible
                    # to remove multiple files from listbox
                    toPop = window['LIST'].get_indexes()
                    toKeep = [i for i in range(len(listboxFiles)) if i not in toPop]
                    while prevLock.locked():
                        sleep(1)
                    listboxFiles = [listboxFiles[i] for i in toKeep]

            # ADDING AND REMOVING (BOTH LEAD TO SAME EFFECT)
            if values["LIST"]:
                # Auto-select a entry of listbox (previous one of added/removed)
                # Updating preview too
                pIndex = toPop[0]-1
                pIndex = pIndex if pIndex == 0 else pIndex-1
                window["LIST"].Update(
                    [each.file for each in listboxFiles], set_to_index=pIndex
                )
                clearAndSetPrev(pIndex)
                window.refresh()
                #TODO TEST

        # START, PAUSE, RESUME, ERROR BUTTONS
        if event == "SPR":
    
            # START BUTTON
            # Enabled by at least one entry added from listbox
            if window["SPR"].ButtonText == "Start":
                # Settings pause and stop 
                _stop = stop()
                status = threading.Event()

                # Waiting for old thread
                # Because why not? (I don't remember why I've added it...)
                try:
                    if thread.is_alive():
                        thread.join()
                except:
                    pass

                # Starting the upload thread in a not-paused status
                thread = threading.Thread(target=upload, daemon=True)
                thread.start()
                status.set()
                window["SPR"].Update("Pause")
                window["STOP"].Update(disabled=False)

            # PAUSE BUTTON
            elif window["SPR"].ButtonText == "Pause":
                # Pausing upload, updating task status, changing button text
                status.clear()
                window["SPR"].Update("Resume")
                updateStatus("Paused")

            # RESUME BUTTON
            elif window["SPR"].ButtonText == "Resume":
                # Resuming upload, updating task status, changing button text
                status.set()
                window["SPR"].Update("Pause")
                updateStatus("Working")

            # ERROR BUTTON
            elif window["SPR"].ButtonText == 'You are doing something terrible':
                # Welcome to coding hell
                sg.Popup('Restart the programm\nYou managed to bug it')

        # STOP BUTTON
        if event == "STOP":
            # Disabling Stop Button, enabling Start Button, updating task status
            # Removing pause and Enabling Stop
            window["STOP"].Update(disabled=True)
            window["SPR"].Update("Start")
            status.set()
            _stop.clear()
            updateStatus("Stopped")

        # PREVIEW CHANING
        if event == 'LIST':
            # Changing image preview of listbox
            try:
                clearAndSetPrev(window['LIST'].get_indexes()[0])
            except:
                pass
        
        # IMPORT SETTINGS FROM PRODUCT TAB
        if event == 'IMPORT':
            # Loades json file and parse into a dict for rcw module
            if values['IMPORT'] != '':
                with open(values['IMPORT'], 'r') as out:
                    prod_data = json.load(out)
                for each in prod_data.keys():
                    window['prod_'+each].Update(prod_data[each]['enabled'])
                    window['type_'+each].Update(prod_data[each]['type'])

        # EXPORT SETTINGS FROM PRODUCT TAB
        if event == 'EXPORT':
            if values['EXPORT'] != '':
                # Parse data for dumping json
                prod_data = parseDict(values)
                with open(values['EXPORT'], "w") as out:
                    json.dump(prod_data, out)

        # IMPORT TEXT FROM CONSTANT TAB
        if event == 'IMPORTTEXT':
            if values['IMPORTEXT'] != '':
                with open(values['IMPORTEXT'], 'r') as out:
                    textDict = json.load(out)
                for each in textDict.keys():
                    window[each].Update(textDict[each])

        # EXPORT TEXT FROM CONSTANT TAB
        if event == 'EXPORTTEXT':
            if values['EXPORTEXT'] != '':
                textDict = {
                    "CTITLE" : values['CTITLE'],
                    "CDESC" : values['CDESC'],
                    "CTAGS" : values['CTAGS'],
                }
                with open(values['EXPORTEXT'], 'w') as out:
                    json.dump(textDict, out)
                del textDict

        # TODO TEST IMPORT EXPORT TEXT





    window.close()

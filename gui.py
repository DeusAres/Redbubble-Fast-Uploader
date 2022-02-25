import traceback
import sys
import threading
from base64 import b64decode
from io import BytesIO
from random import uniform
from time import sleep
from playsound import playsound

import PySimpleGUI as sg
from PIL import Image

import layout
import redbubbleCopyWork as rcw
from classes import *
import functions as f

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
                login.close()
                return driver

def openPlaceholder():
    placeholder = None
    return BytesIO(b64decode(placeholder)).getvalue()

def work(driver, ctitle="", ctags="", cdesc="", vtitle="", vtags="", vdesc=""):

    window = sg.Window("Redbubble upload", layout.create(ctitle, ctags, cdesc, vtitle, vtags, vdesc))

    # List of custom class entry (filename, preview, (x,y) 4 graph)
    queuePreview = queue()

    # List of lists for displaying tasks
    queueUpload = queue()

    # Useless, lazy me should remove it
    #placeholder = openPlaceholder()


    # TREADING THE PREVIEW LOADING
    def threadPreview():
        try:
            if queuePreview:
                i = 0
                realLen = queuePreview.len()
                while i < queuePreview.len():

                    # Acquiring a lock to prevent listbox modification
                    # during saving the preview
                    prevLock.acquire()

                    # If changes have been made update index
                    if queuePreview.len() != realLen:
                        i = i - (realLen - queuePreview.len())
                        realLen = queuePreview.len()
                    
                    # Crop PNGs, resize and save to memory
                    image = Image.open(queuePreview[i].file).convert('RGBA')
                    tupla = image.getbbox()
                    image = image.crop(tupla)
                    w, h = image.size
                    s = layout.GSIZE*100 / max(w,h) / 100
                    image.thumbnail((w*s, h*s))
                    with BytesIO() as output:
                        image.save(output, format="PNG")
                        queuePreview[i].updatePreview(output.getvalue(), (layout.GSIZE//2 - image.size[0]//2, layout.GSIZE//2 - image.size[1]//2))

                    # TODO DELETE IF NOT NEEEDED FOR SHOWING
                    try:
                        if i == window['LIST'].get_indexes()[0]:
                            pass#clearAndSetPrev(i)
                    except Exception as e:
                        print(e)

                    i+=1
                    # Release the lock for changes
                    prevLock.release()

        except:
            try:
                prevLock.release()
            except:
                pass
                
    # THREADING THE UPLOAD (LOOPED)
    def upload():
        while True:
            try:
                # Waiting for pause or stop, updating task status
                status.wait()
                _stop.wait()
                f.updateStatus(window, queueUpload, "Working")
                file = queueUpload.getCurrentFile()
                # Send data to selenium to upload the new copy with pause and stop objects
                driver.copy_thread(file, status, _stop)

                if file.pin is True:
                    driver.pin(file)
                
                f.moveToCompleted(file)
                f.updateStatus(window, queueUpload, "Sleeping")
                sleep(uniform(100, 200))
                f.updateStatus(window, queueUpload, "Cleared")
                queueUpload.next()

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
                playsound("ka-ching.mp3")
                sys.exit()

            # Must admit, if gui buttons are spammed to much between 
            # Start/Pause/Resume and Stop IDK what happens
            except Exception as e:
                #window["SPR"].Update('You are doing something terrible')
                print(traceback.format_exc())
                window["STOP"].Update(disabled=True)
                window.refresh()
                playsound("ka-ching.mp3")
                sys.exit()

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Quit":
            break

        # CHANGING LISTBOX AND PREVIEWS
        if event == "IMAGES" and values["IMAGES"] != "":
            
            queuePreview = f.addImagesToListbox(queuePreview, values['IMAGES'])
            # Setting Listbox to first entry
            window["LIST"].Update(queuePreview.displayListbox(), set_to_index=0)

            # Load placeholder and eventually deletes previous
            window['PREVIEW'].erase()
            window['PREVIEW'].draw_image(data=None)

            # Threading the image to bytes for previewing so non-blocking
            prevLock = threading.Lock()
            threadPrew = threading.Thread(target=threadPreview, daemon=True)
            threadPrew.start()

        # ADDING AND REMOVING FROM LISTBOX
        if event in ["Add", "Remove"] and values["LIST"] :
            #TODO INPUT NONE
            # ADDING
            if event == "Add":

                # Adding if listbox file is selected
                if f.dataReadyForUpload(values):
                    
                    while prevLock.locked():
                        sleep(1)
                    
                    # Enable start
                    window["SPR"].Update(disabled=False)
                    
                    title, tags, desc = f.parseStringsForUpload(values)
                    products = f.parseDict(values)
                    types = f.parseType(products)
                    color = f.colorOverride(values)
                    
                    while prevLock.locked():
                        sleep(1)

                    index = window["LIST"].get_indexes()[0]
                    queuePreview[index].addData(
                        title, tags, desc, types,
                        color, products
                    )

                    while prevLock.locked():
                        sleep(1)

                    pin = f.pinOverride(values)
                    if pin is not False:
                        queuePreview[index].addPin(*pin)

                    queueUpload.append(queuePreview[index])
                    queuePreview.pop(index)

                    while prevLock.locked():
                        sleep(1)

                    f.clearVariable(window)
                    
                        
            # REMOVING
            elif event == 'Remove':
                # Different from adding because it's possible
                # to remove multiple files from listbox
                queuePreview.popMultiple(window['LIST'].get_indexes())


            # ADDING AND REMOVING (BOTH LEAD TO SAME EFFECT)
            # Auto-select a entry of listbox
            # Updating preview too
            while prevLock.locked():
                sleep(1)
            _index = f.setListboxIndex(window, queuePreview)
            window["QUEUE"].Update(queueUpload.displayUpload())
            f.clearAndSetPrev(_index, window, queuePreview)
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
                f.updateStatus(window, queueUpload, "Paused")

            # RESUME BUTTON
            elif window["SPR"].ButtonText == "Resume":
                # Resuming upload, updating task status, changing button text
                status.set()
                window["SPR"].Update("Pause")
                f.updateStatus(window, queueUpload, "Working")

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
            f.updateStatus(window, queueUpload, "Stopped")

        # PREVIEW CHANING
        if event == 'LIST':
            # Changing image preview of listbox
            f.clearAndSetPrev(window['LIST'].get_indexes()[0], window, queuePreview)
            
        # IMPORT SETTINGS TO PRODUCT TAB
        if event == 'IMPORT' and values[event] != "":
            f.importProduct(values['IMPORT'], window)
            
        # EXPORT SETTINGS FROM PRODUCT TAB
        if event == 'EXPORT' and values[event] != "":
            f.exportProduct(values['EXPORT'], values)
            
        # IMPORT TEXT TO CONSTANT TAB
        if event == 'IMPORTTEXT' and values[event] != "":
            f.importConstantText(values['IMPORTTEXT'], window)

        # EXPORT TEXT FROM CONSTANT TAB
        if event == 'EXPORTTEXT' and values[event] != "":
            f.exportConstantText(values['EXPORTTEXT'], values)

        # TODO TEST IMPORT EXPORT TEXT

    window.close()

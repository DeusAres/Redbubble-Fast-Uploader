import os
import json
from classes import *
import traceback


# =====================================================
# ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  
# ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  
# ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗
#  ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                  
#  ██████╗ ██╗   ██╗██╗                             
# ██╔════╝ ██║   ██║██║                             
# ██║  ███╗██║   ██║██║                             
# ██║   ██║██║   ██║██║                             
# ╚██████╔╝╚██████╔╝██║                             
#  ╚═════╝  ╚═════╝ ╚═╝                             
# =====================================================


def addImagesToListbox(queuePreview, folder):
    """
    Add images (entries) to listbox gui
    folder : str to image

    return list of entry objects
    """
    
    for path in os.listdir(folder):
        if path.casefold().endswith('.jpg'.casefold()) or path.casefold().endswith('.png'.casefold()):
            full_path = os.path.join(folder, path)
            if os.path.isfile(full_path):
                queuePreview.append(entry(full_path))

    return queuePreview

def setListboxIndex(window, queuePreview):
    """
    Set the correct index for window after removing or adding

    window : sg.Window
    queuePreview : class Queue object for listbox

    return index
    """
    index = window['LIST'].get_indexes()[0]
    if index <= 0:
        index = 0
    if index == len(window['LIST'].Values)-1:
        index -= 1

    window['LIST'].Update(
        queuePreview.displayListbox(), set_to_index=index
    )

    return index
    
def clearVariable(window):
    """
    Clear variable entry fields for new products

    window : sg.Window

    return None
    """
    window['VTITLE'].Update('')
    window['VDESC'].Update('')
    window['VTAGS'].Update('')
    window['VCOLOR'].Update('')

def updateStatus(window, queueUpload, message):
    """
    Shows status in upload section of GUI

    _index : index obj
    window : sg.Window
    queueUpload : queue obj
    message : status of task (str)

    return None
    """
    queueUpload.updateStatus(message)
    window["QUEUE"].Update(queueUpload.displayUpload())
    window.refresh()

def clearAndSetPrev(pIndex, window, queuePreview):
    try:
        window['PREVIEW'].erase()
        image = queuePreview[pIndex]
        window['PREVIEW'].draw_image(data=image.preview, location = image.xy)
    except Exception as e:
        window['PREVIEW'].erase()
    window.refresh()   


# =====================================================
# ██████╗  █████╗ ██████╗ ███████╗███████╗
# ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝
# ██████╔╝███████║██████╔╝███████╗█████╗  
# ██╔═══╝ ██╔══██║██╔══██╗╚════██║██╔══╝  
# ██║     ██║  ██║██║  ██║███████║███████╗
# ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝
                                        
# ██████╗  █████╗ ████████╗ █████╗        
# ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗       
# ██║  ██║███████║   ██║   ███████║       
# ██║  ██║██╔══██║   ██║   ██╔══██║       
# ██████╔╝██║  ██║   ██║   ██║  ██║       
# ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝       
# =====================================================                                        


def dataReadyForUpload(values):
    """
    Checking that all datas are set before sending to queue
    values : data from sg.Window.read()[1]

    return boolean
    """
    vtexts = all(
                [values[each] != "" for each in ["VTAGS","VDESC","VTITLE"]]
            )
    ctexts = all(
                [values[each] != "" for each in ["CTAGS","CDESC","CTITLE"]]
            )
    return (
        True in [vtexts, ctexts]
        and 
        True in [values[each] != '' and values[each] != 'None' for each in ["VCOLOR", "CCOLOR"]])

def parseStringsForUpload(values):
    """
    values : data from sg.Window.read()[1]

    return title, tags, desc
    """
    def stripChar(values, data):
        return values[data].strip("\n").strip(" ").strip(",")

    title = stripChar(values, "CTITLE").replace("@text", stripChar(values, "VTITLE"))
    tags = stripChar(values, "CTAGS") + ", " + stripChar(values, "VTAGS")
    tags = tags.strip(',')
    desc = stripChar(values, "CDESC").replace("@text", stripChar(values, "VDESC"))
    return title, tags, desc

def parseDict(values):
    """
    Parse product data for upload or export settings
    Needs to be done because the GUI shows 2 type of datas
    A check if needs to be changed and a list on what change

    values : data from sg.Window.read()[1]

    return dict = { product_name : { "enabled" : bool , "type" : str}, ... }
    """
    prod_data = {}
    for prod in values.keys():
        if 'prod_' in str(prod):
            each = prod.replace('prod_', '')
            prod_data[each] = {
                'enabled' : values['prod_'+ each], 
                'type' : values['type_'+ each]}

    return prod_data

def parseType(prod_data):
    """
    Counts single types of variations of image to create
    new images variations for upload on redbubble

    prod_data : dict of products info

    return list of variations (str)
    """
    types = [each['type'] for each in prod_data.values() if each['enabled']]
    return list(dict.fromkeys(types))

def colorOverride(values):
    """
    Variable Color has priority over Constant Color
    to be sent to upload

    values : sg.Window.read()[1]

    return hex color (str)
    """
    if values['VCOLOR'] != '' and values['VCOLOR'] != 'None':
        color = values['VCOLOR']
    else:
        color = values['CCOLOR']

    return color

def pinOverride(values):
    """
    Variable Pin and its datas has priority over Constant Pin Data's

    values : sg.Window.read()[1]

    return False or (board, section)
    """
    if values['VPIN'] == 'Yes':
        board = values['VBOARD'].strip('\n').strip(' ')
        section = values['VSECTION'].strip('\n').strip(' ')
        if section in ['None', '']:
            section = None
        return board, section

    elif values['VPIN'] == 'No':
        return False
    
    elif values['VPIN'] == 'Use Constant':
        if values['CPIN'] == 'Yes':
            board = values['CBOARD'].strip('\n').strip(' ')
            section = values['CSECTION'].strip('\n').strip(' ')
            if section in ['None', '']:
                section = None
            return board, section
        elif values['CPIN'] == 'No':
            return False


# =====================================================
# ██╗███╗   ███╗██████╗  ██████╗ ██████╗ ████████╗  
# ██║████╗ ████║██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝  
# ██║██╔████╔██║██████╔╝██║   ██║██████╔╝   ██║     
# ██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗   ██║     
# ██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║   ██║     
# ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝     
                                                  
# ███████╗██╗  ██╗██████╗  ██████╗ ██████╗ ████████╗
# ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝
# █████╗   ╚███╔╝ ██████╔╝██║   ██║██████╔╝   ██║   
# ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══██╗   ██║   
# ███████╗██╔╝ ██╗██║     ╚██████╔╝██║  ██║   ██║   
# ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
# =====================================================


def importProduct(file, window):
    """
    Loades json file and parse into a dict to be readed by GUI

    file : path to file (str)
    window : sg.Window
    
    return None
    """
    with open(file, 'r') as out:
        prod_data = json.load(out)
    for each in prod_data.keys():
        window['prod_'+each].Update(prod_data[each]['enabled'])
        window['type_'+each].Update(prod_data[each]['type'])

def exportProduct(file, values):  
    """
    Dumps json file with data from product tab 

    file : path to file (str)
    values : sg.Window.read()[1]

    return None
    """
    prod_data = parseDict(values)
    with open(file, "w") as out:
        json.dump(prod_data, out)

def importConstantText(file, window):
    """
    Loads json file and updates constant tab entry fields

    file : path to file (str)
    window : sg.Window
    
    return None
    """
    with open(file, 'r') as out:
        textDict = json.load(out)
    for each in textDict.keys():
        window[each].Update(textDict[each])
    del textDict

def exportConstantText(file, values):
    """
    Dumps json file with data from product tab 

    file : path to file (str)
    values : sg.Window.read()[1]

    return None
    """
    textDict = {
        "CTITLE" : values['CTITLE'],
        "CDESC" : values['CDESC'],
        "CTAGS" : values['CTAGS'],
        "CCOLOR" : values['CCOLOR'],
    }
    with open(file, 'w') as out:
        json.dump(textDict, out)
    del textDict

# =====================================================
# ███╗   ███╗██╗███████╗ ██████╗
# ████╗ ████║██║██╔════╝██╔════╝
# ██╔████╔██║██║███████╗██║     
# ██║╚██╔╝██║██║╚════██║██║     
# ██║ ╚═╝ ██║██║███████║╚██████╗
# ╚═╝     ╚═╝╚═╝╚══════╝ ╚═════╝
# =====================================================                            

def moveToCompleted(file):
    """
    Move file to a folder called "complete"
    Create the folder if it doesn't exist
    
    file : path to file (str)

    return None
    """
    completed = Path(file.file).parent / "completed"
    if not os.path.exists(completed):
        os.mkdir(completed)

    os.rename(file, completed / (Path(file).name))
 
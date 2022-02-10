import PySimpleGUI as sg
import redbubbleCopyWork as rcw

GSIZE = 300

def create(ctitle, ctags, cdesc, vtitle, vtags, vdesc):

    # WHERE CONST DATA END
    constant = [
        [
            sg.Column(
                [
                    [sg.Input(enable_events=True, key='IMPORTTEXT', visible=False), 
                    sg.FileBrowse('Import settings', file_types=(('JSON', '.json'),), target='IMPORTTEXT'),
                    sg.Input(enable_events=True, key='EXPORTTEXT', visible=False), 
                    sg.FileSaveAs('Export settings', file_types=(('JSON', '.json'),), target='EXPORTTEXT')],
                    [sg.Text("Title"), sg.Push(), sg.Multiline(ctitle, key="CTITLE")],
                    [sg.Text("Tags"), sg.Push(), sg.Multiline(ctags, key="CTAGS")],
                    [sg.Text("Description"), sg.Push(), sg.Multiline(cdesc, key="CDESC")],
                ]
            )
        ]
    ]

    # WHERE VARIABLED DATA END
    variable = [
        [
            sg.Column(
                [
                    [sg.Text("Title"), sg.Push(), sg.Multiline(vtitle, key="VTITLE")],
                    [sg.Text("Tags"), sg.Push(), sg.Multiline(vtags, key="VTAGS")],
                    [sg.Text("Description"), sg.Push(), sg.Multiline(vdesc, key="VDESC")],
                ]
            )
        ]
    ]

    # NEEDED FOR FILE VARIATIONS
    listbox = ['rotated', 'sticker', 'rotatedSticker']
    # PRODUCTS VARIATIONS ANS IMPORT/EXPORT
    products = [
        [   
            sg.Column([
                [
                    sg.Input(enable_events=True, key='IMPORT', visible=False), 
                    sg.FileBrowse('Import settings', file_types=(('JSON', '.json'),), target='IMPORT'),
                    sg.Input(enable_events=True, key='EXPORT', visible=False), 
                    sg.FileSaveAs('Export settings', file_types=(('JSON', '.json'),), target='EXPORT')
                ],
                *[[sg.Checkbox(str(each), key='prod_'+each), 
                sg.Push(), 
                sg.Combo(listbox, default_value='rotated', key='type_'+each)] 
                        for each in rcw.products.keys()]
            ], scrollable=True, key='CHECKS')
        ]
    ]

    # IMAGE PREVIEW SIZE

    layout = [
        [   
            # TAB FOR CHOSING DISPLAYING
            sg.Column([
                [sg.TabGroup([
                    [
                        sg.Tab("Fixed", constant), 
                        sg.Tab("Variable", variable),
                        sg.Tab('Products', products)
                    ]
                ], size=(550, 300))],
            ]),

            # LIST OF FILE
            sg.Column(
                [
                    [
                        sg.Text("Folder"),
                        sg.Input(key="IMAGES", enable_events=True),
                        sg.Push(),
                        sg.FolderBrowse("Browse", target="IMAGES"),
                    ],
                    [
                        sg.Listbox(
                            [],
                            enable_events=True,
                            select_mode=sg.SELECT_MODE_EXTENDED,
                            size=(50, 10),
                            key="LIST",
                        ),
                        sg.Column(
                            [
                                [sg.Button("Add", s=(10, 1))],
                                [sg.Button("Remove", s=(10, 1))],
                            ]
                        ),
                    ],
                ],
                element_justification="center",
            ),

            # IMAGE PREVIEW
            sg.Column([
                [sg.Push(), sg.Text("Preview", ), sg.Push()],
                [sg.Graph((GSIZE, GSIZE), (0, GSIZE), (GSIZE, 0), key='PREVIEW')]
            ])
        ],


        # UPLOAD QUEUE AND BUTTONS
        [
            # QUEUE
            sg.Table(
                values=[
                    ["Welcome to", "redbubble uploader!", "To begin", "select a folder", "select an image", "////////////"],
                    ["write the proper data", "and add it", "to the queue.", "You can start and", "stop whenever", "////////////"],
                    ["you want.", "Enjoy your free", "time without uploading", "every image", "manually :)", "////////////"]
                ],  
                def_col_width=1000,
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                headings=["File", "Title", "Tags", "Description", "Products", "Status"],
                display_row_numbers=True,
                justification="center",
                p=((0, 0), (20, 0)),
                key="QUEUE",
            ),
            # BUTTONS
            sg.Column(
                [
                    [sg.Button("Start", disabled=True, size=(15, 2), key="SPR")],
                    [sg.Button("Stop", disabled=True, size=(15, 2), key="STOP")],
                ]
            ),
        ],
    ]

    return layout
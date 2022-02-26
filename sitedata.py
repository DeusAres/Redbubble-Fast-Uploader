editButton = "//div[@data-type='@REPLACE']//div[@class='rb-button edit-product'][normalize-space()='Edit']"
oldUpload = "//div[contains(@class,'upload-button-wrapper')]//input[@id='select-image-@REPLACE']"
newUpload = "//div[contains(@class,'app-entries-uploaderPage-components-ReplaceDesign-ReplaceDesign_button_je6ss')]//input[@id='select-image-@REPLACE']"

products =  {
    "Standard Print Clothing": ["mens", "clothing", "old"],
    "Large Print Clothing" : ["large_clothing", "large_clothing", 'new'],
    "Caps" : ["cap", "cap", 'new'],
    "Chiffon Tops" : ["womens_panel_clothing", "womens_panel_clothing", 'new'],
    "Graphic T-shirt Dresses" : ["panel_dress", "panel_dress", 'new'],
    "Graphic T-shirt" : ["panel_clothing", "panel_clothing", 'new'],
    "A-Line Dresses" : ["trapeze_dress", "trapeze_dress", 'new'],
    "Stickers & Magnets" : ["sticker", "sticker", 'new'],
    "Phone Cases & Skins" : ["phone", "phone", "new"],
    "Desk Mat" : ["desk_mat", "desk_mat", 'new'],
    "Mouse Pad" : ["mouse_pad", "mouse_pad", 'new'],
    "Pillows & Totes" : ["thow_pillow", "thow_pillow", 'new'],
    "Prints, Cards & Posters" : ["print", "print", "old"],
    "Pouches, Laptop Skins & Sleeves" : ["laptop", "laptop", 'new'],
    "Duvets, Comforters & Shower Curtains" : ['duvet', 'duvet', 'new'],
    "Mugs" : ['mugs', 'mugs', 'old'],
    "Travel Mugs" : ["travel_mug", 'travel_mug', 'old'],
    "Mini Skirts" : ['pencil_skirt', 'pencil_skirt', 'new'],
    "Scarves" : ["scarf", "scarf", 'new'],
    "Tablet Cases & Skins" : ['tablet', 'tablet', 'new'],
    "Drawstring Bags" : ['drawstring_bag', 'drawstring_bag', 'new'],
    "Spiral Notebooks" : ['spiral_notebook', 'spiral_notebook', 'new'],
    "Hardcover Journals" : ['hardcover_journal', 'hardcover_journal', 'new'],
    "Cloks" : ["clock", 'clock', 'old'],
    "Art Board Prints" : ['gallery_board', 'gallery_board', 'new'],
    "Acrylic Blocks & Coasters" : ['acrylic_block', 'acrylic_block', 'new'],
    "Throw Blankets & Tapestries" : ['tapestry', 'tapestry', 'new'],
    "Bath Mats" : ['bath_mat', 'bath_mat', 'new'],
    "Water Bottles" : ['water_bottle', 'water_bottle', 'new'],
    "Wood & Canvas Mounted Prints" : ['mounted_print', 'mounted_print', 'new'],
    "Cotton Tote Bags" : ['cotton_tote_bag', 'cotton_tote_bag', 'new'],
    "Pin Buttons" : ['pin_button', 'pin_button', 'new'],
    "Masks" : ['mask', 'mask', 'new'],
    "Aprons" : ['apron', 'apron', 'new'],
    "Jigsaw Puzzles" : ['jigsaw_puzzle', 'jigsaw_puzzle', 'new'],
    "Sleeveless Tops" : ['panel_tank', 'panel_tank', 'new'],
    "Floor Pillows" : ['floor_pillow', 'floor_pillow', 'new'],
    "Phone Wallets" : ['phone_wallet', 'phone_wallet', 'new'],
    "Leggings" : ['leggings', 'leggings', 'new'],
    "Socks" : ['socks', 'socks', 'new'],
    "Backpacks" : ['backpack', 'backpack', 'new'],
    "Duffle Bags" : ['duffle_bag', 'duffle_bag', 'new'],
    "Fitted Masks" : ['fitted_mask', 'fitted_mask', 'new']
}

def rep(text, button):
    return button.replace("@REPLACE", text)

for each in products:
    products[each][0] = rep(products[each][0], editButton)
    if products[each][2] == 'old':
        upload = oldUpload
    elif products[each][2] == 'new':
        upload = newUpload

    products[each][1] = rep(products[each][1], upload)

site = {
    "redbubble" : "https://www.redbubble.com",
    "homepage1" : "https://www.redbubble.com/explore/for-you/",
    "homepage2" : "https://www.redbubble.com/explore/for-you/#",
    "login" : "https://www.redbubble.com/auth/login",
    "portfolio" : "https://www.redbubble.com/portfolio/manage_works?ref=account-nav-dropdown",
    "settings" : "/html[1]/body[1]/div[1]/div[4]/div[2]/section[1]/div[6]/div[1]/div[1]/div[1]",
    "copySettings" : "/html[1]/body[1]/div[1]/div[4]/div[2]/section[1]/div[6]/div[1]/div[1]/div[2]/a[3]",
    "title" : "/html[1]/body[1]/div[1]/div[5]/div[2]/form[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]",
    "tags" : "/html[1]/body[1]/div[1]/div[5]/div[2]/form[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/textarea[1]",
    "desc" : "/html[1]/body[1]/div[1]/div[5]/div[2]/form[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/textarea[1]",
    "replaceImage" : "/html[1]/body[1]/div[1]/div[5]/div[2]/form[1]/div[1]/div[1]/div[3]/input[1]",
    "openColor" : "/html[1]/body[1]/div[1]/div[5]/div[2]/form[1]/div[1]/div[1]/div[4]/div[1]",
    "sendColor" : "/html[1]/body[1]/div[41]/div[2]/div[2]/input[1]",
    "rights" : "/html[1]/body[1]/div[1]/div[5]/div[2]/form[1]/section[2]/div[3]/input[1]",
    "saveWork" : "/html[1]/body[1]/div[1]/div[5]/div[2]/form[1]/section[2]/div[4]/div[1]/input[1]"
}


pinData = {
    "pinterest_home" : "https://www.pinterest.com/",
    "pre_login_button" : ('//*[@id="__PWS_ROOT__"]/div[1]/div/div/div/div[1]/div[1]/div[2]/div[2]/button'),
    "login_button" : "//button[@type='submit']",
    "pin_builder" : "https://www.pinterest.com/pin-builder/",
    "pin_name" : "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/textarea[1]",
    "pin_description" : "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]",
    "image_input" : "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]",
    "pin_link" : "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/textarea[1]",
    "drop_down_menu" : "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/button[1]",
    "section_not_defined" : "//div[@class='Jea jzS zI7 iyn Hsu zmN']//div[@class='Jea Pyg Umk X6t gjz hDW lnZ qJc s2n wsz zI7 iyn Hsu']",
    "publish_button" : "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/button[2]",
    "new_pin" : "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[1]/div[1]/button[1]",
    "return_pin_builder" : "//*[starts-with(@class, 'JJV MIw Rym QLY p6V ojN Cii kOw Smz')]",
}
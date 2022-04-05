import os
from pathlib import Path
os.chdir(Path(__file__).parents[0])

import functions.gui as gui
import functions.redbubbleCopyWork as rcw

driver = rcw.bot("", "")

gui.work(driver=driver)

try:
    driver.quit()
except:
    pass

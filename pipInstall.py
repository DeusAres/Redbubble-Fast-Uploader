import subprocess

requirements  = [
    'PySimpleGUI',
    'selenium',
    'webdriver-manager'
    'Pillow'
    'numpy'
]

for each in requirements:
    subprocess.run(f'pip install {each} --upgrade', shell=True)
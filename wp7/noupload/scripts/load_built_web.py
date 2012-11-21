import os

BUILD_DIR = r'..\build_web'
MAIN_DIR = r'..\..\\'

for fn in os.listdir(BUILD_DIR):
    if fn.endswith(".html"):
        


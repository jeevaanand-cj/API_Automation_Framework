from allure_combine import combine_allure
import os

source = ''
des = ''
# 1) Create complete.html in allure-generated folder
combine_allure(source)

# 2) Create complete.html in specified folder
combine_allure(source, dest_folder=des)

# 3) Make sure that dest folder exists, create if not
combine_allure(
    source,
    dest_folder=des,
    auto_create_folders=True
)
# 4) Remove sinon.js and server.js from allure folder after complete.html is generated:
combine_allure(
    source,
    remove_temp_files=True
)
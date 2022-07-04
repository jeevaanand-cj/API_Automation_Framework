#!/bin/bash
cd ..
python3.9 -m pytest -s -v ${PWD}/TestCases/apirequesttest/test_DocsperaEHR.py --html=HtmlReport/DocsperaEHR_Report.html --self-contained-html --capture=sys --show-capture=log --alluredir=Reports/DocsperaEHR
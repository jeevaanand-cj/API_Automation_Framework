cd ..
echo %cd%
python3 -m pytest -s -v %cd%\TestCases\apirequesttest\test_DocsperaEHR.py --html=HtmlReport/DocsperaEHR_Report.html --self-contained-html --capture=sys --show-capture=log --alluredir=Reports/DocsperaEHR
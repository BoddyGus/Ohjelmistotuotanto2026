*** Settings ***
Library  Browser

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      500ms
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${BROWSER}    chromium
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $HEADLESS == 'true'
        New Browser  browser=${BROWSER}  headless=True
    ELSE
        New Browser  browser=${BROWSER}  headless=False  slowMo=${DELAY}
    END
    New Context
    New Page  about:blank

Add Test Reference
    [Arguments]  ${key}  ${title}
    Go To  ${HOME_URL}/new_reference
    Fill Text  [name="citation_key"]  ${key}
    Select Options By  [name="type"]  value  book
    Fill Text  [name="author"]  Test Author
    Fill Text  [name="title"]  ${title}
    Fill Text  [name="year"]  2026
    Click  button >> text=Add reference
    Get Text  body  *=  Reference added successfully.

Reset References
    Go To  ${RESET_URL}

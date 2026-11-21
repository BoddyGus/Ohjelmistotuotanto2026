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

Reference details can be opened
    Go To  ${HOME_URL}/new_reference
    Fill Text  [name="citation_key"]  detail1
    Fill Text  [name="type"]  book
    Fill Text  [name="author"]  Ada Lovelace
    Fill Text  [name="title"]  Notes
    Fill Text  [name="year"]  1843
    Fill Text  [name="publication"]  Publisher
    Click  button >> text=Add reference
    Click  text=detail1
    Get Text  body  *=  Ada Lovelace
    Get Text  body  *=  Notes
    Get Text  body  *=  1843

Unknown reference displays not-found message
    Go To  ${HOME_URL}/references/999999
    Get Text  body  *=  Reference not found

Reset References
    Go To  ${RESET_URL}

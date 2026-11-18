*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset References

*** Test Cases ***
Homepage shows reference application
    Go To  ${HOME_URL}
    Get Title  ==  Pooki - References
    Get Text  body  *=  No references have been added.

User can open add reference page
    Go To  ${HOME_URL}
    Click  text=Add a new reference
    Get Text  body  *=  Add a new reference
    Get Element States  [name="citation_key"]  contains  visible
    Get Element States  [name="author"]  contains  visible
    Get Element States  [name="title"]  contains  visible
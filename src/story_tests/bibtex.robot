*** Settings ***
Resource  resource.robot
Library  OperatingSystem
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset References

*** Test Cases ***
User can download BibTex file
    Go To  ${HOME_URL}/new_reference
    Fill Text  [name="citation_key"]  download-test
    Select Options By  [name="type"]  value  book
    Fill Text  [name="author"]  Test Author
    Fill Text  [name="title"]  Test Book
    Fill Text  [name="year"]  2026
    Fill Text  [name="publication"]  Test Publisher
    Click  button >> text=Add reference

    Go To  ${HOME_URL}
    ${download_promise}=  Promise To Wait For Download  saveAs=${OUTPUT DIR}${/}references.bib
    Click  text=Export references as BibTeX
    Wait For  ${download_promise}

    File Should Exist  ${OUTPUT DIR}${/}references.bib
    ${bib}=  Get File  ${OUTPUT DIR}${/}references.bib
    Should Contain  ${bib}  @book{download-test,
    Should Contain  ${bib}  author = {Test Author}
    Should Contain  ${bib}  title = {Test Book}
    Should Contain  ${bib}  publisher = {Test Publisher}
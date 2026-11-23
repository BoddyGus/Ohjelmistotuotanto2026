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

User can cancel adding a reference
    Go To  ${HOME_URL}
    Click  text=Add a new reference
    Fill Text  [name="citation_key"]  cancel-test
    Select Options By  [name="type"]  value  book
    Fill Text  [name="author"]  Test Author
    Fill Text  [name="title"]  Test Title
    Fill Text  [name="year"]  2026
    Click  text=Cancel
    Get Title  ==  Pooki - References
    Get Text  body  *=  No references have been added.
    Get Text  body  not contains  cancel-test


User can open reference details from the list
    Go To  ${HOME_URL}/new_reference
    Fill Text  [name="citation_key"]  detail1
    Select Options By  [name="type"]  value  book
    Fill Text  [name="author"]  Ada Lovelace
    Fill Text  [name="title"]  Notes
    Fill Text  [name="year"]  1843
    Fill Text  [name="publication"]  Publisher
    Click  button >> text=Add reference
    Get Text  body  *=  Reference added successfully.
    Click  text=detail1
    Get Text  h1  ==  Reference details
    Get Text  body  *=  detail1
    Get Text  body  *=  book
    Get Text  body  *=  Ada Lovelace
    Get Text  body  *=  Notes
    Get Text  body  *=  1843
    Get Text  body  *=  Publisher

User can return from reference details to the list
    Go To  ${HOME_URL}/new_reference
    Fill Text  [name="citation_key"]  detail2
    Select Options By  [name="type"]  value  book
    Fill Text  [name="author"]  Grace Hopper
    Fill Text  [name="title"]  Compilers
    Fill Text  [name="year"]  1952
    Click  button >> text=Add reference
    Click  text=detail2
    Click  text=Back to reference list
    Get Title  ==  Pooki - References
    Get Text  body  *=  detail2

User can edit an existing reference including its citation key
    Go To  ${HOME_URL}/new_reference
    Fill Text  [name="citation_key"]  before-edit
    Select Options By  [name="type"]  value  book
    Fill Text  [name="author"]  Original Author
    Fill Text  [name="title"]  Original Title
    Fill Text  [name="year"]  2020
    Fill Text  [name="publication"]  Original Publisher
    Click  button >> text=Add reference
    Click  text=before-edit
    Click  text=Edit reference
    Get Text  h1  ==  Edit reference
    Get Property  [name="citation_key"]  value  ==  before-edit
    Fill Text  [name="citation_key"]  after-edit
    Fill Text  [name="title"]  Updated Title
    Click  button >> text=Save changes
    Get Text  body  *=  after-edit
    Get Text  body  *=  Updated Title
    Get Text  body  *=  Reference updated successfully.

Unknown reference shows not found message
    Go To  ${HOME_URL}/references/999999
    Get Text  body  *=  Reference not found
    Click  text=Back to reference list
    Get Title  ==  Pooki - References

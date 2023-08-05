# Description
This module will allow you to quickly create interesting and user-friendly menus for console applications!

ATTENTION: Required keyboard module

# Code example
```python
from MenuCreator import CreateMenu

Menu = CreateMenu(title="Example Menu", elements=[  
    'First element',  
    'Second element',  
    'Third element'  
])

Menu.load_menu()  
Menu.wait()

if Menu.get_selected_item() == 0:
    print("Selected first element!")
    
elif Menu.get_selected_item() == 1:
    print("Selected second element!")

else:
    pass

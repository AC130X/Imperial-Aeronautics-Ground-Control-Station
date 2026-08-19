#importing lib
from nicegui import ui 
import sys


sys.path.append(r'C:\Users\Vaibhav\Desktop\Files\IA-GCS\Tab Functions')

#importing functions for each tab

import PFD                              # type: ignore
import MissionSetup                     # type: ignore
import DataReview                       # type: ignore
import SettingsHelp                     # type: ignore
import SITL                             # type: ignore
import vehiclesetup                     # type: ignore

#ui.query('body').classes('overflow-hidden') #uncomment to remove scroll bar

#defining tabs
with ui.tabs().classes('w-full') as tabs:
    PFD_tab = ui.tab('Primary Flight Display')
    Mission_Setup_tab = ui.tab('Autonomous Mission Setup')
    Data_Review_tab = ui.tab('Flight Data Review')
    Vehicle_Setup_tab = ui.tab('Vehicle Setup')
    SITL_tab = ui.tab('SITL')
    Settings_Help_tab = ui.tab('Settings and Help')

#assigning functions to tab
with ui.tab_panels(tabs, value=PFD_tab).classes('w-full'):#add h-full for removing scroll bar
    
    with ui.tab_panel(PFD_tab):
        PFD.render()
        
    with ui.tab_panel(Mission_Setup_tab):
        MissionSetup.render()
    
    with ui.tab_panel(Data_Review_tab):
        DataReview.render()
    
    with ui.tab_panel(Vehicle_Setup_tab):
        vehiclesetup.render()
    
    with ui.tab_panel(SITL_tab):
        SITL.render()

    with ui.tab_panel(Settings_Help_tab):
        SettingsHelp.render()

#running ui 
ui.run(native=True, title="Imperial Aeronautics Ground Control Station by Vaibhav Rajesh", window_size=(1920, 1080))
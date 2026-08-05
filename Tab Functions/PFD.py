from nicegui import ui

def render():
    with ui.grid(columns=2).classes('w-full h-[90vh] gap-4 grid-rows-[2fr_1fr]'):
        
        # TOP LEFT 
        with ui.card().classes('h-full flex flex-col justify-center items-center'):
            ui.label('Attitude Indicator').classes('text-xl font-bold')
            
        # TOP RIGHT 
        with ui.card().classes('h-full flex flex-col justify-center items-center bg-blue-50'):
            ui.label('Map View').classes('text-xl font-bold')
            
        # BOTTOM 
        with ui.card().classes('col-span-2 h-full w-full p-6'):
            
            # Master Grid inside the card: Splits the card 50/50
            with ui.grid(columns=2).classes('w-full h-full gap-8'):
                
                with ui.column().classes('w-full justify-center'):
                    ui.label('System Data').classes('text-lg font-bold mb-2')
                    
                    # The nested grid for your labels
                    with ui.grid(columns=2).classes('w-full gap-4'):
                        with ui.column().classes(' p-2 rounded'):
                            ui.label('Battery Voltage')
                            ui.label('Elapsed Time: 00:00:00')
                        with ui.column().classes(' p-2 rounded'):
                            ui.label('Flight Mode:')
                            ui.label('Mission Status')
                        with ui.column().classes(' p-2 rounded'):
                            ui.label('Preflight Status: Done')
                            ui.label('Arm Status: DISARMED')
                        with ui.column().classes(' p-2 rounded'):
                            ui.label('GPS Status:')
                            ui.label('Connection Status: ')


                with ui.column().classes('w-full border-l-2 pl-8 justify-center'):
                    ui.label('System Controls').classes('text-lg font-bold mb-2')
                    
                    # A row for the dropdown and a button
                    with ui.row().classes('items-center gap-4 w-full'):
                        ui.select(['Auto', 'Manual', 'Diagnostic'], value='Auto', label='Flight Mode').classes('w-48')
                        ui.button('Set Mode', color='primary').classes('mt-4') # mt-4 aligns button with the select input
                    
                    # A row for action buttons
                    with ui.row().classes('items-center gap-4 mt-4'):
                        ui.button('Calibrate Sensors', color='secondary')
                        ui.button('Emergency Stop', color='red')

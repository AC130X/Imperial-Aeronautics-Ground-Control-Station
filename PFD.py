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
                
                # --------------------------------------------------
                # LEFT HALF: The Data Labels (Option 2 Grid)
                # --------------------------------------------------
                with ui.column().classes('w-full justify-center'):
                    ui.label('System Data').classes('text-lg font-bold mb-2')
                    
                    # The nested grid for your labels
                    with ui.grid(columns=2).classes('w-full gap-4'):
                        with ui.column().classes('bg-blue-50 p-2 rounded'):
                            ui.label('Grid Col 1').classes('font-bold text-sm')
                            ui.label('Speed: 100')
                        with ui.column().classes('bg-green-50 p-2 rounded'):
                            ui.label('Grid Col 2').classes('font-bold text-sm')
                            ui.label('Fuel: 80%')
                        with ui.column().classes('bg-red-50 p-2 rounded'):
                            ui.label('Grid Col 3').classes('font-bold text-sm')
                            ui.label('Errors: 0')
                        with ui.column().classes('bg-yellow-50 p-2 rounded'):
                            ui.label('Grid Col 4').classes('font-bold text-sm')
                            ui.label('Ping: 12ms')

                # --------------------------------------------------
                # RIGHT HALF: Buttons and Dropdowns
                # --------------------------------------------------
                # 'border-l-2' adds a vertical line, 'pl-8' adds padding so text doesn't touch the line
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

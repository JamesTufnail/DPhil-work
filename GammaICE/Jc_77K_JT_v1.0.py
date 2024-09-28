from dash import Dash, html, dash_table, dcc, callback, Output, Input, ALL
import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
import pyvisa
from datetime import datetime
import pathlib
import os

port = 8082

# Initialise
app = Dash(__name__) # Dash constructor - creates a new Dash application
pio.templates.default = 'plotly_white' # Setting the default template for the plots

######## Define the initial variables ##############
V_lim = 3e-4                                # voltage limit [V]
I_start = 0.50                              # starting current [A]
I_target = 10.0                             # target current [A]
slew_rate = 0.1                             # slew rate [A/s]
sampling_rate_on = 0.001                    # minimum time between samples (when current is on). One measurement every 0.001 s, best performance with python only is 3.5e-6     
sampling_rate_off = 0.001  
running_time = ((I_target - I_start) / slew_rate) / 60 # running time [m]

sample_name = 'test'                        # sample name
path = 'C:/Users/.../data'                   # save path
save = 'yes'                                # save data
app_mode = 'Simulation'                    # app mode

# Section 1 - setting the profile variables
section1 = html.Div([
    html.Hr(),
    html.Div('Profile Settings', style={'textAlign': 'center', 'fontSize': 20}),
    dash_table.DataTable(
        id='profile_settings',
        columns=[
            {'name': 'Save', 'id': 'save', 'presentation': 'dropdown'},
            {'name': 'App Mode', 'id': 'app_mode', 'presentation': 'dropdown'},
            {"name":"Voltage Limit (V)", "id": "V_lim"},
            {"name":"Sample Name", "id":"sample_name"},
            {"name":"Save Path", "id":"path"},
            {"name":"Current-on Sampling Rate (Hz)", "id":"sampling_rate_on"},
            {"name":"Current-off Sampling Rate (Hz)","id":"sampling_rate_off"}
        ],
        data=[
            {
                'save': save, 
                'app_mode': app_mode, 
                'V_lim': V_lim,
                'sample_name': sample_name, 
                'path': path, 
                'sampling_rate_on': sampling_rate_on, 
                'sampling_rate_off': sampling_rate_off
            }
        ],
        editable=True,
        dropdown={
            'save': {'options': [{'label': i, 'value': i} for i in ['yes', 'no']]},
            'app_mode': {'options': [{'label': i, 'value': i} for i in ['Simulation', 'Real Data']]}
        }
    ),
])

# Section 2 - setting the measurement settings
section2 = html.Div([
    html.Div(className='row', children=[
        html.Div('Measurement Settings', style={'textAlign': 'center', 'fontSize': 20}),
        dash_table.DataTable(
            id='measurement_settings',
            columns=[
                {"name": 'Starting Current (A)', "id": "I_start"},
                {'name': 'Target Current (A)', 'id': 'I_target'},
                {'name': 'Slew Rate (A/s)', 'id': 'slew_rate'},
                {'name': 'Running Time (min)', 'id': 'running_time'}
            ],
            data=[{
                'I_start': I_start,
                'I_target': I_target,
                'slew_rate': slew_rate,
                'running_time': np.round(running_time, 2)
            }],
            editable=True
        ),
    ], style={'width': '40%', 'display': 'inline-block'}),
])


# Section 3 - connecting to the instruments
# create disctionary of instruments
instruments = {
    "keysight":{"name":"Keysight N697A", "address": "USB0::0x0957::0x3307::MY59160232::INSTR", "method":"Resource_Manager"}, # power supply
    "keithley":{"name":"Keithley DMM6500", "address": "USB0::0x05E6::0x6500::04497374::INSTR","method":"Resource_Manager"}, # voltmeter
}

instrument_objects = [] # list of instrument objects
for value in list(instruments.keys()):
    instrument_objects.append(html.Div(children=instruments[value]['name'], id=f"{value}_connection"))
    instrument_objects.append(dcc.Input(id = {'id': f"{value}_address", 'type':'equipment'}, value=instruments[value]['address']))
    instrument_objects.append(html.Div(id = f'{value}_status', children = ["Not Connected"]))
    # print(instrument_objects)

instrument_objects = html.Div(
    instrument_objects,
    style = {"columns": f'300px {str(len(instruments))}', "margin":"10px"},
)

section3 = html.Div([
    html.Div(className='row', children=[
        html.Div('Instrument Settings',
                  style={'textAlign': 'left', 'fontSize': 20}),
        html.Div([
            html.Button('Check Instruments Connected', id='inst_check', n_clicks=0,
            style = {'Position': 'right'})
        ]),
        # html.Br(),
        instrument_objects
    ]),
],
style={"width": "50%", "display": "inline-block"}
    )



# Section 4 -- Run the Experiment
Section4 = html.Div([
    html.H2("Run the Experiment", style={"textAlign": "center"}),
    html.Div("Save Status"),
    html.Div(id="save_text"),
    html.Div("Plot Settings"),
    dcc.Interval(id="interval-component", interval=1*1000, n_clicks=0),
    html.Div([
        html.Div([
            html.Label("Refresh every (s)", style={"margin": "10px"}),
            dcc.Slider(0, 4, marks={0: "1", 1: "2", 2: "5", 3: "13", 4: "30"}, tooltip={"placement": "bottom", "always_visible": False}, value=0, id="Interval_user")
        ]),
        html.Div([
            html.Div([
                html.Label("File Prefix", style={"margin": "10px"}),
                dcc.Input(id="file_prefix", value='I_V_77K_trace', style={"width": "100%"})
            ], style={"columns": "10px 2"})
        ]),
        html.Div([
            html.Button("Start", id="start_button", n_clicks=0, style={"width": "75px", "height": "0px", "margin": "10px", "border": "20px solid transparent", "border-right": "0px", "border-left": "20px solid lightgreen", "background-color": "white", "color": "darkgreen", "border-radius": "5px"}),
            html.Button("Stop", id="stop_button", n_clicks=0, style={"background-color": "red", "color": "black", "width": "50px", "height": "50px", "border-radius": "50%", "margin": "10px"}),
            html.Button("Clear", id="Clear_button", n_clicks=0, style={"margin": "10px", "height": "50px"}),
            html.Div(id="Status_Message", children="Initiation")
        ])
    ], style={"columns": "10px 4"}),
    html.Div([
        html.Div([
            dcc.Dropdown(id="Y-Axis", options=["Set Current [A]", "Measured Current [A]", "Keithley Voltage [V]", "PSU Voltage [V]"], value="Keithley Voltage [V]", style={"min-width": "400px"}),
            dcc.Graph(id="live-figure")
        ], style={"display": "flex", "flex-direction": "column"}),
        dcc.Graph(id="V_vs_I_graph"),
        dcc.Graph(id="temp_graph")
    ], style={"display": "flex", "flex-direction": "row", "justify-content": "space-around"})
])



app.layout = html.Div([
    html.H1('Jc(77K) Measurement', style={'textAlign': 'center'}),
    section1,
    html.Br(),
    section2,
    html.Br(),
    section3,
    html.Br(),
    Section4
    ])

# Callbacks
@callback(
        Output("instrument_list","children"),
        Input("inst_check","n_clicks")
        )

def inst_check(click):
    """ Function checks whether instruments are connected or not"""
    rm = pyvisa.ResourceManager()
    insts = list(rm.list_resources())
    text = ""
    for inst in insts:
        text = text + inst + "<>"
    return text


@callback(
        Output("save_text", "children"),
        Input("profile_settings", "data")
        )

def set_save_text(profile_settings):
    """
    Function to save save text - saying whether data is saved or not
    DOESN'T ACTUALLY SAVE DATA ITSELF
    
    Args:
    profile_settings: dict, profile settings
    
    Returns:
    save_statement: str, statement about saving
    """
    if profile_settings[0]["save"] == "Yes":
        try:
            sample_name = profile_settings[0]["sample_name"]
            date = datetime.now().strftime("%Y%m%d_")           #date for file names
            datet = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")   #date and time for file names

            new_dir_name = str(date) + str(sample_name)
            new_dir = pathlib.Path(profile_settings[0]["path"], new_dir_name)
            new_dir.mkdir(parents=True, exist_ok=True)
            new_file = new_dir / ('I_77K_V_Curve_' + str(datet) + '.csv')
            save_statement = "The results will be saved to " + str(new_dir) +  '\I_77K_V_Curve_' + str(datet)
        except:
            save_statement = "Please check your file path, unable to create a folder."
    else:
        save_statement = "The results will not be saved"
    return save_statement


@callback(
    Output("live-figure", "figure"),
    Output("temp_graph","figure"),
    Output("V_vs_I_graph","figure"),
    Output("Status_Message","children"),
    Input("start_button", "n_clicks"),
    Input("profile_settings","data"),
    Input("profile_stages","data"),
    Input({"type":"equipment_address", "id":ALL}, "value"),
    Input('interval-component', 'n_intervals'),
    Input("Y-Axis","value"),
    Input("Interval_user","value")
    )

def run_measurement(start, profile_settings, profile_stages, instrument_addresses, n , yaxis1, interval_user):
    button_id = ctx.triggered_id

    if button_id == 'start_button':
        hard_stop.append("Go")

         # connect to the instruments
        def equipment_object(object):
            connections = {}
            rm = pyvisa.ResourceManager()
            for instrument in object:
                address = instrument[instrument]["address"]
                if instrument[instrument]["method"] == "Resource_Manager":
                    try:
                        connections[instrument] = rm.open_resource(address)
                    except:
                        connections[instrument] = "Not Connected"
                else:
                    connections[instrument] = "Not Connected"
            return connections
             
                 
                







# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)


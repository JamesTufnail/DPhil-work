
port = 8082
debug = False
# import required modules
from datetime import datetime    
import pathlib
import pyvisa
import easy_scpi as scpi
import time
import plotly.io as pio
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px
import easygui
from scipy import stats
from dash import Dash, html, dash_table, dcc, callback, Input, Output, ctx, ALL
import os

# define plotly template
pio.templates["josh_template"] = pio.templates["simple_white"]
pio.templates.default = "josh_template"
josh_template = pio.templates["josh_template"].layout.update({"yaxis":{"mirror":True,"ticks":"inside"},"xaxis":{"mirror":"all","ticks":"inside"}})


#---VARIABLES--------------------------------------------------------------------------------------
V_lim = 3e-4                                #voltage limit [V]
I_start = 0.50                              #starting current [A]
sampling_rate_on = 0.025                   # minimum time between samples (when current is on). One measurement every 0.001 s, best performance with python only is 3.5e-6     
sampling_rate_off = 0.025                     # minimum time between samples (when current is off) One measurment every 0.01 s

target_1 = 1.04                             #target current 1 [A]
dwell_1 = 1                             #dwell time at target current 1 [s]
increment_1 = 0.18                          #current step size [A] up to target current 1
step_gap_1 = 0.5                            #time between steps [s]
pulse_length_1 = 0.13                       #length of each pulse [s]

target_2 = 3.63                           #target current 2 [A]
dwell_2 = 1                         #dwell time at target current 2 [s]
increment_2 = .18                          #current step size [A] up to target current 2
step_gap_2 = .5                            #time between steps [s]
pulse_length_2 = 0.13                      #length of each pulse [s]

target_3 = 5.22                             #target current 3 [A]
dwell_3 = 1                              #dwell time at target current 3 [s]
increment_3 = 0.0475              #current step size [A] up to target current 3
step_gap_3 = .5                           #time between steps [s]
pulse_length_3 = 0.13                       #length of each pulse [s]

save_it = "Yes"                             # whether to save or not     
sample_name = "Kirk_"                         #sample name for exported files
path = "C:/Users/cfas/Desktop/Data Logging Files/"                       # path location to save the file to

# keithley,lakeshore,keysight = Instrument_Connection()


stages = {}
stages["1"]={"target":target_1, "dwell":dwell_1, "increment":increment_1, "step_gap":step_gap_1, "pulse_length":pulse_length_1}
stages["2"]={"target":target_2, "dwell":dwell_2, "increment":increment_2, "step_gap":step_gap_2, "pulse_length":pulse_length_2}
stages["3"]={"target":target_3, "dwell":dwell_3, "increment":increment_3, "step_gap":step_gap_3, "pulse_length":pulse_length_3}

profile_dict = []
for i,stage in enumerate(list(stages.keys())):
    profile_dict.append({"stage":stage})
    for key in list(stages[stage].keys()):
        profile_dict[i][key] = stages[stage][key]


log_1 = [] #initiate the logging variable
hard_stop = ["Go"]#initiate the hard-stop condition

# Section 1 -- Measurement Settings
Section1 = html.Div([html.Div("Measurement Settings"),
    dash_table.DataTable(id = "profile_settings", 
        columns = 
        [{"name":"save","id":"save_it","presentation":"dropdown"},
        {"name":"App Mode","id":"mode", "presentation":"dropdown"},
        {"name":"Voltage Limit", "id": "V_lim"},
        {"name":"Starting Current", "id":"I_start"},
        {"name":"Sample Name", "id":"sample_name"},
        {"name":"Save Path", "id":"path"},
        {"name":"Current On Sample Rate", "id":"sampling_rate_on"},
        {"name":"Current Off Sample Rate","id":"sampling_rate_off"}
    ],
    data =[{"save_it": save_it, "mode":"Real Data","V_lim":V_lim, "I_start":I_start,
        "sample_name":sample_name, "path":path,
        "sampling_rate_on":sampling_rate_on, "sampling_rate_off":sampling_rate_off }
    ],
    editable = True,
    dropdown = {"save_it": {"options":[{"label":i, "value":i} for i in ["No", "Yes"]]},"mode": {"options":[{"label":i, "value":i} for i in ["Simulation", "Real Data"]]}
    })
],style = {"display":"flex", "flex-direction":"column", "align-items":"center"})

# Section 2 profile settings
Section2 = html.Div([
    html.Div([
        html.Div([
            html.Div("Profile Settings"),
            dash_table.DataTable(
                id='profile_stages',
                columns=[{"name":"stage","id":"stage"},
                {"name":"target","id":"target"},
                {"name":"dwell","id":"dwell"},
                {"name":"increment","id":"increment"},
                {"name":"step_gap","id":"step_gap"},
                {"name":"pulse_length","id":"pulse_length"}], data = profile_dict , editable = True,
            )
        ]),
        dcc.Graph(id = "profile_figure")
    ],style = {"display":"flex", "align-items":"center","justify-content":"space-evenly" })
])


# Section 3:  Instrument Connection
instruments = {
    "keysight":{"name":"Keysight N697A", "address":"USB0::0x0957::0x3307::MY59160232::INSTR", "method":"Resource_Manager"},
    "keithley":{"name":"Keithley DMM6500", "address":"USB0::0x05E6::0x6500::04497374::INSTR","method":"Resource_Manager"},
    "lakeshore":{"name":"Lakeshore 325", "address":"GPIB0::12::INSTR", "method":"Resource_Manager"}
}

instrument_objects = []
for instrument in list(instruments.keys()):
    instrument_objects.append(html.Div(children = instruments[instrument]["name"], id = instrument+"_name"))
    instrument_objects.append(dcc.Input(id = {"id": instrument +"_address", "type":"equipment_address"}, value = instruments[instrument]["address"]))
    instrument_objects.append(html.Div(id = instrument + "_status", children = ["initial"]))

instrument_objects = html.Div(
    instrument_objects,
    style = {"columns":"300px "+str(len(instruments)),"margin":"10px"}
)


Section3 = html.Div([
    html.H2("Instrument Connection"),
    html.Div([
        html.Button('Check Instruments Connected', id='inst_check', n_clicks=0),
        html.Div(id = "instrument_list",children = "none")],style = {"columns":"100px 4","margin":"10px"}),
        html.Br(),
        instrument_objects
        ])

# Section 4 -- Run the Experiment
Section4 = html.Div([html.H2("Run the Experiment"),
    html.Div("Save Status"),
    html.Div(id = "save_text"),
    html.Div("Plot Settings"),
    dcc.Interval(id = "interval-component", interval = 1*1000, n_intervals = None),
    html.Div([
        html.Div([
            html.Label("Refresh every (s)", style = {"margin":"10px 10px 10px 10px"}),
            dcc.Slider(0,4,marks = {0:"1", 1:"2", 2:"5", 3:"13", 4:"30"},tooltip={"placement": "bottom", "always_visible": False},value =0, id = "Interval_user")
        ]),
        html.Div([
            html.Div([
                html.Label("File Prefix", style = {"margin":"10px 10px 10px 10px"}),
                dcc.Input(id = "file_prefix", value = 'Pulsed_IV_', style = {"width":"100%"}),
            ],style = {"columns" : "10px 2"})
        ]),
        html.Div([
            html.Button("Start", id = "start_button", n_clicks = 0, style = {"width":"75px", "height":"0px","margin":"10px 10px 10px 10px", "border":"20px solid transparent","border-right":"0px","border-left":"20px solid lightgreen", "background-color":"white","color":"darkgreen","border-radius":"5px"}),
            html.Button("Stop", id = "stop_button", n_clicks = 0,style = {"background-color":"red", "color":"black","width":"50px", "height":"50px", "border-radius":"50%","margin":"10px 10px 10px 10px"}),
            html.Button("Clear", id = "Clear_button", n_clicks = 0,style = {"margin":"10px 10px 10px 10px", "height":"50px"}),
            html.Div(id = "Status_Message", children = "Initiation")
        ])
    ], style = {"columns":"10px 4"}),
    # html.Div(children = [html.Div(id = "stop_times"), html.Div(id = "clear_times")]),
    # html.Button("Stop", id = "stop_button", n_clicks = 0)
    html.Div([
        html.Div([
            dcc.Dropdown(id = "Y-Axis", options = ["Set Current [A]","Measured Current [A]", "Keithley Voltage [V]","PSU Voltage [V]"], value = "Keithley Voltage [V]",style = {"min-width":"400px"}),
            dcc.Graph(id = "live-figure")
        ],style = {"display":"flex", "flex-direction":"column"}),
        dcc.Graph(id = "V_vs_I_graph"),
        dcc.Graph(id = "temp_graph")
    ],style = {"display":"flex", "flex-direction":"row", "justify-content":"space-around"})])



#Section 5 Analysis of a file
Section5 = html.Div([html.H2("Analysis"),
    html.Div("Choose a File to Analyze"),
    html.Button("Refresh Files", id = "refresh_button",n_clicks = 0),
    dcc.Dropdown(id = "file_dropdown"),
    html.Div([dcc.Graph(id = "linearized_figure"),
    dcc.Graph(id = "full_figure")],style = {"display":"flex", "flex-direction":"row"}),
    html.Div(id = "ideal_message"),
     html.Div(id = "Ic_and_n_message")])
# time_start = time.perf_counter_ns()
app = Dash(__name__, title = "Pulsed_IV")

app.layout = html.Div([
    html.H1("Pulsed_IV Logger",style = {"textAlign":"center"}),
    Section1,
    Section2,
    Section3,
    Section4,
    Section5    
    ])

@callback(Output("linearized_figure", "figure"),Output("full_figure", "figure"),Output("ideal_message","children"),Output("Ic_and_n_message","children"),Input("profile_settings", "data"), Input("save_text", "children"), Input("file_dropdown", "value"))

def analyze_extract(profile_settings, save_text, file_name):
    file_path = save_text[save_text.find("C:"):save_text.find("\\",save_text.find("\\",len("The results will be saved to "+profile_settings[0]["path"])))+1] + file_name
    analysis = pd.read_csv(file_path)
    l = 1 #length = 0.2 cm
    analysis["Voltage"] = analysis["Keithley Voltage [V]"].copy()
    # analysis[" Keithley Voltage [V]"] = analysis["Keithley Voltage [V]"].copy()
    # analysis[" Measured Current [A]"] = analysis["Measured Current [A]"].copy()
    dt_on = analysis[analysis["Current ON"] == 1]

    noise_floor = 3*np.std(dt_on.copy()[dt_on.index < dt_on[analysis["Voltage"] < 0].index.max()]["Voltage"])
    if noise_floor > 1e-6*l:
        print("Warning, the voltage measurement noise floor is higher than E0*l")
    dt_on_pos = dt_on.copy()[dt_on.index > dt_on[analysis["Voltage"] < noise_floor].index.max()]
    fit_current_cutoff = dt_on.loc[dt_on[dt_on.index > dt_on[analysis["Voltage"] < noise_floor].index.max()].index.min(),"Measured Current [A]"]

    dt_on_pos["new_y"] = np.log10(dt_on_pos["Voltage"].copy()/(1e-6*l))
    dt_on_pos["new_x"] = np.log10(dt_on_pos["Measured Current [A]"].copy()/100)
    line_fit = stats.linregress(dt_on_pos["new_x"].values,dt_on_pos["new_y"].values)
    # print(line_fit.slope)
    Ic_value = 100*10**(-line_fit.intercept/line_fit.slope)
    # print(Ic_value)
    dt_on_pos["new_x"] = np.log10(dt_on_pos["Measured Current [A]"].copy()/(Ic_value))
    line_fit = stats.linregress(dt_on_pos["new_x"].values,dt_on_pos["new_y"].values)
    # print(line_fit.slope)
    # linearized_figure = go.Figure()
    # linearized_figure.add_trace(go.Scatter(x=dt_on_pos["new_x"] , y = [0 for i in dt_on_pos["new_y"]], name = "Original Data",mode = "lines"))
    # linearized_figure.add_trace(go.Scatter(x=dt_on_pos["new_x"] , y = (line_fit.intercept + line_fit.slope*dt_on_pos["new_x"]) -dt_on_pos["new_y"]  , name = "Fit",mode = "markers"))
    # print("fit stddev ",np.std((line_fit.intercept + line_fit.slope*dt_on_pos["new_x"]) -dt_on_pos["new_y"]))
    Ic_value = round(Ic_value*10**(-line_fit.intercept/line_fit.slope ),2)
    # print(Ic_value)
    Ic_range = round(line_fit.intercept_stderr*1.96,2)
    n_value = round(line_fit.slope ,4)
    n_range = round(line_fit.stderr*1.96,2)
    I_pers = round((((1e-12/(l*1e-6)))*Ic_value**n_value)**(1/(n_value-1)),2)
    ideal_message = "ideal increment for this V_lim and noise_floor is "+ str(round((Ic_value*(V_lim/l/1e-6)**(1/n_value)-Ic_value*(noise_floor/l/1e-6)**(1/n_value))/10,4))+" with a target 2 of " +str(round(0.9*Ic_value*(noise_floor/l/1e-6)**(1/n_value),4))
    Ic_and_n_message = "Ic = "+str(Ic_value)+ " +-" +  str(Ic_range) + "\n" + "    n = "+ str(n_value)+" +- "+ str(n_range)
    # print("Persistent_current ~ ",I_pers, ", I_pers/Ic= ",round(I_pers/Ic_value,3)*100,"%")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dt_on["Measured Current [A]"] ,y = np.log10(dt_on["Keithley Voltage [V]"]),mode = "markers",name = "Original Data"))
    fig.add_trace(go.Scatter(x = np.array([Ic_value,Ic_value]) ,y = np.log10(np.array([1.1*(dt_on["Keithley Voltage [V]"]).max(),max(.9*((dt_on["Keithley Voltage [V]"]).min()),1e-14)])),mode = "lines",name = "Ic"))
    fig.add_trace(go.Scatter(x = np.array([fit_current_cutoff,fit_current_cutoff]) ,y = np.log10(np.array([1.1*(dt_on["Keithley Voltage [V]"]).max(),max(.9*((dt_on["Keithley Voltage [V]"]).min()),1e-14)])),mode = "lines",name = "fit cut-off"))
    fig.add_trace(go.Scatter(y = np.log10(np.array([1e-6*l,1e-6*l])) ,x = np.array([(dt_on["Measured Current [A]"]).min(),(dt_on["Measured Current [A]"]).max()]),mode = "lines",name = "V0"))
    fig.add_trace(go.Scatter(x = dt_on["Measured Current [A]"], y = np.log10(1e-6*l*(dt_on["Measured Current [A]"]/Ic_value)**n_value) , name = "fit"))
    # fig.add_trace(go.Scatter(x = dt_on["Measured Current [A]"], y = np.log10(1e-6*l*(dt_on["Measured Current [A]"]/3)**23.33) , name = "matlab_fit"))
    fig.add_trace(go.Scatter(x = np.array([I_pers,I_pers]) ,y = np.log10(np.array([1.1*(dt_on["Keithley Voltage [V]"]).max(),max(.9*((dt_on["Keithley Voltage [V]"]).min()),1e-14)])),mode = "lines",name = "Ic_persistent"))
    linearized_figure = fig
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x = dt_on["Measured Current [A]"] ,y = dt_on["Keithley Voltage [V]"],mode = "markers",name = "Original Data"))
    fig.add_trace(go.Scatter(x = np.array([Ic_value,Ic_value]) ,y = np.array([1.1*(dt_on["Keithley Voltage [V]"]).max(),.9*((dt_on["Keithley Voltage [V]"]).min())]),mode = "lines",name = "Ic"))
    fig.add_trace(go.Scatter(x = np.array([fit_current_cutoff,fit_current_cutoff]) ,y = np.array([1.1*(dt_on["Keithley Voltage [V]"]).max(),.9*((dt_on["Keithley Voltage [V]"]).min())]),mode = "lines",name = "fit cut-off"))
    fig.add_trace(go.Scatter(y = np.array([1e-6*l,1e-6*l]) ,x = np.array([(dt_on["Measured Current [A]"]).min(),(dt_on["Measured Current [A]"]).max()]),mode = "lines",name = "V0"))
    fig.add_trace(go.Scatter(y = np.array([noise_floor,noise_floor]) ,x = np.array([(dt_on["Measured Current [A]"]).min(),(dt_on["Measured Current [A]"]).max()]),mode = "lines",name = "noise floor"))
    fig.add_trace(go.Scatter(x = dt_on["Measured Current [A]"], y = 1e-6*l*(dt_on["Measured Current [A]"]/Ic_value)**n_value , name = "fit"))
    # fig.add_trace(go.Scatter(x = dt_on["Measured Current [A]"], y = 1e-6*l*(dt_on["Measured Current [A]"]/3)**23.33 , name = "matlab_fit"))
    fig.add_trace(go.Scatter(x = np.array([I_pers,I_pers]) ,y = np.array([1.1*(dt_on["Keithley Voltage [V]"]).max(),.9*((dt_on["Keithley Voltage [V]"]).min())]),mode = "lines",name = "Ic_persistent"))
    full_fig = fig
    full_fig.update_layout({"xaxis":{"title":"Keithley Voltage [V]"}, "yaxis":{"title":"Measured Current [A]"}})
    return linearized_figure,full_fig,ideal_message,Ic_and_n_message

def stop_or_clear_button(n_stop,n_clear):
    """function for what happens when the stop or clear button is pressed"""
    trigger_id = ctx.triggered_id
    print(trigger_id)
    if trigger_id == "stop_button":
        hard_stop.append("Stop")
        original_len = len(log_1)
        log_1.append(["Stop Button", time.perf_counter_ns(),np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan])
        time.sleep(0.1)
        final_len = len(log_1)
        if (final_len - original_len) > 1:
            print("you may need to unplug an instrument from the computer to stop the measurement, your time between measurements is smaller than the time it takes to collect a measurement")
            hard_stop.append("Stop")
        updated_interval = 4 #reset interval to every 30 seconds
    elif trigger_id == "Clear_button":
        log_1.clear()
        # log_1.append(["ok", time.perf_counter_ns(),np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan])
        updated_interval = 0 #reset interval to every 1 seconds
    else:
        updated_interval = 0
    return updated_interval
app.callback(Output("Interval_user","value"),Input("stop_button", "n_clicks"),Input("Clear_button", "n_clicks"))(stop_or_clear_button)


def update_interval(value):
    """takes the interval slider value and converts it to the corresponding seconds (custom formula which matches the label for the slider)"""
    return int(round(2.34**(float(value)),0))*1000
app.callback(Output("interval-component", "interval"),Input("Interval_user","value"))(update_interval)

# @callback(Output("stop_times","children"), Input("stop_button", "n_clicks"))
# def stop_button(n):
#     log_1.append(["Stop_Button",time.perf_counter_ns(), np.nan,np.nan, np.nan,np.nan, np.nan, np.nan,np.nan,np.nan])
#     return n

# @callback(Output("clear_times","children"), Input("clear_button", "n_clicks"))

# def clear_button(n):
#     log_1.clear()
#     log_1.append(["Under Limit",time.perf_counter_ns(), np.nan,np.nan, np.nan,np.nan, np.nan, np.nan,np.nan,np.nan])
#     return n


def refresh_directory(profile_settings,save_text,n_clicks):
    """This function refreshes the list of files available for analysis in the parent directory"""
    folder_path = save_text[save_text.find("C:"):save_text.find("\\",save_text.find("\\",len("The results will be saved to "+profile_settings[0]["path"])))+1]
    print(folder_path)
    options = os.listdir(folder_path)
    value = options[-1]
    return options,value
app.callback(
    Output("file_dropdown", "options"),
    Output("file_dropdown","value"),
    Input("profile_settings","data"),
    Input("save_text","children"), 
    Input("refresh_button","n_clicks"))(refresh_directory)

@callback(Output("live-figure", "figure"),Output("temp_graph","figure"),Output("V_vs_I_graph","figure"),Output("Status_Message","children"),Input("start_button", "n_clicks"),Input("profile_settings","data"),Input("profile_stages","data"),Input({"type":"equipment_address", "id":ALL}, "value"),Input('interval-component', 'n_intervals'),Input("Y-Axis","value"),Input("Interval_user","value"))

def run_measurement(start,profile_settings, profile_stages,instrument_addresses,n,yaxis1,interval_user):
    # check to make sure the start button triggered this, else do nothing
    button_id = ctx.triggered_id
    # print(button_id)
   
    
    if button_id == "start_button":
        hard_stop.append("Go")
        # connect to instruments
        def equipment_object(object):
            connections = {}
            rm = pyvisa.ResourceManager()
            for instrument in object:
                address = instruments[instrument]["address"]
                if instruments[instrument]["method"] == "Resource_Manager":
                    try:
                        connections[instrument] = rm.open_resource(address)
                    except:
                        connections[instrument] = "none"
                elif instruments[instrument]["method"] == "lakeshore":
                    try:
                        model = address[:address.find("_")]
                        com_port = address[address.find("_")+1:]
                        print(model + "(57600,com_port=com_port)")
                        connections[instrument] = eval(model + "(57600,com_port=com_port)")
                    except:
                        connections[instrument] = "none"
            return connections
        
        equipment_updated = instruments
        for i,instrument in enumerate(equipment_updated):
            equipment_updated[instrument]["address"] = instrument_addresses[i]
        conn = equipment_object(equipment_updated)
       
        print("Here 0",conn)
                
        # redo time profile fresh
        I_start = float(profile_settings[0]["I_start"])
        sampling_rate_on = float(profile_settings[0]["sampling_rate_on"])
        sampling_rate_off = float(profile_settings[0]["sampling_rate_off"])
        edited_stages = {}
        for i,row in enumerate(profile_stages):
            del profile_stages[i]["stage"]
            edited_stages[str(i+1)] = profile_stages[i]
        # print(edited_stages)
        # print(I_start)
        current_profile = [0]
        time_profile = []
        for stage in edited_stages.keys():
            while max(current_profile) < float(edited_stages[stage]["target"]):
                # print(edited_stages[stage])
                # point1
                if len(time_profile) == 0:
                    # print("start")
                    time_profile.append(0)
                else:
                    time_profile.append(time_profile[len(time_profile)-1])
                    current_profile.append(0)
                #point2
                time_profile.append(time_profile[len(time_profile)-1] + float(edited_stages[stage]["step_gap"]))
                current_profile.append(0)
                #point3
                time_profile.append(time_profile[len(time_profile)-1])
                if (max(current_profile) == 0):
                    # print("start2")
                    current_profile.append(I_start)
                else:
                    current_profile.append(current_profile[len(current_profile)-3] + float(edited_stages[stage]["increment"]))
                #point4
                time_profile.append(time_profile[len(time_profile)-1] + float(edited_stages[stage]["pulse_length"]))
                current_profile.append(current_profile[len(current_profile)-1])


                # incre
                # I_inst += stages[stage]["increment"]
                    
                #Increment peak for the next cycle
                # peak +=1
                # print(time_profile,current_profile)
            time_profile = time_profile[:-2]
            current_profile = current_profile[:-2]
            time_profile.append(time_profile[len(time_profile)-1])
            current_profile.append(float(edited_stages[stage]["target"]))
            time_profile.append(time_profile[len(time_profile)-1] + float(edited_stages[stage]["dwell"]))
            current_profile.append(float(edited_stages[stage]["target"]))
        # create functions for measure, set
        def measure_fake(V_lim,set_current):
            timestart = time.perf_counter_ns()
            voltage = _read_fake("V_K",set_current)
            if voltage > V_lim:
                _set_fake("I",0)
                print(voltage," is higher than the limit of ",V_lim, " with a set current of ", set_current)
                limit_status = "Over Limit"
                hard_stop.append("Stop")
                voltage_k = voltage
                voltage_psu = np.nan
                current_on = 0
                current = np.nan
                temp_a = np.nan
                temp_b = np.nan
                
            else:
                voltage =_read_fake("V_K",set_current)
                current = _read_fake("I",set_current)
                voltage_k = (_read_fake("V_K",set_current) + voltage)/2 #take voltage reading twice, surrounding the current measurement, then take the average Voltage
                voltage_psu = _read_fake("V_PSU",set_current)
                if set_current == 0:
                    current_on = 0
                else:
                    current_on = 1
                limit_status = "Under Limit"
                temp_a = _read_fake("T_a",set_current)
                temp_b = _read_fake("T_b",set_current)

                
            timeend = time.perf_counter_ns()
            time_meas = (timestart + timeend)/2
            return [limit_status,time_meas,set_current,current,voltage_k,voltage_psu,current_on,temp_a,temp_b,V_lim]
        def measure(V_lim,set_current):
            timestart = time.perf_counter_ns()
            voltage = _read("V_K")
            if abs(voltage) > V_lim:
                _set("I",0)
                print(voltage," is higher than the limit of ",V_lim, " with a set current of ", set_current)
                limit_status = "Over Limit"
                hard_stop.append("Stop")
                voltage_k = voltage
                voltage_psu = np.nan
                current_on = 0
                current = np.nan
                temp_a = np.nan
                temp_b = np.nan
                
            else:
                #voltage =_read("V_K")
                current = _read("I")
                voltage_k = voltage#(_read("V_K") + voltage)/2 #take voltage reading twice, surrounding the current measurement, then take the average Voltage
                voltage_psu = _read("V_PSU")
                if set_current == 0:
                    current_on = 0
                else:
                    current_on = 1
                limit_status = "Under Limit"
                temp_a,temp_b = _read("Temps")
                #temp_b = _read("T_b")

                
            timeend = time.perf_counter_ns()
            time_meas = (timestart + timeend)/2
            return [limit_status,time_meas,set_current,current,voltage_k,voltage_psu,current_on,temp_a,temp_b,V_lim]
    # This is a function which will connect with the instrument and take an actual reading
        def _read_fake(Metric,set_current):
            if Metric == "V_K":
                value = 1e-6*1*(set_current/3)**23.33 + np.random.normal(0,1e-6)
            elif Metric == "V_PSU":
                value = (set_current + np.random.normal(0,max(1e-3,set_current/1000)))*.0795 #assuming V = IR and R = 0.0795 Ohms
            elif Metric == "I":
                value = set_current + np.random.normal(0,max(1e-6,set_current/1000))
            elif Metric == "Temps":
                value = [23,24]
            #elif Metric == "T_b":
                #value = 24
            else:
                value = np.nan
            return value
        
        def _read(Metric):
            if Metric == "V_K":
                value = float(conn["keithley"].query("MEASURE:VOLTAGE:DC?"))
            elif Metric == "V_PSU":
                value = float(conn["keysight"].query("MEASURE:VOLTAGE:DC?"))
            elif Metric == "I":
                value = float(conn["keysight"].query("MEASURE:CURRENT:DC?"))
            elif Metric == "Temps":
                value = [float(item) for item in conn["lakeshore"].query("KRDG? A;KRDG? B").split(sep = ";")]
            #elif Metric == "T_b":
                #value = float(conn["lakeshore"].query("KRDG? B"))
            else:
                value = np.nan
            return value
        # this is a function which will set the desired metric (likely Current) current on the instrument
        def _set_fake(Metric,desired_value):
            # print(Metric,desired_value)
            connection_status = True
            return connection_status

        def _set(metric,desired_value):
            # print(Metric,desired_value)
            if metric == "I":
                if desired_value == 0:
                    conn["keysight"].write("OUTPUT OFF")
                    connection_status = "command sent"
                else:
                    conn["keysight"].write(f"CURRENT {desired_value}A")
                    conn["keysight"].write("OUTPUT ON")
                    connection_status = "command sent"
            else:
                connection_status = "metric not recognized"
            return connection_status
        
        # build save statement again
        if profile_settings[0]["save_it"] == "Yes":
            try:
                sample_name = profile_settings[0]["sample_name"]
                date = datetime.now().strftime("%Y%m%d_")           #date for file names
                datet = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")   #date and time for file names
                save_it = True
                new_dir_name = str(date) + str(sample_name)
                new_dir = pathlib.Path(profile_settings[0]["path"], new_dir_name)
                new_dir.mkdir(parents=True, exist_ok=True)
                new_file = new_dir / ('IV_Curve_' + str(datet) + '.csv')
                save_statement = "The results will be saved to " + str(new_dir) +  '\_'+sample_name + str(datet)
            except:
                save_it = False
                save_statement = "The results will not be saved, unable to create folder with specified path"

        else:
            save_it = False
            save_statement = "The results will not be saved"

        if profile_settings[0]["mode"] == "Simulation":
            if easygui.ccbox("Simulation only\nTotal run time is estimated to be " + str(round(time_profile[-1]/60,1)) + " minutes. \n" + save_statement  +".\nWould you like to proceed?"):
                # create app for viewing the data
                
                # Initialize the set_current to 0
                _set_fake("I",0)
                V_lim = float(profile_settings[0]["V_lim"])
                # start the timer
                time_start = time.perf_counter_ns()
                # initialize the log list
                # log_1 = []
                log_1.append(measure_fake(V_lim,0))
                # print(log_1[-1])   
                # Cycle through each transition in current, performing measurements and checking for voltage
                for sequence in range(len(current_profile)):
                    # check for voltage break condition
                    if log_1[-1][0] != "Under Limit":
                        print("breaking")
                        break
                    else:
                        # perform a measurement for this sequence as quickly as possible, prior to current  set-up
                        log_1.append(measure_fake(V_lim,current_profile[sequence]))
                        # print(current_profile[sequence])
                        # Set current at desired set-point
                        _set_fake("I",current_profile[sequence])
                        # may need to add a delay here to allow the current to get to max before measuring voltage ?? 
                        # take measurements of the metrics following the appropriate sampling_rate for the type of sequence (on or off)
                        while ((time.perf_counter_ns() - time_start)/1e9 < time_profile[sequence]) & (log_1[-1][0] == "Under Limit") & (hard_stop[-1] == "Go"):
                            # take a measurement
                            log_1.append(measure_fake(V_lim,current_profile[sequence]))
                            # wait for a delay until the next measurement (fastest python measurements are about )
                            if current_profile[sequence] == 0:
                                time_1 = time.perf_counter_ns()
                                while (time.perf_counter_ns() - time_1)/1e9 < sampling_rate_off:
                                    pass
                                # time.sleep(min((time_profile[sequence] - time_profile[sequence-1])/4,sampling_rate_off))
                            else:
                                time_1 = time.perf_counter_ns()
                                while (time.perf_counter_ns() - time_1)/1e9 < sampling_rate_on:
                                    pass
                                # time.sleep(sampling_rate_on)
                            # print(log_1[-1])
                            # print(len(log_1))
                _set_fake("I",0)
                log = pd.DataFrame(data = log_1,columns = ["Limit_Status","Time [ms]", "Set Current [A]","Measured Current [A]", "Keithley Voltage [V]","PSU Voltage [V]", "Current ON", "Ta [K]","Tb [K]","V_lim [V]"])
                log["Time [ms]"] = (log["Time [ms]"].copy() - time_start)/1e6
                # Save off in a specific format
                if save_it:
                    log[log.Limit_Status == "Under Limit"].loc[:,log.columns[1:]].to_csv(str(new_dir) +  '\Pulsed_IV_' + str(datet) + ".csv")
                else:
                    pass
                log = pd.DataFrame(data = log_1,columns = ["Limit_Status","Time [ms]", "Set Current [A]","Measured Current [A]", "Keithley Voltage [V]","PSU Voltage [V]", "Current ON", "Ta [K]","Tb [K]","V_lim [V]"])
                log["Time (s)"] = (log["Time [ms]"].copy() - time_start)/1e9
                if yaxis1 == "Keithley Voltage [V]":
                    ys = [yaxis1,"V_lim [V]"]
                else:
                    ys = yaxis1
                fig = px.line(log,x = "Time (s)",y = ys) 
                # log["time_per_meas [ms]"] = log["Time [ms]"].diff()
                # # fig = px.line(log,"Time [ms]","Keithley Voltage [V]")
                # display(px.line(log,"Time [ms]","Keithley Voltage [V]"))
                # display(px.line(log,"Time [ms]",["Measured Current [A]","Set Current [A]"]))
                # display(px.line(log,"Time [ms]","time_per_meas [ms]"))
            else:
                fig = "none"
                print("user cancelled")
        else:
            if easygui.ccbox("Real Data\nTotal run time is estimated to be " + str(round(time_profile[-1]/60,1)) + " minutes. \nThe file " + save_statement  +".\nWould you like to proceed?"):
                # create app for viewing the data
                
                # Initialize the set_current to 0
                _set("I",0)
                V_lim = float(profile_settings[0]["V_lim"])
                # start the timer
                time_start = time.perf_counter_ns()
                # initialize the log list
                # log_1 = []
                log_1.append(measure(V_lim,0))
                # print(log_1[-1])   
                # Cycle through each transition in current, performing measurements and checking for voltage
                for sequence in range(len(current_profile)):
                    # check for voltage break or hard stop condition
                    if (log_1[-1][0] != "Under Limit") or (hard_stop[-1] != "Go"):
                        _set("I",0) ## turn off any current that may be there.
                        log_1.append(log_1[0])
                        if hard_stop[-1] != "Go": ## add a row to the log mentioning a hard stop is what stopped the program
                            log_1[-1][0] = "Hard Stop"
                        else: ## add a row to the log mentioning that the limit breach is what stopped the program
                            log_1[-1][0] = "Stopped due to limit breach"
                        log_1[-1][1] = time.perf_counter_ns()
                        for i,row in enumerate(log_1[-1]):
                            if i < 2:
                                pass
                            else:
                                log_1[-1][i] = np.nan 
                        print("breaking")
                        break
                    else:
                        # perform a measurement for this sequence as quickly as possible, prior to current  set-up
                        log_1.append(measure(V_lim,current_profile[sequence]))
                        # print(current_profile[sequence])
                        # Set current at desired set-point
                        _set("I",current_profile[sequence])
                        # may need to add a delay here to allow the current to get to max before measuring voltage ?? 
                        # take measurements of the metrics following the appropriate sampling_rate for the type of sequence (on or off)
                        while ((time.perf_counter_ns() - time_start)/1e9 < time_profile[sequence]) & (log_1[-1][0] == "Under Limit") & (hard_stop[-1] == "Go"):
                            # take a measurement
                            log_1.append(measure(V_lim,current_profile[sequence]))
                            # wait for a delay until the next measurement (fastest python measurements are about )
                            if current_profile[sequence] == 0:
                                time_1 = time.perf_counter_ns()
                                while (time.perf_counter_ns() - time_1)/1e9 < sampling_rate_off:
                                    pass
                                # time.sleep(min((time_profile[sequence] - time_profile[sequence-1])/4,sampling_rate_off))
                            else:
                                time_1 = time.perf_counter_ns()
                                while (time.perf_counter_ns() - time_1)/1e9 < sampling_rate_on:
                                    pass
                                # time.sleep(sampling_rate_on)
                            # print(log_1[-1])
                            # print(len(log_1))
                _set("I",0)
                # if completed naturally (no limit breach or hard stop), add message 
                if (log_1[-1][0] == "Under Limit"):
                    status_message = "Program completed without exceeding the limit"
                    log_1.append(log_1[0])
                    log_1[-1][0] = "Program completed without exceeding the limit"
                    log_1[-1][1] = time.perf_counter_ns()
                    for i,row in enumerate(log_1[-1]):
                        if i < 2:
                            pass
                        else:
                            log_1[-1][i] = np.nan 
                log = pd.DataFrame(data = log_1,columns = ["Limit_Status","Time [ms]", "Set Current [A]","Measured Current [A]", "Keithley Voltage [V]","PSU Voltage [V]", "Current ON", "Ta [K]","Tb [K]","V_lim [V]"])
                log["Time [ms]"] = (log["Time [ms]"].copy() - time_start)/1e6
                # Save off in a specific format
                if save_it:
                    log.to_csv(str(new_dir) +  '\ALL_'+sample_name + str(datet) + ".csv")
                    log[log.Limit_Status == "Under Limit"].loc[:,log.columns[1:]].to_csv(str(new_dir) +  '\_'+sample_name + str(datet) + ".csv")
                else:
                    pass
                log = pd.DataFrame(data = log_1,columns = ["Limit_Status","Time [ms]", "Set Current [A]","Measured Current [A]", "Keithley Voltage [V]","PSU Voltage [V]", "Current ON", "Ta [K]","Tb [K]","V_lim [V]"])
                log["Time (s)"] = (log["Time [ms]"].copy() - time_start)/1e9
                if yaxis1 == "Keithley Voltage [V]":
                    ys = [yaxis1,"V_lim [V]"]
                else:
                    ys = yaxis1
                fig = px.line(log,x = "Time (s)",y = ys) 
                # log["time_per_meas [ms]"] = log["Time [ms]"].diff()
                # # fig = px.line(log,"Time [ms]","Keithley Voltage [V]")
                # display(px.line(log,"Time [ms]","Keithley Voltage [V]"))
                # display(px.line(log,"Time [ms]",["Measured Current [A]","Set Current [A]"]))
                # display(px.line(log,"Time [ms]","time_per_meas [ms]"))
            else:
                fig = "none"
                print("user cancelled")
    
    else: # if the trigger was not the start button, just update the graphs and status message
        try:
            if log_1[-1][0] == "Under Limit":
                if len(log_1) == 0:
                    status_message = "Not Collecting Data, Recently Cleared"
                else:
                    status_message = "Collecting " + profile_settings[0]["mode"]
            else:
                status_message = "Not Collecting Data, last log was '" + log_1[-1][0] + "'"
            log = pd.DataFrame(data = log_1,columns = ["Limit_Status","Time [ms]", "Set Current [A]","Measured Current [A]", "Keithley Voltage [V]","PSU Voltage [V]", "Current ON", "Ta [K]","Tb [K]","V_lim [V]"])
            try:
                log["Time (s)"] = (log["Time [ms]"].copy() - time_start)/1e9
            except: 
                # print("no time_start yet")
                try:
                    log["Time (s)"] = (log["Time [ms]"].copy() - time.perf_counter_ns() - min(log["Time [ms]"].copy()[1:] - time.perf_counter_ns()))/1e9
                except:
                    log = pd.DataFrame(data = {"Limit_Status":"Under Limit","Time [ms]":time.perf_counter_ns(), "Set Current [A]":np.nan,"Measured Current [A]":np.nan, "Keithley Voltage [V]":np.nan,"PSU Voltage [V]":np.nan, "Current ON":np.nan, "Ta [K]":np.nan,"Tb [K]":np.nan,"V_lim [V]":np.nan,"Time (s)":time.perf_counter_ns()},index = [0])
        except:
            status_message = "No Data to Plot"
            log = pd.DataFrame(data = {"Limit_Status":"Under Limit","Time [ms]":time.perf_counter_ns(), "Set Current [A]":np.nan,"Measured Current [A]":np.nan, "Keithley Voltage [V]":np.nan,"PSU Voltage [V]":np.nan, "Current ON":np.nan, "Ta [K]":np.nan,"Tb [K]":np.nan,"V_lim [V]":np.nan,"Time (s)":time.perf_counter_ns()},index = [0])
        if yaxis1 == "Keithley Voltage [V]":
            ys = [yaxis1,"V_lim [V]"]
        else:
            ys = yaxis1
        fig = px.line(log,x = "Time (s)",y = ys) 
        temp_graph = px.line(log,x = "Time (s)", y = ["Ta [K]", "Tb [K]"], title = "Temp Monitor",width = 400)  
        V_vs_I_graph = px.scatter(log,x = "Measured Current [A]", y = "Keithley Voltage [V]", title = "Voltage vs Current",width = 400)
    return fig,temp_graph,V_vs_I_graph,status_message

# @callback(Output("interval-component", "interval"),Input("Interval_user","value"))

# def update_interval(value):
#     return float(value)*1000

def status_equip(instrument):
    def status(address):
        if instruments[instrument]["method"] == "Resource_Manager":
            rm = pyvisa.ResourceManager()
            try:
                rm.open_resource(address)
                status = "Connected Resource Manager"
            except pyvisa.errors.VisaIOError as e:
                status = e.args[0]
            except:
                status = "Error"
    
        elif instruments[instrument]["method"] == "lakeshore":
            model = address[:address.find("_")]
            com_port = address[address.find("_")+1:]
            if model == "Model335":
                try:
                    lk = Model335(57600,com_port=com_port)
                    status = "Connected Lakeshore"
                except Exception as e:
                    status = e.args[0]
                except:
                    status = "Error_lakeshore"
            else:
                status ="Address not Recognized"
        else:
            status = "Equipment not configured"
        return str(status)[:50]
    return status

for instrument in list(instruments.keys()):
    app.callback(
        Output(instrument+"_status", "children"),
        Input({"id":instrument+"_address","type":"equipment_address"}, "value"))(status_equip(instrument))

@callback(Output("profile_figure", "figure"),Input("profile_settings","data"),Input("profile_stages","data"))

def profile_graph(profile_settings, profile_stages):
    I_start = float(profile_settings[0]["I_start"])
    edited_stages = {}
    for i,row in enumerate(profile_stages):
        del profile_stages[i]["stage"]
        edited_stages[str(i+1)] = profile_stages[i]
    # print(edited_stages)
    # print(I_start)
    current_profile = [0]
    time_profile = []
    for stage in edited_stages.keys():
        while max(current_profile) < float(edited_stages[stage]["target"]):
            # print(edited_stages[stage])
            # point1
            if len(time_profile) == 0:
                # print("start")
                time_profile.append(0)
            else:
                time_profile.append(time_profile[len(time_profile)-1])
                current_profile.append(0)
            #point2
            time_profile.append(time_profile[len(time_profile)-1] + float(edited_stages[stage]["step_gap"]))
            current_profile.append(0)
            #point3
            time_profile.append(time_profile[len(time_profile)-1])
            if (max(current_profile) == 0):
                # print("start2")
                current_profile.append(I_start)
            else:
                current_profile.append(current_profile[len(current_profile)-3] + float(edited_stages[stage]["increment"]))
            #point4
            time_profile.append(time_profile[len(time_profile)-1] + float(edited_stages[stage]["pulse_length"]))
            current_profile.append(current_profile[len(current_profile)-1])


            # incre
            # I_inst += stages[stage]["increment"]
                
            #Increment peak for the next cycle
            # peak +=1
            # print(time_profile,current_profile)
        time_profile = time_profile[:-2]
        current_profile = current_profile[:-2]
        time_profile.append(time_profile[len(time_profile)-1])
        current_profile.append(float(edited_stages[stage]["target"]))
        time_profile.append(time_profile[len(time_profile)-1] + float(edited_stages[stage]["dwell"]))
        current_profile.append(float(edited_stages[stage]["target"]))

    # print(time_profile)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x = time_profile, y = current_profile))
    fig2.update_layout({"xaxis":{"title":"Time (s)"},"yaxis":{"title":"Current (A)"},"title":"Current vs Time"})
    fig2.update_layout({"height":500})
    # display(fig2)
    return fig2

@callback(Output("save_text", "children"),Input("profile_settings", "data"))

def set_save_text(profile_settings):
    if profile_settings[0]["save_it"] == "Yes":
        try:
            sample_name = profile_settings[0]["sample_name"]
            date = datetime.now().strftime("%Y%m%d_")           #date for file names
            datet = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")   #date and time for file names

            new_dir_name = str(date) + str(sample_name)
            new_dir = pathlib.Path(profile_settings[0]["path"], new_dir_name)
            new_dir.mkdir(parents=True, exist_ok=True)
            new_file = new_dir / ('IV_Curve_' + str(datet) + '.csv')
            save_statement = "The results will be saved to " + str(new_dir) +  '\IV_Curve_' + str(datet)
        except:
            save_statement = "Please check your file path, unable to create a folder."
    else:
        save_statement = "The results will not be saved"
    return save_statement

@callback(Output("instrument_list","children"),Input("inst_check","n_clicks"))

def inst_check(click):
    rm = pyvisa.ResourceManager()
    insts = list(rm.list_resources())
    text = ""
    for inst in insts:
        text = text + inst + "<>"
    return text

if __name__ == '__main__':
    app.run(debug=debug, port=port)
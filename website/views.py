from flask import Blueprint, jsonify, render_template, request
from .models import Temperature, pH, Distilled_Oxygen, Pressure
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

views = Blueprint('views', __name__)

# Dictionary that maps data options to their respective model classes
data_table_options = {'All': None,
                      'Temperature': Temperature,
                      'pH': pH,
                      'Distilled Oxygen': Distilled_Oxygen,
                      'Pressure': Pressure}

# Dictionary that maps time window options to their respective time delta
time_window_options = {'All Time': None,
                       'Last Hour': timedelta(hours=1),
                       'Last 24 Hours': timedelta(days=1),
                       'Last Week': timedelta(weeks=1),
                       'Last Month': timedelta(days=30)}

# Dictionary that stores dataframes for each data option for download purpose
database = {}


# dashboard page
@views.route("/", methods=['GET', 'POST'])
def dashboard():
    """
    Displays a dashboard page that allows the user to select which data 
    to view and over what time period, and displays the data as a plot.
    """
    # default for data and time_window
    selected_data_option = ''
    time_window = time_window_options['All Time']

    # update data and time window based on user's input
    if request.method == 'POST':
        selected_data_option = request.form['data_options']
        time_window = time_window_options[request.form['time-window']]

    # check the user's selected data option and display plot accordingly.
    if selected_data_option == '':
        # display nothing
        plot_div = ''
    elif selected_data_option == 'All':
        # display all plots in a 2x2 grid
        fig = make_subplots(rows=2,
                            cols=2,
                            subplot_titles=['Temperature', 'pH',
                                            'Distilled Oxygen', 'Pressure'],
                            vertical_spacing=0.5)
        for i, option in enumerate(data_table_options.keys()):
            if i == 0:
                continue
            df = df_generate(option, time_window)
            row = ((i-1) // 2) + 1
            col = ((i-1) % 2) + 1
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df['value'],
                mode='lines',
                name=option,
                showlegend=False),
                row=row, col=col)
            fig.update_xaxes(title_text='Time', row=row, col=col)
            fig.update_yaxes(title_text=option, row=row, col=col)
        plot_div = fig.to_html(full_html=False)
    else:
        # display chosen data plot
        df = df_generate(selected_data_option, time_window)

        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Scatter(
            x=df['time'],
            y=df['value'],
            mode='lines',
            name=selected_data_option))
        fig.update_layout(title=f"{selected_data_option} Data",
                          xaxis_title='Time', yaxis_title=selected_data_option)

        plot_div = fig.to_html(full_html=False)

    if request.method == 'POST':
        return jsonify({'plot_div': plot_div})

    return render_template('index.html',
                           data_options=data_table_options.keys(),
                           time_options=time_window_options.keys(),
                           plot_div=plot_div)


# route for downloading data as csv
@views.route("/download_csv", methods=['POST'])
def download_csv():
    """
    This function allows the user to download data that they select and specify a time period for. 
    The selected data is then converted to CSV format and returned as a list of tuples, where each 
    tuple contains the name of the data and its corresponding CSV file. 
    """

    selected_data_option = request.form['data_options']
    result_csv = []

    # check the user's selected data option and generate the CSV data accordingly.
    if selected_data_option == '':
        # no data is being converted to csv
        result_csv = []
    elif selected_data_option == "All":
        # all data is being converted to csv
        for key, val in database.items():
            csv = val.to_csv(index=False)
            result_csv.append((key, csv))
    else:
        # chosen data is being converted to csv
        csv = database[selected_data_option].to_csv(index=False)
        result_csv.append((selected_data_option, csv))

    return result_csv


# function for convert database to dataframe
def df_generate(option, time_window):
    """
    Generates a pandas dataframe containing data for the given data option within the specified time window.

    Args:
        option (str): The selected data option.
        time_window (timedelta): The selected time window, represented as a timedelta object.

    Returns:
        pandas.DataFrame: The generated dataframe containing the selected data within the specified time window.
    """
    selected_table = data_table_options[option]
    data = selected_table.query.all()
    df = pd.DataFrame([(d.time, d.value)
                       for d in data], columns=['time', 'value'])

    # filter the time by given time window
    if time_window:
        end_time = datetime.now()
        start_time = end_time - time_window
        df = df.loc[(df['time'] >= start_time) & (df['time'] <= end_time)]

    database[option] = df

    return df

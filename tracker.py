# CLIENT MANAGEMENT SYSTEM
# RUDRANSH KUMAR
# This program inputs user-provided body metrics to a 
# Google Sheet for tracking.

import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def track():

    # runs core editing interface and functions
    # input: user enters command to console
    # output: None

    dataTable = initialize()
    prompts = [
        'Enter a command number to continue:',
        ('Add daily entry for today'.ljust(49,'.') + '1'),
        ('Update height'.ljust(49,'.') + '2'),
        ('Quit'.ljust(49,'.') + 'X')
    ]
    for prompt in prompts:
        print(prompt)
    asking = True 
    legalEntry = True
    while asking:
        command = raw_input().rstrip()
        if legalEntry:
            print('-' * 50)
        if command.lower() in ['quit','x','abort']:
            quit()
        elif command == '1':
            addTDailyEntry(dataTable)
        elif command == '2':
            updateHeight(dataTable)
        else:
            legalEntry = False
            print('Illegal command: Please choose from the commands above.')

def initialize():

    # authorizes program to access spreadsheet, and returns worksheet
    # input: None
    # output: data table (worksheet)

    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(\
    'manager_credentials.json',scope)
    client = gspread.authorize(credentials)
    system = client.open('Body Metrics')
    dataTable = system.worksheet('Data Table')
    return dataTable

def getRow(worksheet):

    # finds and returns row number of next available (empty) row
    # input: worksheet (worksheet)
    # ouput: row number (int)

    values = filter(None,worksheet.col_values(1))
    return len(values) + 1

def addTDailyEntry(dataTable):

    # adds day-to-day variable metrics (date, mass, fat %, water %, 
    # and muscle %) and does not update height
    # input: user enters mass, fat %, water %, and muscle % to console
    # output: None

    running = True
    while running:
        mass = raw_input('Enter current mass (kg): ').rstrip()
        fatPercent = raw_input('Enter current body fat (%): ').rstrip()
        waterPercent = raw_input(\
        'Enter current water composition (%): ').rstrip()
        musclePercent = raw_input(\
        'Enter current muscle composition (%): ').rstrip()
        date = datetime.now().date()
        row = getRow(dataTable)
        height =  dataTable.cell(row - 1,2)
        columns = {1:date,2:height,3:mass,4:fatPercent,\
        5:waterPercent,6:musclePercent}
        for column in columns.keys():
            dataTable.update_cell(row,column,columns[column])
        print('Today\'s metrics have been entered.')
        print('-' * 50)
        running = False
    quit()

def updateHeight(dataTable):

    # adds/updates a height record 
    # input: user enters day to add record from, 
    # and enters new height to console
    # ouput: None

    running = True 
    while running:
        gettingDate = True 
        while gettingDate:
            date = raw_input(\
            'Enter date (yyyy-mm-dd) from which to edit or "today": ').rstrip()
            if date.lower() == 'today':
                date = datetime.now().date()
                gettingDate = False
            else:
                try:
                    date = date.split('-')
                    date = [int(component) for component in date]
                    date = datetime(date[0],date[1],date[2]).date()
                except ValueError:
                    print(\
                    'Date Error: Enter a date in the format prescribed above.')
                else:
                    gettingDate = False
        height = raw_input('Enter the new height to update to: ').rstrip()
        dates = filter(None,dataTable.col_values(1))
        endRow = getRow(dataTable)
        if date in dates:
            startRow = dates.index(date) + 1
            for row in range(startRow,endRow):
                dataTable.update_cell(row,2,height)
            running = False
            print(('Past records have been updated ' + \
            'to reflect height change from {}.').format(str(date)))
        elif date < datetime.now().date():
            dataTable.update_cell(endRow,1,date)
            dataTable.update_cell(endRow,2,height)
            running = False
            print('A new height-only record was created on {}.'.format(str(date)))
        elif date == datetime.now().date():
            mass = raw_input('Enter current mass (kg): ').rstrip()
            fatPercent = raw_input('Enter current body fat (%): ').rstrip()
            waterPercent = raw_input(\
            'Enter current water composition (%): ').rstrip()
            musclePercent = raw_input(\
            'Enter current muscle composition (%): ').rstrip()
            columns = {1:date,2:height,3:mass,4:fatPercent,\
            5:waterPercent,6:musclePercent}
            for column in columns.keys():
                dataTable.update_cell(endRow,column,columns[column])
            running = False
            print('Today\'s metrics and height have been entered.')
        else:
            print('Date Error: A future record cannot be edited.')
        print('-' * 50)
    quit()

# RUN PROGRAM
track()  
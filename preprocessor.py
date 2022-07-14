import pandas as pd
import re


def preprocessor(data):
    message_pattern = '\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2} [^-\s]+ - '
    # the resulting list has an empty string at the beggining, adding [1:] to exclude it in the result
    message = re.split(message_pattern, data)[1:]
    date_time = re.findall(message_pattern, data)

    # Creating dataframe
    df = pd.DataFrame({'message': message, 'date_time': date_time})
    df[['sender', 'message']] = df['message'].str.split(': ', 1, expand=True)
    df['date_time'] = df['date_time'].str.replace(' - ', '')
    df['message'] = df['message'].str.replace('\n', ' ')
    # Removing any white spaces
    df['date_time'] = df['date_time'].str.strip()
    df['message'] = df['message'].str.strip()
    df['sender'] = df['sender'].str.strip()
    df['date_time'] = pd.to_datetime(df['date_time'], format='%m/%d/%y, %I:%M %p')
    # Splitting the components of date time
    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month_name()
    df['month_short'] = df['date_time'].dt.month_name().str[:3]
    df['day'] = df['date_time'].dt.day
    df['day_name'] = df['date_time'].dt.day_name()
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute

    # removing incorrect sender names
    df = df[df['sender'].str.contains('blocked this contact') == False]
    df = df[df['sender'].str.contains('Group notification') == False]
    df = df[df['sender'].str.contains('Messages and calls are end-to-end') == False]
    df = df[df['sender'].str.contains('Your security code') == False]
    # showing only first 3 columns
    df_display = df.iloc[:, 0:3]
    # rearranging the columns
    df_display = df_display.loc[:, ['date_time', 'sender', 'message']]
    # adding period column to plot heatmap
    period = []
    for i in df['hour']:
        if i == 23:
            period.append(str(i) + '-' + str('0'))
        else:
            period.append(str(i) + '-' + str(i + 1))
    df['period'] = period
    return df, df_display

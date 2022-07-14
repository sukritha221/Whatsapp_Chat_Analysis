from wordcloud import WordCloud
from urlextract import URLExtract
import emoji
from collections import Counter
import pandas as pd

extractor = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]
        # shape[0] returns the number of rows
    num_message = df.shape[0]

    # num words
    words = []
    for message in df['message']:
        if message is not None:
            words = words + message.split()

    # num of media sent
    num_media = df[df['message'] == '<Media omitted>'].shape[0]

    # num of links sent
    links = []

    for message in df['message']:
        if message is not None:
            links = links + extractor.find_urls(message)

    return num_message, len(words), num_media, len(links)


'''def remove_unwanted_members(member_list):
    new_list = []
    for e in member_list:
        # users to be removed in bracket
        if e not in ('You blocked this contact. Tap to unblock.', 'You unblocked this contact.', 'Group notification'):
            new_list.append(e)
    member_list = new_list
    member_list.sort()
    member_list.insert(0, 'Overall')

    member_list = [x for x in member_list if 'Your security code' not in x]
    member_list = [x for x in member_list if 'Messages and calls are end-' not in x]
    return member_list'''


def busiest_users(df):
    # this graph will be shown only for overall analysis
    message_counts = df['sender'].value_counts()
    senders = message_counts.index
    # senders.tolist()
    # using [1:] to remove overall added in the function
    # senders = remove_unwanted_members(senders)[1:]
    # keeping only the wanted members in num_messages list
    num_messages = message_counts.values

    # busiest users df
    df = round((df['sender'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df = df.rename(columns={'index': 'sender', 'sender': 'percentage'})
    return senders, num_messages, df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]
    words_list = df['message'].str.cat(sep=' ')
    stop_words = ['<media', 'omitted>']
    for i in stop_words:
        words_list = words_list.lower().replace(i, '')
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(words_list)
    return df_wc


def emoji_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]

    timeline_df = df.groupby(['month', 'year'], sort=False).count()['message'].reset_index()
    timeline_df['month_year'] = timeline_df['month'] + '-' + timeline_df['year'].astype(str)
    return timeline_df


def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    busy_day = df.groupby(['day_name']).count()['message'].reindex(day_order)
    return busy_day


def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    busy_month = df.groupby(['month_short']).count()['message'].reindex(month_order)
    return busy_month


def heat_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['sender'] == selected_user]
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    df_pivot = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0).reindex(day_order)
    df_pivot = df_pivot.reindex(
        columns=['0-1', '1-2', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10', '10-11', '11-12', '12-13', '13-14',
                 '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-0'])
    return df_pivot

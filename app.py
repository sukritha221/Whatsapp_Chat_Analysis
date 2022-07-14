import streamlit as st
import preprocessor
import functinos
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Adding title to the sidebar
st.sidebar.title('WhatsApp Chat Analysis')

# Uploading chat file
uploaded_file = st.sidebar.file_uploader('Upload file')
if uploaded_file is not None:
    # data is uploaded as a stream of bytes, need to convert it into string
    bytes_data = uploaded_file.getvalue()
    # converting into utf-8 string
    data = bytes_data.decode('utf-8')

    # displaying the data
    # st.text(data)

    # calling the preprocess/cleaning function
    df, df_display = preprocessor.preprocessor(data)
    # displaying the df in streamlit
    st.dataframe(df_display)

    # showing members in the chat
    member_list = df['sender'].unique().tolist()
    # member_list = functinos.remove_unwanted_members(member_list)
    member_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox('Show analysis with respect to:', member_list)

    if st.sidebar.button('Show Analysis'):
        col1, col2, col3, col4 = st.columns(4)

        num_messages, words, num_media, num_links = functinos.fetch_stats(selected_user, df)

        with col1:
            st.header('Total Messages Sent')
            st.title(num_messages)
        with col2:
            st.header('Number of words')
            st.title(words)
        with col3:
            st.header('Number of Media files sent')
            st.title(num_media)
        with col4:
            st.header('Number of links shared')
            st.title(num_links)

        # busiest users
        if selected_user == 'Overall':
            st.title('Busiest Users')
            senders, num_messages, df_perc = functinos.busiest_users(df)
            fig, ax = plt.subplots()
            ax.pie(num_messages, labels=senders, autopct='%0.1f')

            # to add labels to bar chart
            # def addlabels(x, y):
            #    for i in range(len(x)):
            #        plt.text(i, y[i], y[i])

            #  addlabels(senders, num_messages)
            #  plt.xlabel("Members of Chat")
            #  plt.ylabel("Number of Messages sent")
            st.pyplot(fig)

        #  with col2:
        #     st.dataframe(df_perc)

        # Word Cloud
        st.title('Word Cloud')
        df_wc = functinos.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Emojis
        st.title('Number of Emjois')
        emoji_df = functinos.emoji_analysis(selected_user, df)

        # col1, col2 = st.columns(2)

        # with col1:
        st.dataframe(emoji_df)
        # with col2:
        #    fig, ax = plt.subplots()
        #    ax.bar(emoji_df[0].head(10), emoji_df[1].head(10))
        #   st.pyplot(fig)

        # Messages line graph
        st.title('Timeline')
        timeline_df = functinos.timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot(timeline_df['month_year'], timeline_df['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activiy Map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day = functinos.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='green')
            plt.xticks(rotation=10)
            st.pyplot(fig)

        with col2:
            st.header('Most busy month')
            busy_month = functinos.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation=10)
            st.pyplot(fig)

        # heatmap
        st.title('Heatmap')
        df_heatmap = functinos.heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(df_heatmap.fillna(0), linewidths=.5)
        ax.set(ylabel=None)
        ax.set(xlabel=None)
        st.pyplot(fig)



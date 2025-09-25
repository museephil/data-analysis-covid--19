# cord19_streamlit.py
# Philip Musee David
# Quick exploration of CORD-19 metadata with Streamlit

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import streamlit as st

# ------------------------------
# Load the dataset
# ------------------------------
df = pd.read_csv('metadata.csv')  # metadata.csv must be in the same folder

st.title("CORD-19 Data Explorer")
st.write("Exploring COVID-19 research papers with Python & Streamlit")

# Show basic info
st.subheader("Dataset Overview")
st.write("Rows and Columns:", df.shape)
st.write("Columns and types:")
st.write(df.dtypes)
st.write("Missing values per column:")
st.write(df.isnull().sum())

# ------------------------------
# Clean the data
# ------------------------------
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['abstract'] = df['abstract'].fillna('')
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(x.split()))

st.write("Data cleaned! Ready for analysis.")

# ------------------------------
# Analysis & Visualizations
# ------------------------------

# Papers per year
st.subheader("Publications by Year")
year_counts = df['year'].value_counts().sort_index()
fig1, ax1 = plt.subplots()
ax1.bar(year_counts.index, year_counts.values)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
ax1.set_title("Papers Published Each Year")
st.pyplot(fig1)

# Top journals
st.subheader("Top 10 Journals Publishing COVID-19 Research")
top_journals = df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots(figsize=(10,5))
top_journals.plot(kind='bar', ax=ax2)
ax2.set_xlabel("Journal")
ax2.set_ylabel("Number of Papers")
ax2.set_title("Top 10 Journals")
st.pyplot(fig2)

# Word cloud of titles
st.subheader("Word Cloud of Paper Titles")
all_titles = ' '.join(df['title'].dropna())
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
fig3, ax3 = plt.subplots(figsize=(12,6))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis("off")
st.pyplot(fig3)

# Most frequent words in titles
st.subheader("Most Frequent Words in Titles")
words = all_titles.lower().split()
common_words = Counter(words).most_common(20)
st.write(common_words)

# ------------------------------
# Interactive Filtering
# ------------------------------
st.subheader("Filter Papers by Year")
year_range = st.slider("Select year range", int(df['year'].min()), int(df['year'].max()), (2020, 2021))
filtered_df = df[df['year'].between(year_range[0], year_range[1])]
st.write("Sample of filtered papers:")
st.write(filtered_df[['title', 'authors', 'journal', 'year']].head(10))

# Plot filtered papers
st.subheader("Filtered Papers Count by Year")
year_counts_filtered = filtered_df['year'].value_counts().sort_index()
fig4, ax4 = plt.subplots()
ax4.bar(year_counts_filtered.index, year_counts_filtered.values)
ax4.set_xlabel("Year")
ax4.set_ylabel("Number of Papers")
ax4.set_title("Filtered Papers per Year")
st.pyplot(fig4)

st.write("All done! Scroll through tables and plots above to explore the data, done by Philip Musee David.")

from matplotlib import image
from streamlit_option_menu import option_menu
from wordcloud import STOPWORDS
from wordcloud import WordCloud
import requests
import pickle
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
st.title("JOB RECOMMENDATION SYSTEM")
st.image("./image/job_search_portals.png")
# sidebar starts
with st.sidebar:
    choose = option_menu("App Gallery", ["Recommender", "Other Recommendations", "Want to change your industry?", "Location-wise jobs", "Jobs on basis of skills", "Correlational Heatmaps and Our Recommendations", "Experience and Vacancies", "Top Companies and Sectors for Jobs"],
                         icons=['house', 'camera fill', 'kanban',
                                'book', 'person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#ffffff"},
        "icon": {"color": "#222EEE ", "font-size": "25px", "--hover-color": "white"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#43A5FC "},
    }
    )
#sidebar ends
#navbar starts
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #3498DB;">
  <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">YouTube</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Twitter</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)
datas = pickle.load(open('job_list.pkl', 'rb'))

if choose == "Recommender":
    city_list = datas['joblocation_adress'].unique()
    industry_list = datas['Industry'].unique()
    exp_list = datas['Min Experience'].unique()
    selected_city = st.selectbox(
        "Type or select location from the dropdown",
        city_list

    )
    selected_industry = st.selectbox(
        "Type or select industry from the dropdown",
        industry_list

    )
    selected_exp = st.selectbox(
        "Type or select minimum-experience from the dropdown",
        exp_list
        
    )
    ans = datas.loc[(datas['joblocation_adress'] == selected_city)
                    & (datas['Industry'] == selected_industry)
                    & (datas['Min Experience'] == selected_exp)][[
                        'company',
                        'jobtitle',
                        'Education',
                        'payrate',
                        'numberofpositions',
                    ]]
    if st.button('Show Recommendation'):
        st.write(ans)
# other recommendations
if choose == "Other Recommendations":
    # recommendations based on cosine similarity
    cosine_sim = pickle.load(open('cosine_sim.pkl', 'rb'))
    st.subheader("FIND SIMILAR JOBS")
    def recommend(job):
        index = datas[datas['jobtitle'] == job].index[0]
        distances = sorted(
            list(enumerate(cosine_sim[index])), reverse=True, key=lambda x: x[1])
        recommended_job_names = []
        for i in distances[1:6]:
            recommended_job_names.append(datas.iloc[i[0]].jobtitle)
        return recommended_job_names
    job_list = datas['jobtitle'].unique()
    selected_job = st.selectbox(
        "Type or select a job from the dropdown",
        job_list
    )
    if st.button('Get Similar Jobs'):
        recommended_job_names = recommend(selected_job)
        st.table(recommended_job_names)
    st.subheader("Plot graph between parameters")
    x = pd.crosstab(datas['Education'], datas['Industry'])

   
        # plotting graph between different features
    column = st.selectbox(
        "Type or select a job from the dropdown",
        (datas.columns[3:])
    )
    column1 = st.selectbox(
        "Type or select a job from the dropdown",
        (datas.columns[4:])
    )
    if st.button("Plot"):
        fig11 = plt.figure(figsize=(14, 15))
        sns.barplot(datas[column], datas[column1])
        plt.xticks(rotation=90)
        st.pyplot(fig11)
        plt.show()
if choose == "Location-wise jobs":
    st.header("LOCATION WISE AVAILABLE JOBS")

    fig = plt.figure(figsize=(10, 5))
    sns.countplot(datas['joblocation_adress'], palette='inferno')
    plt.title('Locations with Highest Jobs', fontsize=20)
    plt.xlabel(' ')
    plt.xticks(rotation=90)
    st.pyplot(fig)
    plt.show()
    counts = datas['joblocation_adress'].value_counts()
    datas = datas.loc[datas['joblocation_adress'].isin(
        counts.index[counts > 25])]
    st.table(datas['joblocation_adress'].value_counts())
if choose == "Jobs on basis of skills":
    st.header("AVAILABILITY OF JOBS FOR SKILLS")
    datas['Skills'] = datas['Skills'].str.split(" - ")
    datas['Skills'] = datas['Skills'].apply(
        lambda x: x[1] if len(x) > 1 else x[0])

    fig2 = plt.figure(figsize=(15, 5))
    # fig2 =plt.rcParams['figure.figsize'] = (15, 4)
    plt.title('Requirement of Overall Skills', fontsize=20)
    datas['Skills'].value_counts().head(25).plot(kind='bar', color='black')
    plt.grid()
    plt.yticks(fontsize=15)
    plt.ylabel(" ")
    plt.xlabel(" ")
    st.pyplot(fig2)
    st.table(datas['Skills'].value_counts())
# plt.show()

# if check:
#     st.write(check)
if choose == "Correlational Heatmaps and Our Recommendations":
    st.header("CORRELATIONAL HEAT MAPS FOR JOBS")
    jobs = pd.read_csv('jobs.csv')
    fig3 = plt.figure(figsize=(10, 4))
    sns.heatmap(jobs[['PayGrade', 'EducationLevel',
                      'Experience', 'OrgImpact', 'ProblemSolving',
                      'Supervision', 'ContactLevel', 'FinancialBudget']].corr(),
                cmap='Greens',
                annot=True)
    plt.title('Correlation Map for the Jobs Data', fontsize=20)
    st.pyplot(fig3)
    plt.show()
if choose == "Experience and Vacancies":
    st.header("EXPERIENCE FOR JOBS")
    fig4 = plt.figure(figsize=(15, 10))
    plt.rcParams['figure.figsize'] = (15, 10)
    plt.title('Minimum Experience required from each Industry')
    sns.barplot(datas['Industry'], datas['Min Experience'], palette='magma')
    plt.xticks(fontsize=15, rotation=90)
    plt.xlabel(' ')
    st.pyplot(fig4)
    plt.show()
    st.header("VACANCIES FOR DIFFERENT EDUCATION")
    counts = datas['Education'].value_counts()
    datas = datas.loc[datas['Education'].isin(counts.index[counts >= 25])]

    fig5 = plt.figure(figsize=(12, 6))
    plt.rcParams['figure.figsize'] = (12, 6)
    x = datas[datas['Education'] != 'Any']
    sns.countplot(y=x['Education'], palette='inferno')
    plt.title('Vacancies for Different Education', fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylabel(" ")
    plt.xlabel(" ")
    st.pyplot(fig5)
    st.table(datas['Education'].value_counts())


# companies wise jobs
if choose == "Top Companies and Sectors for Jobs":
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(background_color='gold',
                          max_words=50,
                          stopwords=stopwords,
                          width=2000,
                          height=2000).generate(str(datas['jobtitle']))

    wordcloud2 = WordCloud(background_color='lightgrey',
                           stopwords=stopwords,
                           width=2000,
                           height=2000).generate(str(datas['company']))
    fig9, ax = plt.subplots(figsize=(12, 8))

    plt.subplot(1, 2, 1)
    plt.imshow(wordcloud)
    plt.title('Job Titles', fontsize=20)
    plt.axis('off')
    fig10, ax = plt.subplots(figsize=(12, 8))

    plt.subplot(1, 2, 2)
    plt.imshow(wordcloud2)
    plt.title('Companies', fontsize=20)
    plt.axis('off')

    plt.show()

    col1, col2 = st.columns(2)

    with col1:
        st.pyplot(fig9)

    with col2:
        st.pyplot(fig10)
# top 20 companies providing jobs
    fig8 = plt.figure(figsize=(15, 12))

    plt.rcParams['figure.figsize'] = (15, 12)
    sns.barplot(y=datas['company'].value_counts().head(30).index,
                x=datas['company'].value_counts().head(30).values,
                palette='inferno')
    plt.title('Top Companies providing Jobs', fontsize=20)
    plt.yticks(fontsize=15)
    st.pyplot(fig8)
    plt.show()
    st.header("TOP SECTORS FOR JOBS")
    datas['Industry'] = datas['Industry'].str.split(' / ')
    datas['Industry'] = datas['Industry'].apply(lambda x: x[0])
    fig6 = plt.figure(figsize=(15, 7))
    plt.rcParams['figure.figsize'] = (15, 7)
    plt.title('Top Sectors for Jobs', fontsize=20)
    sns.barplot(y=datas['Industry'].value_counts().head(10).index,
                x=datas['Industry'].value_counts().head(10).values,
                palette='copper')
    st.pyplot(fig6)
# recommending industry on basis of previous industry

if choose == "Want to change your industry?":
    industry_list = datas['Industry'].unique()
    st.header("WANT TO CHANGE YOUR INDUSTRY?")
    st.subheader("Get the similar industries you can apply to")
    select_previous_industry = st.selectbox(
        "Type or select a job from the dropdown",
        industry_list
    )
    
 #  def recommendation_jobs(Industry = list(datas['Industry'].value_counts().index)):
    x = pd.crosstab(datas['Education'], datas['Industry'])
    jobs = x[select_previous_industry]
    similar_jobs = x.corrwith(jobs)
    similar_jobs = similar_jobs.sort_values(ascending=False)
    similar_jobs = similar_jobs.iloc[2:]
    sol = similar_jobs.head(3)
    if st.button('Recommend'):
        st.write(sol)
    st.subheader("Job Vacancies for different job levels")
    st.image("./image/download.png")

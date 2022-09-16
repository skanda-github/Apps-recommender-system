import streamlit as st
import pickle
import pandas as pd
from bs4 import BeautifulSoup
import requests

# ---- Title & Icon ----
st.set_page_config(page_title = "Recommender Page", page_icon = ":globe_with_meridians:",layout = 'wide')

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            img { height : 220px }
            .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            button[title="View fullscreen"] {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.text("")
st.title("Apps Recommender System")
st.text("")

new = pickle.load(open('apps_list.pkl','rb'))
new = pd.DataFrame(new)
apps_similarity = pickle.load(open('apps_similarity.pkl','rb'))

# @st.cache()
def app_image(app_name):

    url_head = 'https://www.google.no/search?q='
    value = app_name
    url_tail = '&client=opera&hs=cTQ&source=lnms&tbm=isch&sa=X&ved=0ahUKEwig3LOx4PzKAhWGFywKHZyZAAgQ_AUIBygB&biw=1920&bih=982'
    url = url_head + value + url_tail


    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')

    for i,raw_img in enumerate(soup.find_all('img',limit = 2)):
        img_link = raw_img.get('src')
        if (img_link) and (i == 1):
            photo_url = img_link
            break 

    return str(photo_url)


def apps_recommend(select_app):
    recommend_list = []
    recommend_list_app_id = []
    recommend_list_images = []
    app_index = new[new['app_name'] == select_app].index[0]
    app_distances = sorted(list(enumerate(apps_similarity[app_index])),reverse = True,key = lambda x : x[1])
    for i in app_distances[1:6]:
        recommend_list.append(new.iloc[i[0]].app_name)
        recommend_list_app_id.append(new.iloc[i[0]].app_id)
        recommend_list_images.append(app_image(new.iloc[i[0]].app_name))
    

    return recommend_list, recommend_list_app_id, recommend_list_images


apps_list = new['app_name'].values
select_app = st.selectbox("Choose any app", apps_list)

st.text("")
if st.button("Recommend"):
    st.text("")
    # st.success("Success: App Selected is " + select_app)
    # st.text("")
    
    apps, links, images = apps_recommend(select_app)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(apps[0])
        st.image(images[0],width = 220)

    with col2:
        st.text(apps[1])
        st.image(images[1],width = 220)

    with col3:
        st.text(apps[2])
        st.image(images[2],width = 220)

    with col4:
        st.text(apps[3])
        st.image(images[3],width = 220)

    with col5:
        st.text(apps[4])
        st.image(images[4],width = 220)
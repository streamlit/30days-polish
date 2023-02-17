import streamlit as st
import os
import pandas as pd
from PIL import Image
import glob

def update_params():
    st.experimental_set_query_params(challenge=st.session_state.day)

md_files = sorted([int(x.strip('Day').strip('.md')) for x in glob.glob1('content',"*.md") ])

# Logo and Navigation
col1, col2, col3 = st.columns((1,4,1))
with col2:
    st.image(Image.open('streamlit-logo-secondary-colormark-darktext.png'))
st.markdown('# 30 dni ze Streamlitem po polsku 🎈')

days_list = [f'Dzień {x}' for x in md_files]

query_params = st.experimental_get_query_params()

if query_params and query_params["challenge"][0] in days_list:
    st.session_state.day = query_params["challenge"][0]

selected_day = st.selectbox('Rozpocznij lekcję 👇', days_list, key="day", on_change=update_params)

with st.expander("Przeczytaj więcej o inicjatywie #30DaysOfStreamlit"):
    st.markdown('''**#30DaysOfStreamlit** to programistyczne wyzwanie, które pomoże Ci rozpocząć przygodę z 
    tworzeniem aplikacji Streamlit.

    
    Przede wszystkim, nauczysz się:
    - Jak skonfigurować środowisko do tworzenia aplikacji Streamlit 
    - Jak zbudować swoją pierwszą aplikację
    - W jaki sposób korzystać w wielu niesamowitych widżetów, które pomogą Ci zbudować interaktywną aplikację
    ''')

# Sidebar
st.sidebar.header('O Streamlicie')
st.sidebar.markdown('[Streamlit](https://streamlit.io) jest biblioteką Pythona, która umożliwia tworzenie '
                    'interaktywnych aplikacji internetowych opartych na danych. '
                    'Aplikacje tworzysz wyłącznie z użyciem Pythona i bez konieczności używania innych technologii,'
                    ' takich jak JavaScript, HTML, CSS.')

st.sidebar.header('Zobacz też (materiały po angielsku)')
st.sidebar.markdown('''
- [Dokumentacja Streamlita](https://docs.streamlit.io/)
- [Ściągawka](https://docs.streamlit.io/library/cheatsheet)
- [Książka](https://www.amazon.com/dp/180056550X) (Pierwsze kroki ze Streamlitem w przetwarzaniu danych)
- [Blog](https://blog.streamlit.io/how-to-master-streamlit-for-data-science/) (Jak opanować Streamlita do analizy danych)
''')

st.sidebar.header('Wdrażanie')
st.sidebar.markdown('Dzięki [Społecznościowej Chmurze Streamlita](https://streamlit.io/cloud) możesz szybko wdrożyć '
                    'swoją aplikację za pomocą kilku kliknięć.')

# Display content
for i in days_list:
    if selected_day == i:
        st.markdown(f'# 🗓️ {i}')
        j = i.replace('Dzień ', 'Day')
        with open(f'content/{j}.md', 'r') as f:
            st.markdown(f.read())
        if os.path.isfile(f'content/figures/{j}.csv') == True:
            st.markdown('---')
            st.markdown('### Ilustracje')
            df = pd.read_csv(f'content/figures/{j}.csv', engine='python', quotechar="'")
            for i in range(len(df)):
                st.image(f'content/images/{df.img[i]}')
                st.info(f'{df.figure[i]}: {df.caption[i]}')

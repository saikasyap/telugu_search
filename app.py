import warnings
from database import Elastic_Search
from sentence_transformers import SentenceTransformer
import pandas as pd
import time
import numpy as np
from aksharamukha import transliterate
pd.set_option("display.max_rows", None, "display.max_columns", None)
from PIL import Image
import streamlit as st
#from st_aggrid import AgGrid
pd.set_option("display.max_rows", None, "display.max_columns", None)
#nltk.download('stopwords')


url = "http://localhost:9200"
et = Elastic_Search(url, index_name='search_telugu')

# Converting Search Results to pandas DataFrame
def res_toDF(res):
    hits = res['hits']['hits']
    if len(hits) > 0:
        keys = list(hits[0]['_source'].keys())

        out = [[h['_score']] + [h['_source'][k] for k in keys] for h in hits]
        df = pd.DataFrame(out, columns=['_score'] + keys)
      
    else:
        df = pd.DataFrame([])
    return df



def basic_search(query,field):
    res_1 = et.search(query,field=field,type='match',embedder=None, size =1000)
    df1 = res_toDF(res_1)
    if not df1.empty:
        #Exact Match..
        df1['_score'] =np.where(df1['text'].str.contains(query), 4+df1['_score'],df1['_score'])
        df1['_score'] = df1['_score']+1
        df1 = df1.sort_values(by='_score', ascending=False)
        df1 = df1.drop_duplicates()
    else:
        df1 = pd.DataFrame([])
    return df1

def basic_search_tokenize(query,field):
    res_1 = et.search(query,field=field,type='match',embedder=None, size =1000)
    df1 = res_toDF(res_1)
    if not df1.empty:
        #Exact Match..
        df1['_score'] =np.where(df1['text'].str.contains(query), 1+df1['_score'],df1['_score'])
        df1 = df1.sort_values(by='_score', ascending=False)
        df1 = df1.drop_duplicates()
    else:
        df1 = pd.DataFrame([])
    return df1


STYLE = """
<style>
img {
    max-width: 100%;
}
</style> """
# CSS to inject contained in a string
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

# Inject CSS with Markdown
lst1 = []


st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
def main():

    st.title('Search Engine for Telugu')

    #image = Image.open('/home/kasyap/Desktop/Search/search_search/search/data/indic-search-logo.png')
    #st.image(image, use_column_width=True)

    # Collect Input from user :
    query = str()
    query = str(st.text_input("Enter the Text you want to search(Press Enter once done)"))



    start_time = time.time()  # get the current time in seconds

    try:
        st.markdown("#### search results in the text")
        if len(query) > 0:
        # Call the function to extract the data. pass the topic and filename you want the data to be stored in.
            with st.spinner("Please wait, Search Results are being extracted"):
            #Akshara Mukha translation to 
                #query1 = transliterate.process('autodetect', 'Telugu',  query, param="script_code")
                st.write("Your query was :" , query)

                #query3 = transliterate.process('autodetect', 'iast',  query, param="script_code")
                lst = basic_search(query, 'text')
        
                #tokenized_sent1 = tokenizer.tokenize(query3)
              
                lst = lst.drop_duplicates(subset=['text'], keep = 'first',ignore_index=True)

        

                lst = lst.drop_duplicates(subset=['text'], keep = 'first',ignore_index=True)
                st.json(lst.head(15).to_json(orient="records"),expanded = True)


        st.success('Search results have been extracted !!!!')
    except:
        st.write("No results Found")
    end_time = time.time()  # get the current time again
    time_taken = end_time - start_time  # calculate the time difference
    st.markdown (f"Time taken : {time_taken:.2f} seconds")

    if st.button("Exit"):
        st.balloons()


if __name__ == '__main__':
    main()

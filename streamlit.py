import streamlit as st
from fact_checker import fact_check_fn, fact_check_fn_img, fact_check_fn_video
import json
import os

st.title("Factstral AI")

claim = st.text_input("Enter the claim you want to fact check:")
num_articles = st.number_input("Enter the number of sources to refer to:", min_value=1, step=1)
uploaded_file = st.file_uploader("Upload an image or video", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"])

brave_api_key = st.text_input("Enter your Brave API key:", type="password")
mistral_api_key = st.text_input("Enter your Mistral API key:", type="password")
if brave_api_key:
    os.environ['BRAVE_API_KEY'] = brave_api_key
if mistral_api_key:
    os.environ['MISTRAL_API_KEY'] = mistral_api_key

if st.button("Check Claim"):
    if uploaded_file is not None:
        # print(uploaded_file.name)
        # file_path = '/tmp/' + uploaded_file
        # print(file_path)
        # with open(file_path, "wb") as f:
        #     f.write(uploaded_file.getbuffer())

        save_directory = '/tmp'
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        
        # Create the full path where the file will be saved
        file_path = os.path.join(save_directory, uploaded_file.name)

        # Write the uploaded file's content to a new file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if uploaded_file.type.startswith('image/'):
            st.write("Uploaded file is an image.")
            st.image(uploaded_file)
            check = fact_check_fn_img(file_path, num_articles)
            
        elif uploaded_file.type.startswith('video/'):
            st.write("Uploaded file is a video.")
            st.video(uploaded_file)
            check = fact_check_fn_video(file_path, num_articles)

        os.remove(file_path)

    elif claim:
        check = fact_check_fn(claim, num_articles)

    check_json = check[8:-4]
    check_dict = json.loads(check_json)
    print(check_dict)

    summary = check_dict.get("summary", "No summary available")
    st.markdown("### Summary of the findings:")
    st.markdown(summary)

    with st.expander(f"Agreeing Articles ({check_dict['tally']['agree']['count']})", expanded=False):
        for article in check_dict['tally']['agree']['sources']:
            st.write(article['source_name'] + "(" + article['link'] + ")")
            st.write(article['summary'])
            st.divider()

    with st.expander(f"Neutral Articles ({check_dict['tally']['neutral']['count']})", expanded=False):
        for article in check_dict['tally']['neutral']['sources']:
            st.write(article['source_name'] + "(" + article['link'] + ")")
            st.write(article['summary'])
            st.divider()

    with st.expander(f"Disagreeing Articles ({check_dict['tally']['disagree']['count']})", expanded=False):
        for article in check_dict['tally']['disagree']['sources']:
            st.write(article['source_name'] + "(" + article['link'] + ")")
            st.write(article['summary'])
            st.divider()

# if st.button("Check Claim"):
    
#     check = fact_check_fn(claim, num_articles)
#     check_json = check[8:-4]
#     check_dict = json.loads(check_json)
#     print(check_dict)

#     summary = check_dict.get("summary", "No summary available")
#     st.markdown("### Summary of the findings:")
#     st.markdown(summary)

#     with st.expander(f"Agreeing Articles ({check_dict['tally']['agree']['count']})", expanded=False):
#         for article in check_dict['tally']['agree']['sources']:
#             st.write(article['source_name'] + "(" + article['link'] + ")")
#             st.write(article['summary'])
#             st.divider()

#     with st.expander(f"Neutral Articles ({check_dict['tally']['neutral']['count']})", expanded=False):
#         for article in check_dict['tally']['neutral']['sources']:
#             st.write(article['source_name'] + "(" + article['link'] + ")")
#             st.write(article['summary'])
#             st.divider()

#     with st.expander(f"Disagreeing Articles ({check_dict['tally']['disagree']['count']})", expanded=False):
#         for article in check_dict['tally']['disagree']['sources']:
#             st.write(article['source_name'] + "(" + article['link'] + ")")
#             st.write(article['summary'])
#             st.divider()

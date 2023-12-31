import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

word_to_index = imdb.get_word_index()

def sentiment_classification(new_review_text, model):
    max_review_length = 500
    new_review_tokens = [word_to_index.get(word, 0) for word in new_review_text.split()]
    new_review_tokens = pad_sequences([new_review_tokens], maxlen=max_review_length)
    prediction = model.predict(new_review_tokens)
    if type(prediction) == list:
        prediction = prediction[0]
    return "Positive" if prediction > 0.5 else "Negative"

def tumor_detection(img, model):
    img = Image.open(img)
    img=img.resize((128,128))
    img=np.array(img)
    input_img = np.expand_dims(img, axis=0)
    res = model.predict(input_img)
    return "Tumor Identified" if res else "No Tumor"


#title
st.title("Sentiment Classification / Tumor Detection")

st.sidebar.title("Choose Your Option")
st.sidebar.write("Execute Sentiment Analysis or Identify Tumors.")

task = st.sidebar.radio("", ("Sentiment Classification", "Identify Tumors"))

model=None
st.subheader(f"Performing {task}")

if task == "Sentiment Classification":
    new_review_text = st.text_area("Enter a New Review:", value="")
    if st.button("Submit") and not new_review_text.strip():
        st.warning("Please enter a review.")

    if new_review_text.strip():
        st.subheader("Choose your Model ")
        model_option = st.selectbox("Select Model", ("Perceptron", "Backpropagation", "DNN", "RNN", "LSTM"))

        if model_option == "Perceptron":
            with open(r'H:\Deep-learning\Assignment2\Perceptron.pkl', 'rb') as file:
                model = pickle.load(file)
        elif model_option == "DNN":
            model = load_model(r'H:\Deep-learning\Assignment2\DNN.keras')
        elif model_option == "Backpropagation":
            with open(r'H:\Deep-learning\Assignment2\Backprop.pkl', 'rb') as file:
                model = pickle.load(file)
        elif model_option == "RNN":
            model = load_model(r'H:\Deep-learning\Assignment2\RNN.keras')
        elif model_option == "LSTM":
            model = load_model(r'H:\Deep-learning\Assignment2\LSTM.keras')
        else:
            model = load_model(f'{model_option}.keras')


        if st.button("Classify as Positive or Negative"):
            if model is not None:
                result = sentiment_classification(new_review_text, model)
                st.subheader("Result")
                st.write(f"**{result}**")

elif task == "Identify Tumors":
    st.subheader("Identify Tumors")
    uploaded_file = st.file_uploader("Upload a tumor image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        model = load_model(r'H:\Deep-learning\Assignment2\CNN.keras')
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=False, width=200)
        st.write("")

        if st.button("Identify Tumor"):
            result = tumor_detection(uploaded_file, model)
            st.subheader("Result")
            st.write(f"**{result}**")


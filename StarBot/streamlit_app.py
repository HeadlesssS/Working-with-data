import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Star Query", layout="centered")
st.title("🌟 Star Information Query")

@st.cache_resource
def load_resources():
    try:
        # Try loading from saved files first
        df = pd.read_csv("GAIA-with-NAME.csv")
        df["Name_normalized"] = (
            df["Name"]
            .str.lower()
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )
        
        gru_model = load_model("gru_model.h5")
        mlp_model = load_model("mlp_model.h5")
        bilstm_model = load_model("bilstm_model.h5")
        
        import pickle
        with open("tokenizer.pkl", "rb") as f:
            tokenizer = pickle.load(f)
        with open("label_encoder.pkl", "rb") as f:
            le = pickle.load(f)
            
    except FileNotFoundError:
        # Fallback: Load data and create dummy models if files don't exist
        st.warning("⚠️ Models not found. Please save trained models first!")
        df = pd.read_csv("GAIA-with-NAME.csv")
        df["Name_normalized"] = (
            df["Name"]
            .str.lower()
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )
        
        # Create tokenizer from data
        texts = df["Name"].dropna().tolist()
        tokenizer = Tokenizer(num_words=1000)
        tokenizer.fit_on_texts(texts)
        
        # Create dummy label encoder
        le = LabelEncoder()
        le.fit(["exists", "vmag", "color", "spectral", "parallax"])
        
        # Try loading models
        try:
            gru_model = load_model("gru_model.h5")
            mlp_model = load_model("mlp_model.h5")
            bilstm_model = load_model("bilstm_model.h5")
        except:
            gru_model = mlp_model = bilstm_model = None
            st.error("Models not found. Train and save models as .h5 files")
    
    return df, tokenizer, le, {"GRU": gru_model, "MLP": mlp_model, "BiLSTM": bilstm_model}

def query(question, model, df, tokenizer, le):
    """Query the model for intent and retrieve star data."""
    q = question.lower()
    
    seq = tokenizer.texts_to_sequences([q])
    seq = pad_sequences(seq, maxlen=15)
    intent_id = np.argmax(model.predict(seq, verbose=0))
    intent = le.inverse_transform([intent_id])[0]
    
    # Get valid star names and sort by length (longest first)
    valid_names = [name for name in df["Name_normalized"] if pd.notna(name) and isinstance(name, str)]
    valid_names = sorted(valid_names, key=len, reverse=True)
    
    star = None
    for name in valid_names:
        if name in q:
            star = name
            break
    
    if star is None:
        return "No star found in the question."
    
    # Get star data
    row = df[df["Name_normalized"] == star].iloc[0]
    
    if intent == "exists":
        return f"Yes, {row['Name']} exists."
    elif intent == "vmag":
        vmag = row['Vmag']
        return f"The Vmag of {row['Name']} is {vmag}."
    elif intent == "color":
        bv = row['B-V']
        return f"The B-V value of {row['Name']} is {bv}."
    elif intent == "spectral":
        sp = row['SpType']
        return f"The spectral type of {row['Name']} is {sp}."
    elif intent == "parallax":
        parallax = row['Parallax']
        return f"The parallax of {row['Name']} is {parallax}."


df, tokenizer, le, models = load_resources()

model_name = st.sidebar.selectbox("Select Model:", list(models.keys()))

query_text = st.text_input("Enter your query about a star (e.g., 'what is the vmag of Sirius'):")

if st.button("Get Answer", type="primary"):
    if query_text.strip():
        if models[model_name] is None:
            st.error("Selected model not loaded. Please train and save the model first.")
        else:
            result = query(query_text, models[model_name], df, tokenizer, le)
            st.success(result)
    else:
        st.warning("Please enter a query.")

import streamlit as st
import pandas as pd

# ── Load dictionary (cached for speed) ──
@st.cache_data
def load_dictionary(csv_path='runyankole.csv'):
    try:
        df = pd.read_csv(csv_path)
        def clean(value):
            if pd.isna(value):
                return ''
            return str(value).strip().lower()
        df['english'] = df['english'].apply(clean)
        df['runyankole'] = df['runyankole'].apply(clean)
        df = df[(df['english'] != '') & (df['runyankole'] != '')]
        return df
    except Exception as e:
        st.error(f"Error loading dictionary: {e}")
        return None

# ── Translation function ──
def translate_word(word, dictionary):
    if dictionary is None:
        return "Dictionary not loaded"
    word = str(word).strip().lower()
    match = dictionary.loc[dictionary['english'] == word]
    if not match.empty:
        return match['runyankole'].values[0]
    match = dictionary[dictionary['english'].str.contains(word, na=False)]
    if not match.empty:
        return match['runyankole'].values[0]
    return None

# ── UI ──
st.set_page_config(page_title="Runyankole Translator", page_icon="🌍")
st.title("🌍 English → Runyankole Translator")

dict_df = load_dictionary()

if dict_df is not None:
    st.success(f"Loaded {len(dict_df)} words")
    word = st.text_input("Enter an English word:").strip()
    if word:
        result = translate_word(word, dict_df)
        if result:
            st.success(f"**{word}** → **{result}**")
        else:
            st.error(f"'{word}' not found in dictionary")
else:
    st.error("Could not load dictionary. Make sure runyankole.csv is in the same folder.")
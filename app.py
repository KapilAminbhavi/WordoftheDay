import streamlit as st
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def explain_word(word):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who explains words in simple English and Marathi, tailored for elderly learners."
        },
        {
            "role": "user",
            "content": f"""
            Explain the word '{word}' for my elderly grandfather who is learning English. Please follow these steps:

            * PRONUNCIATION:
               - Break down the pronunciation of '{word}'.
               - Separate each syllable with a hyphen.
               - Ensure the breakdown accurately represents the English pronunciation.
               - If there are sounds in English that don't exist in Marathi, use the closest approximation and explain the difference.
               - Example format: word (मरा-ठी-ब्रेक-डाउन)

            -------------------------------------------------------------------------------------------------
            
            * ENGLISH EXPLANATION:
               - Provide a very simple explanation of '{word}' in English.
               - Use basic vocabulary and short sentences.
               - Include 1 easy-to-understand example of how to use the word in everyday situations.

            -------------------------------------------------------------------------------------------------
            
            * MARATHI TRANSLATION AND EXPLANATION:
               - Explain the meaning in simple Marathi.
               - Provide 1 example of how to use the word in Marathi sentences.
            
            -------------------------------------------------------------------------------------------------
            
            * MARATHI SYNONYMS:
               - List 2-3 Marathi synonyms or related words, if available.
            
            -------------------------------------------------------------------------------------------------
            
            * MEMORY AID:
               - Suggest a simple memory trick or association to help remember the word and its meaning.
            
            -------------------------------------------------------------------------------------------------
            
            * WORD OF THE DAY: 
                - Generate an intermediate English word of the day, a brief definition, its marathi meaning(explain it very clearly and give marathi synonyms as well) and a simple example sentence in both English and Marathi.

            Format the response clearly with appropriate headings for each section.
            """
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response['choices'][0]['message']['content'].strip()

st.title("English-Marathi Dictionary for SHASHI")

word = st.text_input("Enter an English word you'd like to learn:")

# Add an "Enter" button to submit the word
if st.button("Enter"):
    if word:
        st.write(f"### Word: {word}")

        try:
            with st.spinner("Fetching explanation..."):
                explanation = explain_word(word)

            st.markdown(explanation)

            # Add a feature to save favorite words
            if st.button("Add to Favorites"):
                favorites = st.session_state.get('favorites', [])
                if word not in favorites:
                    favorites.append(word)
                    st.session_state.favorites = favorites
                    st.success(f"'{word}' added to favorites!")
                else:
                    st.info(f"'{word}' is already in your favorites.")

            # Display favorite words
            if 'favorites' in st.session_state and st.session_state.favorites:
                st.markdown("### Your Favorite Words:")
                for fav_word in st.session_state.favorites:
                    st.write(f"- {fav_word}")

        except Exception as e:
            st.error(f"An error occurred: {e}")

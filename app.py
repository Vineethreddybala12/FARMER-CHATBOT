import streamlit as st
import traceback

from intent_classifier import IntentClassifier
from entity_extractor import extract_crop
from responder import build_response


st.set_page_config(
    page_title="🌾 Farmer Advisory Chatbot",
    page_icon="🌾",
    layout="centered"
)


@st.cache_resource
def load_classifier():
    return IntentClassifier()

classifier = load_classifier()



st.title("🌾 Farmer Advisory Chatbot")
st.caption(
    "Ask questions about crops, fertilizers, pests, irrigation, planting, harvesting, diseases, soil, seeds, markets, subsidies, or equipment."
)


if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Type your farming question here...")


if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Processing... 🌱"):

                # 🔹 SAME STEPS AS YOUR /query ROUTE
                intent_res = classifier.predict(user_input)
                intent = intent_res.get("intent")
                score = intent_res.get("score")

                crop = extract_crop(user_input)
                advice = build_response(intent, crop, user_input)

                st.markdown(advice)

        st.session_state.messages.append(
            {"role": "assistant", "content": advice}
        )

    except Exception:
        traceback.print_exc()
        error_msg = "Sorry, there was an error processing your query."

        with st.chat_message("assistant"):
            st.error(error_msg)

        st.session_state.messages.append(
            {"role": "assistant", "content": error_msg}
        )


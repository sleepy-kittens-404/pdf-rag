import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_secret(name):
    value = os.getenv(name)

    if value:
        return value

    return st.secrets[name]


API_KEY = get_secret("API_KEY")
EMBEDDING_KEY = get_secret("EMBEDDING_KEY")
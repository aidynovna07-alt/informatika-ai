import os
import csv
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Informatika AI",
    page_icon="🤖"
)

st.title("🤖 Informatika AI")
st.write("Мектептегі информатика пәніне арналған AI көмекші")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("API кілті табылмады.")
    st.stop()

client = OpenAI(api_key=api_key)

# Dataset-ті оқу
dataset = []

try:
    with open("dataset.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dataset.append(row)
except FileNotFoundError:
    st.warning("dataset.csv файлы табылмады.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Информатика бойынша сұрағыңызды жазыңыз..."):

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Жауап дайындалып жатыр..."):

            response = client.responses.create(
                model="gpt-5.6-luna",
                instructions="""
Сен Informatika AI атты мектептегі информатика пәнінің
жасанды интеллект көмекшісісің.

Оқушыға информатиканы түсінуге көмектес.
Python, алгоритмдер, айнымалылар, шарттар, циклдер,
функциялар, массивтер, деректер базасы, компьютер құрылғылары,
ақпараттық қауіпсіздік, HTML, CSS және жасанды интеллект
тақырыптарын түсінікті қазақ тілінде түсіндір.

Қажет болса код пен қарапайым мысал келтір.
Кодты әрқашан дұрыс Python синтаксисімен көрсет.

Төмендегі оқу деректерін қосымша білім көзі ретінде пайдалан:
"""
                + str(dataset)
                + """

Егер сұрақ информатикаға қатысы жоқ болса,
боттың негізгі бағыты информатика екенін түсіндір.
""",
                input=prompt
            )

            answer = response.output_text
            st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, load_prompt
import pandas as pd
import streamlit as st
import chromadb
import uuid
import os

# Load environment
load_dotenv()

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Load your Excel files
hotels_df = pd.read_excel('hotels.xlsx')
ziyarat_df = pd.read_excel('ziyarat.xlsx')
transport_df = pd.read_excel('transport.xlsx')

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="vectorstore")

# Create or get a collection
collection = client.get_or_create_collection(name="travel_data")

# Add data only if the collection is empty
if not collection.count():
    # ---- Add Hotels Data ----
    for _, row in hotels_df.iterrows():
        doc_text = f"""
        Type: Hotel
        City: {row['City']}
        Hotel Name: {row['Hotel_Name']}
        Distance: {row['Distance (m)']}
        Tier: {row['Tier']}
        Quint: {row['Quint (AED)']}
        Quad: {row['Quad (AED)']}
        Triple: {row['Triple (AED)']}
        Double: {row['Double (AED)']}
        """
        collection.add(
            documents=[doc_text],
            metadatas={"source": "hotels", "city": row['City'], "hotel_name": row['Hotel_Name']},
            ids=[str(uuid.uuid4())]
        )

    # ---- Add Ziyarat Data ----
    for _, row in ziyarat_df.iterrows():
        doc_text = f"""
        Type: Ziyarat
        City: {row['City']}
        Ziyarat Type: {row['Ziyarat_Type']}
        Private: {row['Private (AED)']}
        Sharing: {row['Sharing (AED)']}
        """
        collection.add(
            documents=[doc_text],
            metadatas={"source": "ziyarat", "city": row['City'], "ziyarat_type": row['Ziyarat_Type']},
            ids=[str(uuid.uuid4())]
        )

    # ---- Add Transport Data ----
    for _, row in transport_df.iterrows():
        doc_text = f"""
        Type: Transport
        Route: {row['Route']}
        Private: {row['Private (AED)']}
        Sharing: {row['Sharing (AED)']}
        """
        collection.add(
            documents=[doc_text],
            metadatas={"source": "transport", "route": row['Route']},
            ids=[str(uuid.uuid4())]
        )

    print("✅ Data successfully added to ChromaDB collection!")
else:
    print("⚡ Collection already has data!")


# -------------------- Streamlit UI --------------------
st.title("🕋 Umrah Package Generator")
st.write("Easily create a custom Umrah package based on your preferences.")

# Trip Duration Options
st.subheader("Select Trip Duration")
trip_option = st.radio(
    "Choose a package:",
    [
        "15 Days (8 nights in Makkah, 6 nights in Madinah)",
        "21 Days (14 nights in Makkah, 6 nights in Madinah)"
    ]
)

if "15 Days" in trip_option:
    days_in_mecca = 8
    days_in_medina = 6
    total_duration = 15
else:
    days_in_mecca = 14
    days_in_medina = 6
    total_duration = 21

# Tier and transport preferences
tier = st.selectbox("Select Tier", ["Economy", "Budget", "Luxury"])
transportation_hotel_and_airport = st.selectbox(
    "Transportation (Airport ↔ Hotel)", ["Private", "Sharing"]
)
ziyarah_type = st.selectbox(
    "Ziyarah Type", ["Private", "Sharing"]
)
room_type = st.selectbox(
    "Room Type", ["Double", "Triple", "Quad", "Quint"]
)

# -------------------- Generate Package --------------------
if st.button("Generate Umrah Package"):
    with st.spinner("Creating your package..."):

        # Query ChromaDB for related data
        query = f"""
        List of all hotels for {tier} tier in Makkah and Madinah with room rates,
        all transport routes including 'Jeddah Airport to Makkah Hotel', 'Makkah Hotel to Madinah Hotel', and 'Madinah Hotel to Airport',
        and all ziyarah options in both cities.
        """
        results = collection.query(query_texts=[query], n_results=50)

        # Combine all document results
        query_results = "\n".join(results["documents"][0]) if results["documents"] else "No data found."

        # Load prompt template
        prompt_template = load_prompt("umrah_prompt.json")

        # Chain the prompt and LLM
        chain = prompt_template | llm

        # ✅ FIX: pass input as a single dictionary
        inputs = {
            "tier": tier,
            "days_in_mecca": days_in_mecca,
            "days_in_medina": days_in_medina,
            "transport_type": transportation_hotel_and_airport,
            "ziyarah_type": ziyarah_type,
            "room_type": room_type,
            "query_results": query_results
        }

        # Call the chain
        results = chain.invoke(inputs)

        st.success("✅ Your Umrah Package is ready!")
        st.write(results.content if hasattr(results, "content") else results)


# -------------------- Prompt Template --------------------
from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=[
        "tier", "days_in_mecca", "days_in_medina",
        "transport_type", "ziyarah_type", "room_type", "query_results"
    ],
    template="""
You are an expert Umrah travel planner working for a professional travel agency.
Using the data provided below and the user preferences, create a **clean, structured, and realistic Umrah Package**.

---
**User Preferences**
- Tier: {tier}
- Room Type: {room_type}
- Days in Makkah: {days_in_mecca}
- Days in Madinah: {days_in_medina}
- Transportation (Airport ↔ Hotel): {transport_type}
- Ziyarah Type: {ziyarah_type}

---
**Available Options (Database Data)**
{query_results}

---
**Your Task**
1. Select one suitable hotel each in **Makkah** and **Madinah** that fits the tier and room type.
2. Include Ziyarah cost per person (if Private not found, assume 3× Sharing rate).
3. Include all transport costs:
   - Jeddah Airport → Makkah Hotel
   - Makkah Hotel → Madinah Hotel
   - Madinah Hotel → Airport
   If a route is missing, estimate based on similar routes.
4. Calculate **Total Price per Person (AED)** including hotels, ziyarah, and transport.
5. Present a **structured, readable summary** with bullet points and short explanations.

---
**Output Format Example**
**✅ Umrah Package Summary**
- Duration: 15 Days (8 nights in Makkah, 6 nights in Madinah)
- Tier: {tier}
- Room Type: {room_type}
- Hotel in Makkah: [Hotel Name] – {room_type} – [Rate]/person/night × [days_in_mecca] = [Subtotal] AED
- Hotel in Madinah: [Hotel Name] – {room_type} – [Rate]/person/night × [days_in_medina] = [Subtotal] AED
- Ziyarah ({ziyarah_type}): [Price] AED/person (both cities included)
- Transport ({transport_type}): [Total Transport Cost] AED/person

**💰 Total Price per Person: [Grand Total] AED**

**Highlights:**
- Comfortable stay near Haram in both cities
- Guided Ziyarah tours
- Smooth private transfers between cities and airports
"""
)

prompt_template.save("umrah_prompt.json")


# -------------------- IGNORE ABOVE --------------------
# from langchain.prompts import PromptTemplate

# # ----------- Final Clean & Structured Prompt -----------
# prompt_template = PromptTemplate(
#     input_variables=[
#         "tier", "days_in_mecca", "days_in_medina",
#         "transport_type", "ziyarah_type", "room_type", "query_results"
#     ],
#     template="""
# You are an expert Umrah travel planner at a professional travel agency.
# Use the provided data and user preferences to create a clean, well-formatted Umrah package summary.

# ---
# **User Preferences**
# - Package Tier: {tier}
# - Room Type: {room_type}
# - Days in Makkah: {days_in_mecca}
# - Days in Madinah: {days_in_medina}
# - Transportation Type: {transport_type}
# - Ziyarah: {ziyarah_type}

# ---
# **Available Data**
# {query_results}

# ---
# **Instructions for You**
# 1. Always choose **one hotel** each in Makkah and Madinah matching the tier and room type.  
#    - If an exact tier isn’t available, pick the nearest tier and clearly mention it in brackets (e.g., “closest to Standard”).  
#    - Multiply the per-night rate by the number of nights to get the total hotel cost per person.
# 2. Include both **Makkah and Madinah Ziyarah** costs and sum them up.
# 3. Include all **transport routes** below if available in data:
#    - "Jeddah Airport to Makkah Hotel" → Airport to Hotel  
#    - "Makkah Hotel to Madinah Hotel" → Makkah to Madinah  
#    - "Madinah Hotel to Airport" → Hotel to Airport  
#    If a route exists, always include its price. If not available, skip it (do not say “not provided”).
# 4. Calculate and show:
#    - **Hotel total (Makkah + Madinah)**  
#    - **Ziyarah total**  
#    - **Transport total**  
#    - **Grand total per person**
# 5. Write in a **neat, structured, readable format** using headings, bullet points, and spacing.

# ---
# **Output Format (Follow Exactly)**

# ✅ **Your Umrah Package is Ready!**

# ### 🕋 Umrah Package Summary
# - **Duration:** 15 Days (8 nights in Makkah, 6 nights in Madinah)  
# - **Tier:** Premium  
# - **Room Type:** Double  

# **🏨 Hotels**
# - Makkah: Hilton Makkah (Premium, Double) – 1200 AED/night × 8 = 9600 AED  
# - Madinah: Pullman Zamzam (Premium, Double) – 1100 AED/night × 6 = 6600 AED  
# **Total Hotels:** 16,200 AED/person  

# **🕌 Ziyarah**
# - Makkah: 100 AED/person  
# - Madinah: 100 AED/person  
# **Total Ziyarah:** 200 AED/person  

# **🚐 Transport ({transport_type})**
# - Airport to Hotel: 60 AED/person  
# - Makkah to Madinah: 70 AED/person  
# - Hotel to Airport: 60 AED/person  
# **Total Transport:** 190 AED/person  

# ### 💰 **Grand Total per Person: 16,590 AED**

# **✨ Highlights**
# - Premium hotels close to Haram  
# - Private Ziyarah tours in both cities  
# - Smooth, air-conditioned transport for all routes
# """
# )

# # save as umrah_prompt.json
# prompt_template.save("umrah_prompt.json")



# # -------------------- IGNORE BELOW --------------------

# from langchain.prompts import PromptTemplate

# # ----------- Prompt Template -----------
# prompt_template = PromptTemplate(
#             input_variables=[
#                 "tier", "days_in_mecca", "days_in_medina",
#                 "transport_type", "ziyarah_type", "room_type", "query_results"
#             ],
#             template="""
# You are an expert Umrah travel planner for a professional travel agency.
# Use the provided database data and user preferences to create a detailed custom Umrah package.

# ---
# **User Preferences**
# - Package Tier: {tier}
# - Room Type: {room_type}
# - Days in Makkah: {days_in_mecca}
# - Days in Madinah: {days_in_medina}
# - Transportation (Airport ↔ Hotel): {transport_type}
# - Ziyarah: {ziyarah_type}

# ---
# **Available Options from Database**
# {query_results}

# ---
# **Your Task**
# 1. Select one suitable hotel each in Makkah and Madinah that fits the chosen tier and room type.
# 2. Include Ziyarah details and its cost per person.
# 3. Include transportation (airport ↔ hotel) and Makkah ↔ Madinah travel.
# 4. Show the **total cost per person in AED**, calculated using the prices provided.
# 5. Provide a professional summary with bullet points.

# Format the result like this:

# **Umrah Package Summary**
# - Duration: 15 Days (8 nights in Makkah, 6 nights in Madinah)
# - Tier: Premium
# - Room Type: Double
# - Hotel in Makkah: Hilton Makkah – Double – 1200 AED/person
# - Hotel in Madinah: Pullman Zamzam – Double – 1100 AED/person
# - Ziyarah (Sharing): 55 AED/person
# - Transport (Private): 25 AED/person

# **Total Price per Person: 2380 AED**

# **Highlights:** Comfortable stay close to Haram, guided Ziyarah tours, and round-trip transport.
# """
#         )

# # save as umrah_prompt.json
# prompt_template.save("umrah_prompt.json")
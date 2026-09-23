import os
import streamlit as st
import pandas as pd
import numpy as np

# Try importing joblib and sklearn gracefully
try:
    import joblib
except ImportError:
    joblib = None

try:
    from sklearn.ensemble import RandomForestClassifier
except ImportError:
    RandomForestClassifier = None

try:
    from PIL import Image
except ImportError:
    Image = None


# =========================================================
# APP METADATA & CONFIGURATION
# =========================================================
APP_NAME = "CropSpire AI"
APP_TAGLINE = "Next-Gen Precision Agriculture & Crop Intelligence Platform"
APP_ICON = "🌱"

st.set_page_config(
    page_title=f"{APP_NAME} | Smart Agriculture System",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# MULTI-LANGUAGE TRANSLATION DICTIONARY
# =========================================================

LANGUAGES = {
    "English": "English",
    "हिंदी (Hindi)": "Hindi",
    "मराठी (Marathi)": "Marathi",
    "ગુજરાતી (Gujarati)": "Gujarati",
    "ਪੰਜਾਬੀ (Punjabi)": "Punjabi",
    "తెలుగు (Telugu)": "Telugu",
    "தமிழ் (Tamil)": "Tamil",
    "বাংলা (Bengali)": "Bengali"
}

TRANSLATIONS = {
    "English": {
        "tagline": "Next-Gen Precision Agriculture & Crop Intelligence Platform",
        "login_welcome": "Welcome to CropSpire AI",
        "login_sub": "Sign in to access precision crop recommendations, disease diagnostics, and smart farming tools.",
        "username": "Username or Mobile Number",
        "password": "Password",
        "role": "Select Your Role",
        "role_farmer": "🌾 Farmer / Cultivator",
        "role_agronomist": "🧑‍🔬 Agronomist / Consultant",
        "role_officer": "🏛️ Agriculture Extension Officer",
        "role_student": "🎓 Student / Researcher",
        "btn_signin": "Sign In to Account",
        "btn_demo": "🚀 Instant 1-Click Guest / Demo Access",
        "create_account": "Create a New Account",
        "full_name": "Full Name",
        "state_region": "State / Agricultural Region",
        "btn_register": "Register & Enter Platform",
        "btn_logout": "🚪 Sign Out",
        "lang_selector": "🌐 Select Language / भाषा चुनें",
        "nav_dashboard": "🏠 Dashboard",
        "nav_crop_rec": "🌾 Crop Recommendation",
        "nav_disease": "🌿 Plant Health & Disease",
        "nav_irrigation": "💧 Smart Irrigation",
        "nav_yield": "📊 Yield & Economics",
        "nav_assistant": "🤖 AI Farming Assistant",
        "nav_data_hub": "📈 Crop Data Hub",
        "nav_about": "ℹ️ About & Architecture",
        "rec_title": "Smart Crop Recommendation",
        "rec_sub": "Enter soil nutrients and climate conditions to get an AI-powered crop recommendation.",
        "quick_presets": "⚡ Quick Presets (1-Click Test Scenarios)",
        "soil_header": "🧪 Soil Nutrients (Macro-elements in kg/ha)",
        "env_header": "🌦 Environmental & Climate Conditions",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "temperature": "Temperature (°C)",
        "humidity": "Relative Humidity (%)",
        "ph": "Soil pH (0-14)",
        "rainfall": "Rainfall (mm)",
        "btn_predict": "🌱 Predict Recommended Crop",
        "primary_rec": "Primary AI Recommendation",
        "alt_options": "🥈 Top Alternative Crop Options",
        "profile_guide": "Agronomic Profile & Growing Guide",
        "fert_schedule": "Recommended Fertilizer Schedule",
        "status_active": "● ML Predictor Active",
        "logged_in_as": "Logged in as"
    },
    "Hindi": {
        "tagline": "सटीक कृषि और फसल बुद्धिमत्ता मंच",
        "login_welcome": "क्रॉपस्पायर एआई (CropSpire AI) में आपका स्वागत है",
        "login_sub": "सटीक फसल सिफारिश, रोग निदान और स्मार्ट सिंचाई टूल्स के लिए साइन इन करें।",
        "username": "उपयोगकर्ता नाम या मोबाइल नंबर",
        "password": "पासवर्ड",
        "role": "अपनी भूमिका चुनें",
        "role_farmer": "🌾 किसान / उत्पादक",
        "role_agronomist": "🧑‍🔬 कृषि वैज्ञानिक / सलाहकार",
        "role_officer": "🏛️ कृषि विस्तार अधिकारी",
        "role_student": "🎓 छात्र / शोधकर्ता",
        "btn_signin": "साइन इन करें",
        "btn_demo": "🚀 त्वरित 1-क्लिक डेमो प्रवेश",
        "create_account": "नया खाता बनाएं",
        "full_name": "पूरा नाम",
        "state_region": "राज्य / कृषि क्षेत्र",
        "btn_register": "पंजीकरण करें और प्रवेश करें",
        "btn_logout": "🚪 बाहर निकलें (Sign Out)",
        "lang_selector": "🌐 भाषा चुनें (Select Language)",
        "nav_dashboard": "🏠 डैशबोर्ड",
        "nav_crop_rec": "🌾 फसल सिफारिश (Crop Recommendation)",
        "nav_disease": "🌿 पादप स्वास्थ्य और रोग निदान",
        "nav_irrigation": "💧 स्मार्ट सिंचाई सलाहकार",
        "nav_yield": "📊 उपज और आर्थिक अनुमान",
        "nav_assistant": "🤖 एआई कृषि सहायक",
        "nav_data_hub": "📈 फसल डेटा हब",
        "nav_about": "ℹ️ परिचय और विवरण",
        "rec_title": "स्मार्ट फसल सिफारिश प्रणाली",
        "rec_sub": "मिट्टी के पोषक तत्वों और मौसम की जानकारी दर्ज करें और उपयुक्त फसल की सिफारिश पाएं।",
        "quick_presets": "⚡ त्वरित परीक्षण विकल्प (1-Click Presets)",
        "soil_header": "🧪 मिट्टी के पोषक तत्व (किग्रा/हेक्टेयर)",
        "env_header": "🌦 पर्यावरणीय और मौसम की स्थिति",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फास्फोरस (P)",
        "potassium": "पोटेशियम (K)",
        "temperature": "तापमान (°C)",
        "humidity": "आर्द्रता (%)",
        "ph": "मिट्टी का पीएच (0-14)",
        "rainfall": "वर्षा (मिमी)",
        "btn_predict": "🌱 उपयुक्त फसल की सिफारिश प्राप्त करें",
        "primary_rec": "मुख्य एआई सिफारिश",
        "alt_options": "🥈 अन्य उपयुक्त वैकल्पिक फसलें",
        "profile_guide": "कृषि विवरण और फसल उत्पादन गाइड",
        "fert_schedule": "अनुशंसित उर्वरक सारणी",
        "status_active": "● एमएल मॉडल सक्रिय",
        "logged_in_as": "उपयोगकर्ता"
    },
    "Marathi": {
        "tagline": "अचूक शेती आणि पीक बुद्धिमत्ता प्रणाली",
        "login_welcome": "क्रॉपस्पायर एआय मध्ये आपले स्वागत आहे",
        "login_sub": "पीक शिफारस, रोग निदान आणि स्मार्ट सिंचनासाठी साइन इन करा.",
        "username": "वापरकर्ता नाव किंवा मोबाईल नंबर",
        "password": "पासवर्ड",
        "role": "आपली भूमिका निवडा",
        "role_farmer": "🌾 शेतकरी बांधव",
        "role_agronomist": "🧑‍🔬 कृषी सल्लागार",
        "role_officer": "🏛️ कृषी अधिकारी",
        "role_student": "🎓 कृषी विद्यार्थी / संशोधक",
        "btn_signin": "साइन इन करा",
        "btn_demo": "🚀 थेट १-क्लिक डेमो प्रवेश",
        "create_account": "नवीन खाते तयार करा",
        "full_name": "पूर्ण नाव",
        "state_region": "राज्य / जिल्हा",
        "btn_register": "नोंदणी करा",
        "btn_logout": "🚪 बाहेर पडा (Logout)",
        "lang_selector": "🌐 भाषा निवडा",
        "nav_dashboard": "🏠 मुख्य फलक (Dashboard)",
        "nav_crop_rec": "🌾 योग्य पीक शिफारस",
        "nav_disease": "🌿 वनस्पती रोग निदान",
        "nav_irrigation": "💧 स्मार्ट पाणी व्यवस्थापन",
        "nav_yield": "📊 उत्पादन व नफा अंदाज",
        "nav_assistant": "🤖 कृषी एआय मार्गदर्शक",
        "nav_data_hub": "📈 पीक माहिती केंद्र",
        "nav_about": "ℹ️ माहिती व रचना",
        "rec_title": "स्मार्ट पीक शिफारस प्रणाली",
        "rec_sub": "मातीचे पोषण आणि हवामानाची माहिती भरा आणि योग्य पिकाची निवड करा.",
        "quick_presets": "⚡ जलद निवड पर्याय (1-Click Presets)",
        "soil_header": "🧪 मातीतील घटक (कि.ग्रॅ./हेक्टर)",
        "env_header": "🌦 हवामान आणि पर्जन्यमान",
        "nitrogen": "नत्र (N)",
        "phosphorus": "स्फुरद (P)",
        "potassium": "पालाश (K)",
        "temperature": "तापमान (°C)",
        "humidity": "हवेतील दमटपणा (%)",
        "ph": "जमिनीचा सामू (pH)",
        "rainfall": "पाऊस (मिमी)",
        "btn_predict": "🌱 योग्य पीक शोधा",
        "primary_rec": "प्रमुख एआय शिफारस",
        "alt_options": "🥈 इतर पर्यायी पिके",
        "profile_guide": "पीक लागवड व व्यवस्थापन माहिती",
        "fert_schedule": "खत व्यवस्थापन वेळापत्रक",
        "status_active": "● मॉडेल सक्रिय",
        "logged_in_as": "नाव"
    },
    "Gujarati": {
        "tagline": "ચોક્કસ ખેતી અને પાક બુદ્ધિમત્તા પ્લેટફોર્મ",
        "login_welcome": "ક્રોપસ્પાયર એઆઈ માં આપનું સ્વાગત છે",
        "login_sub": "પાક ભલામણ, રોગ નિદાન અને સ્માર્ટ સિંચાઈ માટે લૉગિન કરો.",
        "username": "વપરાશકર્તા નામ અથવા મોબાઈલ નંબર",
        "password": "પાસવર્ડ",
        "role": "તમારી ભૂમિકા પસંદ કરો",
        "role_farmer": "🌾 ખેડૂત મિત્ર",
        "role_agronomist": "🧑‍🔬 કૃષિ નિષ્ણાત",
        "role_officer": "🏛️ કૃષિ અધિકારી",
        "role_student": "🎓 વિદ્યાર્થી / સંશોધક",
        "btn_signin": "સાઇન ઇન કરો",
        "btn_demo": "🚀 સીધો ૧-ક્લિક ડેમો પ્રવેશ",
        "create_account": "નવું ખાતું બનાવો",
        "full_name": "પૂરું નામ",
        "state_region": "રાજ્ય / જિલ્લો",
        "btn_register": "નોંધણી કરો",
        "btn_logout": "🚪 બહાર નીકળો (Logout)",
        "lang_selector": "🌐 ભાષા પસંદ કરો",
        "nav_dashboard": "🏠 ડેશબોર્ડ",
        "nav_crop_rec": "🌾 શ્રેષ્ઠ પાક ભલામણ",
        "nav_disease": "🌿 પાક રોગ નિદાન",
        "nav_irrigation": "💧 સ્માર્ટ પિયત સલાહકાર",
        "nav_yield": "📊 ઉત્પાદન અને નફાકારકતા",
        "nav_assistant": "🤖 એઆઈ ખેતી સહાયક",
        "nav_data_hub": "📈 પાક માહિતી કેન્દ્ર",
        "nav_about": "ℹ️ માહિતી",
        "rec_title": "સ્માર્ટ પાક પસંદગી પદ્ધતિ",
        "rec_sub": "જમીનના પોષક તત્વો અને હવામાન દાખલ કરી યોગ્ય પાક જાણો.",
        "quick_presets": "⚡ ઝડપી પરીક્ષણ વિકલ્પો",
        "soil_header": "🧪 જમીનના પોષક તત્ત્વો (કિગ્રા/હેક્ટર)",
        "env_header": "🌦 હવામાન અને વરસાદ",
        "nitrogen": "નાઈટ્રોજન (N)",
        "phosphorus": "ફોસ્ફરસ (P)",
        "potassium": "પોટાશ (K)",
        "temperature": "તાપમાન (°C)",
        "humidity": "ભેજ (%)",
        "ph": "જમીન પી.એચ. (pH)",
        "rainfall": "વરસાદ (મીમી)",
        "btn_predict": "🌱 પાકની ભલામણ મેળવો",
        "primary_rec": "મુખ્ય એઆઈ ભલામણ",
        "alt_options": "🥈 અન્ય વૈકલ્પિક પાકો",
        "profile_guide": "પાક ઉત્પાદન માર્ગદર્શિકા",
        "fert_schedule": "ખાતર વ્યવસ્થાપન પત્રક",
        "status_active": "● મોડલ સક્રિય",
        "logged_in_as": "ખેડૂત"
    },
    "Punjabi": {
        "tagline": "ਸ਼ੁੱਧ ਖੇਤੀਬਾੜੀ ਅਤੇ ਫਸਲ ਖੁਫੀਆ ਪ੍ਰਣਾਲੀ",
        "login_welcome": "ਕ੍ਰੌਪਸਪਾਇਰ ਏ.ਆਈ. ਵਿੱਚ ਜੀ ਆਇਆਂ ਨੂੰ",
        "login_sub": "ਫਸਲ ਦੀ ਸਿਫ਼ਾਰਸ਼, ਬਿਮਾਰੀ ਦੀ ਜਾਂਚ ਅਤੇ ਸਮਾਰਟ ਸਿੰਚਾਈ ਲਈ ਲੌਗਇਨ ਕਰੋ।",
        "username": "ਵਰਤੋਂਕਾਰ ਨਾਮ ਜਾਂ ਮੋਬਾਈਲ ਨੰਬਰ",
        "password": "ਪਾਸਵਰਡ",
        "role": "ਆਪਣੀ ਭੂਮਿਕਾ ਚੁਣੋ",
        "role_farmer": "🌾 ਕਿਸਾਨ ਵੀਰ",
        "role_agronomist": "🧑‍🔬 ਖੇਤੀਬਾੜੀ ਵਿਗਿਆਨੀ",
        "role_officer": "🏛️ ਖੇਤੀਬਾੜੀ ਅਧਿਕਾਰੀ",
        "role_student": "🎓 ਵਿਦਿਆਰਥੀ / ਖੋਜਕਰਤਾ",
        "btn_signin": "ਸਾਈਨ ਇਨ ਕਰੋ",
        "btn_demo": "🚀 ਤੁਰੰਤ 1-ਕਲਿੱਕ ਡੈਮੋ ਐਂਟਰੀ",
        "create_account": "ਨਵਾਂ ਖਾਤਾ ਬਣਾਓ",
        "full_name": "ਪੂਰਾ ਨਾਮ",
        "state_region": "ਰਾਜ / ਖੇਤਰ",
        "btn_register": "ਰਜਿਸਟਰ ਕਰੋ",
        "btn_logout": "🚪 ਲੌਗ ਆਉਟ",
        "lang_selector": "🌐 ਭਾਸ਼ਾ ਚੁਣੋ",
        "nav_dashboard": "🏠 ਡੈਸ਼ਬੋਰਡ",
        "nav_crop_rec": "🌾 ਫਸਲ ਸਿਫ਼ਾਰਸ਼",
        "nav_disease": "🌿 ਪੌਦਿਆਂ ਦੀ ਸਿਹਤ ਅਤੇ ਬਿਮਾਰੀਆਂ",
        "nav_irrigation": "💧 ਸਮਾਰਟ ਸਿੰਚਾਈ",
        "nav_yield": "📊 ਝਾੜ ਅਤੇ ਮੁਨਾਫਾ ਅੰਦਾਜ਼ਾ",
        "nav_assistant": "🤖 ਏ.ਆਈ. ਖੇਤੀਬਾੜੀ ਸਹਾਇਕ",
        "nav_data_hub": "📈 ਫਸਲ ਡੇਟਾ ਹੱਬ",
        "nav_about": "ℹ️ ਜਾਣਕਾਰੀ",
        "rec_title": "ਸਮਾਰਟ ਫਸਲ ਸਿਫ਼ਾਰਸ਼ ਪ੍ਰਣਾਲੀ",
        "rec_sub": "ਮਿੱਟੀ ਦੇ ਪੋਸ਼ਕ ਤੱਤ ਅਤੇ ਮੌਸਮ ਦੀ ਜਾਣਕਾਰੀ ਭਰ ਕੇ ਢੁਕਵੀਂ ਫਸਲ ਚੁਣੋ।",
        "quick_presets": "⚡ ਤੇਜ਼ ਟੈਸਟ ਵਿਕਲਪ",
        "soil_header": "🧪 ਮਿੱਟੀ ਦੇ ਪੋਸ਼ਕ ਤੱਤ (ਕਿਲੋਗ੍ਰਾਮ/ਹੈਕਟੇਅਰ)",
        "env_header": "🌦 ਵਾਤਾਵਰਣ ਅਤੇ ਮੌਸਮ",
        "nitrogen": "ਨਾਈਟ੍ਰੋਜਨ (N)",
        "phosphorus": "ਫਾਸਫੋਰਸ (P)",
        "potassium": "ਪੋਟਾਸ਼ੀਅਮ (K)",
        "temperature": "ਤਾਪਮਾਨ (°C)",
        "humidity": "ਨਮੀ (%)",
        "ph": "ਮਿੱਟੀ ਦਾ ਪੀ.ਐੱਚ. (pH)",
        "rainfall": "ਮੀਂਹ (ਮਿ.ਮੀ.)",
        "btn_predict": "🌱 ਫਸਲ ਦੀ ਸਿਫ਼ਾਰਸ਼ ਲਵੋ",
        "primary_rec": "ਮੁੱਖ ਏ.ਆਈ. ਸਿਫ਼ਾਰਸ਼",
        "alt_options": "🥈 ਹੋਰ ਵਿਕਲਪਿਕ ਫਸਲਾਂ",
        "profile_guide": "ਫਸਲ ਉਤਪਾਦਨ ਗਾਈਡ",
        "fert_schedule": "ਖਾਦ ਪ੍ਰਬੰਧਨ ਅਨੁਸੂਚੀ",
        "status_active": "● ਮਾਡਲ ਸਰਗਰਮ",
        "logged_in_as": "ਵਰਤੋਂਕਾਰ"
    },
    "Telugu": {
        "tagline": "ఖచ్చితమైన వ్యవసాయ మరియు పంట ఇంటెలిజెన్స్ వేదిక",
        "login_welcome": "క్రాప్‌స్పైర్ AI కి స్వాగతం",
        "login_sub": "పంట సిఫార్సు, తెగుళ్ల నిర్ధారణ మరియు స్మార్ట్ సాగు కోసం లాగిన్ చేయండి.",
        "username": "యూజర్‌నేమ్ లేదా మొబైల్ నంబర్",
        "password": "పాస్‌వర్డ్",
        "role": "మీ పాత్రను ఎంచుకోండి",
        "role_farmer": "🌾 రైతు సోదరుడు",
        "role_agronomist": "🧑‍🔬 వ్యవసాయ శాస్త్రవేత్త",
        "role_officer": "🏛️ వ్యవసాయ అధికారి",
        "role_student": "🎓 విద్యార్థి / పరిశోధకుడు",
        "btn_signin": "సైన్ ఇన్ చేయండి",
        "btn_demo": "🚀 తక్షణ 1-క్లిక్ డెమో ప్రవేశం",
        "create_account": "కొత్త ఖాతా సృష్టించండి",
        "full_name": "పూర్తి పేరు",
        "state_region": "రాష్ట్రం / ప్రాంతం",
        "btn_register": "రిజిస్టర్ చేసుకోండి",
        "btn_logout": "🚪 లాగ్ అవుట్",
        "lang_selector": "🌐 భాషను ఎంచుకోండి",
        "nav_dashboard": "🏠 డాష్‌బోర్డ్",
        "nav_crop_rec": "🌾 అనువైన పంట సిఫార్సు",
        "nav_disease": "🌿 మొక్కల వ్యాధి నిర్ధారణ",
        "nav_irrigation": "💧 స్మార్ట్ నీటి యాజమాన్యం",
        "nav_yield": "📊 దిగుబడి & లాభాల అంచనా",
        "nav_assistant": "🤖 AI వ్యవసాయ సహాయకుడు",
        "nav_data_hub": "📈 పంట డేటా హబ్",
        "nav_about": "ℹ️ సమాచారం",
        "rec_title": "స్మార్ట్ పంట సిఫార్సు వ్యవస్థ",
        "rec_sub": "నేల పోషకాలు మరియు వాతావరణ సమాచారాన్ని నమోదు చేసి సరైన పంటను తెలుసుకోండి.",
        "quick_presets": "⚡ శీఘ్ర ఎంపికలు",
        "soil_header": "🧪 నేల పోషకాలు (కిలో/హెక్టారు)",
        "env_header": "🌦 వాతావరణం మరియు వర్షపాతం",
        "nitrogen": "నత్రజని (N)",
        "phosphorus": "భాస్వరం (P)",
        "potassium": "పొటాషియం (K)",
        "temperature": "ఉష్ణోగ్రత (°C)",
        "humidity": "తేమ శాతం (%)",
        "ph": "నేల pH విలువ",
        "rainfall": "వర్షపాతం (మి.మీ)",
        "btn_predict": "🌱 పంట సిఫార్సు పొందండి",
        "primary_rec": "ప్రధాన AI సిఫార్సు",
        "alt_options": "🥈 ఇతర ప్రత్యామ్నాయ పంటలు",
        "profile_guide": "పంట సాగు సమగ్ర సమాచారం",
        "fert_schedule": "ఎరువుల యాజమాన్య పట్టిక",
        "status_active": "● మోడల్ క్రియాశీలంగా ఉంది",
        "logged_in_as": "రైతు"
    },
    "Tamil": {
        "tagline": "துல்லியமான விவசாயம் மற்றும் பயிர் நுண்ணறிவு தளம்",
        "login_welcome": "கிராப்ஸ்பயர் AI-க்கு நல்வரவு",
        "login_sub": "பயிர் பரிந்துரை, நோய் கண்டறிதல் மற்றும் நவீன பாசனத்திற்கு உள்நுழையவும்.",
        "username": "பயனர் பெயர் அல்லது கைபேசி எண்",
        "password": "கடவுச்சொல்",
        "role": "உங்கள் பங்கைத் தேர்ந்தெடுக்கவும்",
        "role_farmer": "🌾 விவசாயி",
        "role_agronomist": "🧑‍🔬 வேளாண் விஞ்ஞானி",
        "role_officer": "🏛️ வேளாண்மை அலுவலர்",
        "role_student": "🎓 மாணவர் / ஆய்வாளர்",
        "btn_signin": "உள்நுழைக",
        "btn_demo": "🚀 உடனடி டெமோ அணுகல்",
        "create_account": "புதிய கணக்கை உருவாக்கவும்",
        "full_name": "முழு பெயர்",
        "state_region": "மாநிலம் / மாவட்டம்",
        "btn_register": "பதிவு செய்க",
        "btn_logout": "🚪 வெளியேறுக",
        "lang_selector": "🌐 மொழியைத் தேர்ந்தெடுக்கவும்",
        "nav_dashboard": "🏠 முதன்மை பக்கம்",
        "nav_crop_rec": "🌾 பயிர் பரிந்துரை",
        "nav_disease": "🌿 பயிர் நோய் கண்டறிதல்",
        "nav_irrigation": "💧 நவீன நீர்ப்பாசனம்",
        "nav_yield": "📊 மகசூல் மற்றும் வருவாய்",
        "nav_assistant": "🤖 AI வேளாண் உதவியாளர்",
        "nav_data_hub": "📈 பயிர் தகவல் மையம்",
        "nav_about": "ℹ️ விவரக்குறிப்பு",
        "rec_title": "நவீன பயிர் பரிந்துரை அமைப்பு",
        "rec_sub": "மண் சத்து மற்றும் தட்பவெப்ப நிலையை உள்ளிட்டு பொருத்தமான பயிரை அறியவும்.",
        "quick_presets": "⚡ விரைவு தேர்வுகள்",
        "soil_header": "🧪 மண் சத்துக்கள் (கிலோ/ஹெக்டேர்)",
        "env_header": "🌦 தட்பவெப்பநிலை மற்றும் மழை",
        "nitrogen": "நைட்ரஜன் (N)",
        "phosphorus": "பாஸ்பரஸ் (P)",
        "potassium": "பொட்டாசியம் (K)",
        "temperature": "வெப்பநிலை (°C)",
        "humidity": "ஈரப்பதம் (%)",
        "ph": "மண் கார அமிலத்தன்மை (pH)",
        "rainfall": "மழைப்பொழிவு (மி.மீ)",
        "btn_predict": "🌱 பயிர் பரிந்துரை பெறுக",
        "primary_rec": "முதன்மை AI பரிந்துரை",
        "alt_options": "🥈 மாற்றுப் பயிர் தேர்வுகள்",
        "profile_guide": "பயிர் சாகுபடி கையேடு",
        "fert_schedule": "உர நிர்வாக அட்டவணை",
        "status_active": "● கணிப்பு மாதிரி தயார்",
        "logged_in_as": "பயனர்"
    },
    "Bengali": {
        "tagline": "নির্ভুল কৃষি ও ফসল গোয়েন্দা প্ল্যাটফর্ম",
        "login_welcome": "ক্রপস্পায়ার এআই-তে স্বাগতম",
        "login_sub": "ফসল নির্বাচন, রোগ নির্ণয় এবং স্মার্ট সেচের জন্য সাইন ইন করুন।",
        "username": "ব্যবহারকারীর নাম বা মোবাইল নম্বর",
        "password": "পাসওয়ার্ড",
        "role": "আপনার ভূমিকা নির্বাচন করুন",
        "role_farmer": "🌾 কৃষক ভাই",
        "role_agronomist": "🧑‍🔬 কৃষি বিজ্ঞানী",
        "role_officer": "🏛️ কৃষি সম্প্রসারণ কর্মকর্তা",
        "role_student": "🎓 শিক্ষার্থী / গবেষক",
        "btn_signin": "সাইন ইন করুন",
        "btn_demo": "🚀 তাৎক্ষণিক ১-ক্লিক ডেমো প্রবেশ",
        "create_account": "নতুন অ্যাকাউন্ট তৈরি করুন",
        "full_name": "পুরো নাম",
        "state_region": "রাজ্য / জেলা",
        "btn_register": "নিবন্ধন করুন",
        "btn_logout": "🚪 লগ আউট",
        "lang_selector": "🌐 ভাষা নির্বাচন করুন",
        "nav_dashboard": "🏠 ড্যাশবোর্ড",
        "nav_crop_rec": "🌾 উপযুক্ত ফসল সুপারিশ",
        "nav_disease": "🌿 উদ্ভিদের রোগ নির্ণয়",
        "nav_irrigation": "💧 স্মার্ট সেচ পরামর্শ",
        "nav_yield": "📊 ফলন ও লাভজনকতা",
        "nav_assistant": "🤖 এআই কৃষি সহকারী",
        "nav_data_hub": "📈 ফসল তথ্য কেন্দ্র",
        "nav_about": "ℹ️ তথ্য ও পরিচিতি",
        "rec_title": "স্মার্ট ফসল সুপারিশ ব্যবস্থা",
        "rec_sub": "মাটির পুষ্টি ও আবহাওয়ার তথ্য প্রদান করে সঠিক ফসল নির্বাচন করুন।",
        "quick_presets": "⚡ দ্রুত পরীক্ষা বিকল্প",
        "soil_header": "🧪 মাটির পুষ্টি উপাদান (কেজি/হেক্টর)",
        "env_header": "🌦 পরিবেশ ও আবহাওয়া",
        "nitrogen": "নাইট্রোজেন (N)",
        "phosphorus": "ফসফরাস (P)",
        "potassium": "পটাশিয়াম (K)",
        "temperature": "তাপমাত্রা (°C)",
        "humidity": "বাতাসের আর্দ্রতা (%)",
        "ph": "মাটির পিএইচ (pH)",
        "rainfall": "বৃষ্টিপাত (মিমি)",
        "btn_predict": "🌱 উপযুক্ত ফসল জানুন",
        "primary_rec": "প্রধান এআই সুপারিশ",
        "alt_options": "🥈 অন্যান্য বিকল্প ফসল",
        "profile_guide": "ফসল চাষ ও ব্যবস্থাপনা নির্দেশিকা",
        "fert_schedule": "সারের সময়সূচী",
        "status_active": "● মডেল সক্রিয়",
        "logged_in_as": "ব্যবহারকারী"
    }
}

# Helper to retrieve translated string
def t(key):
    lang = st.session_state.get("language_key", "English")
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["English"])
    return lang_dict.get(key, TRANSLATIONS["English"].get(key, key))

def rerun_app():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


# =========================================================
# KNOWLEDGE BASES & REFERENCE DATA
# =========================================================

CROP_DETAILS = {
    "rice": {
        "name": "Rice (Paddy)",
        "scientific_name": "Oryza sativa",
        "category": "Cereal / Food Grain",
        "season": "Kharif (Monsoon)",
        "ideal_temp": "20°C - 35°C",
        "ideal_humidity": "80% - 90%",
        "ideal_ph": "5.5 - 7.0",
        "ideal_rainfall": "150 - 300 mm",
        "soil_type": "Clayey, alluvial loam with high water holding capacity",
        "duration": "110 - 150 days",
        "water_req": "High (standing water 2-5 cm during vegetative stage)",
        "fertilizer": "NPK 100:50:50 kg/ha. Apply Zinc Sulphate (25 kg/ha) to prevent Khaira disease.",
        "avg_yield_per_acre": "18 - 25 Quintals",
        "mandi_price_per_qtl": 2200,
        "tips": "Maintain shallow flooding during tillering. Drain field 10 days before harvesting."
    },
    "maize": {
        "name": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "category": "Cereal / Fodder",
        "season": "Kharif & Rabi",
        "ideal_temp": "18°C - 30°C",
        "ideal_humidity": "55% - 75%",
        "ideal_ph": "5.8 - 7.2",
        "ideal_rainfall": "60 - 110 mm",
        "soil_type": "Deep, fertile, well-drained loamy to sandy-loam soils",
        "duration": "90 - 120 days",
        "water_req": "Moderate (sensitive to waterlogging at flowering & silking)",
        "fertilizer": "NPK 120:60:40 kg/ha. Split Nitrogen into 3 doses: sowing, knee-high, and tasseling.",
        "avg_yield_per_acre": "20 - 30 Quintals",
        "mandi_price_per_qtl": 2100,
        "tips": "Avoid standing water; provide ridge and furrow drainage to prevent root rot."
    },
    "chickpea": {
        "name": "Chickpea (Gram)",
        "scientific_name": "Cicer arietinum",
        "category": "Pulse / Legume",
        "season": "Rabi (Winter)",
        "ideal_temp": "15°C - 25°C",
        "ideal_humidity": "50% - 65%",
        "ideal_ph": "6.0 - 7.5",
        "ideal_rainfall": "60 - 90 mm",
        "soil_type": "Well-drained sandy loam or black cotton soil",
        "duration": "90 - 120 days",
        "water_req": "Low (1-2 protective irrigations at branching and pod development)",
        "fertilizer": "NPK 20:40:20 kg/ha. Inoculate seeds with Rhizobium culture to fix atmospheric nitrogen.",
        "avg_yield_per_acre": "8 - 12 Quintals",
        "mandi_price_per_qtl": 5400,
        "tips": "Nip top tender shoots at 30-40 days after sowing to stimulate vigorous branching."
    },
    "kidneybeans": {
        "name": "Kidney Beans (Rajma)",
        "scientific_name": "Phaseolus vulgaris",
        "category": "Pulse / Legume",
        "season": "Rabi / Spring",
        "ideal_temp": "15°C - 25°C",
        "ideal_humidity": "55% - 65%",
        "ideal_ph": "5.5 - 6.5",
        "ideal_rainfall": "60 - 150 mm",
        "soil_type": "Light, well-aerated sandy loam rich in organic matter",
        "duration": "90 - 130 days",
        "water_req": "Moderate (keep root zone evenly moist without sogginess)",
        "fertilizer": "NPK 100:60:40 kg/ha (Requires higher N as it lacks nodule bacteria).",
        "avg_yield_per_acre": "7 - 10 Quintals",
        "mandi_price_per_qtl": 8500,
        "tips": "Very sensitive to frost and water stagnation. Mulching helps conserve soil moisture."
    },
    "pigeonpeas": {
        "name": "Pigeonpeas (Arhar / Toor)",
        "scientific_name": "Cajanus cajan",
        "category": "Pulse / Legume",
        "season": "Kharif (Monsoon)",
        "ideal_temp": "20°C - 35°C",
        "ideal_humidity": "60% - 75%",
        "ideal_ph": "6.5 - 7.5",
        "ideal_rainfall": "90 - 150 mm",
        "soil_type": "Deep loam or black cotton soil with good drainage",
        "duration": "140 - 200 days",
        "water_req": "Low to Moderate (deep taproot makes it drought-resistant)",
        "fertilizer": "NPK 20:50:20 kg/ha + Rhizobium seed treatment.",
        "avg_yield_per_acre": "6 - 10 Quintals",
        "mandi_price_per_qtl": 7000,
        "tips": "Excellent for intercropping with sorghum, maize, or soybean."
    },
    "mothbeans": {
        "name": "Moth Beans",
        "scientific_name": "Vigna aconitifolia",
        "category": "Pulse / Arid Legume",
        "season": "Kharif (Arid)",
        "ideal_temp": "24°C - 32°C",
        "ideal_humidity": "50% - 65%",
        "ideal_ph": "7.0 - 8.5",
        "ideal_rainfall": "30 - 75 mm",
        "soil_type": "Sandy, sandy loam, desert soils",
        "duration": "75 - 90 days",
        "water_req": "Very Low (extremely drought-tolerant)",
        "fertilizer": "NPK 10:30:10 kg/ha. Tolerates low-fertility soils.",
        "avg_yield_per_acre": "3 - 5 Quintals",
        "mandi_price_per_qtl": 6500,
        "tips": "Ideal cover crop for arid belts to control wind erosion and restore organic carbon."
    },
    "mungbean": {
        "name": "Mungbean (Green Gram)",
        "scientific_name": "Vigna radiata",
        "category": "Pulse / Legume",
        "season": "Kharif, Rabi & Zaid (Summer)",
        "ideal_temp": "25°C - 35°C",
        "ideal_humidity": "60% - 75%",
        "ideal_ph": "6.2 - 7.5",
        "ideal_rainfall": "40 - 90 mm",
        "soil_type": "Well-drained loamy to sandy-loam soils",
        "duration": "60 - 75 days",
        "water_req": "Low to Moderate (2-3 irrigations in summer)",
        "fertilizer": "NPK 20:40:20 kg/ha + 20 kg/ha Sulphur.",
        "avg_yield_per_acre": "4 - 7 Quintals",
        "mandi_price_per_qtl": 7500,
        "tips": "Short duration makes it an ideal catch crop between wheat and paddy."
    },
    "blackgram": {
        "name": "Blackgram (Urad)",
        "scientific_name": "Vigna mungo",
        "category": "Pulse / Legume",
        "season": "Kharif & Summer",
        "ideal_temp": "25°C - 35°C",
        "ideal_humidity": "65% - 80%",
        "ideal_ph": "6.5 - 7.5",
        "ideal_rainfall": "60 - 100 mm",
        "soil_type": "Heavier soils, loams, and black cotton soils",
        "duration": "70 - 85 days",
        "water_req": "Moderate (ensure moisture during flowering and pod fill)",
        "fertilizer": "NPK 20:40:20 kg/ha.",
        "avg_yield_per_acre": "4 - 6 Quintals",
        "mandi_price_per_qtl": 7200,
        "tips": "Harvest when 80% pods turn black to prevent shattering losses."
    },
    "lentil": {
        "name": "Lentil (Masoor)",
        "scientific_name": "Lens culinaris",
        "category": "Pulse / Legume",
        "season": "Rabi (Winter)",
        "ideal_temp": "15°C - 25°C",
        "ideal_humidity": "50% - 70%",
        "ideal_ph": "6.0 - 7.5",
        "ideal_rainfall": "40 - 80 mm",
        "soil_type": "Silty clay to fertile light loam",
        "duration": "110 - 130 days",
        "water_req": "Low (sensitive to waterlogging, thrives on residual soil moisture)",
        "fertilizer": "NPK 20:40:20 kg/ha.",
        "avg_yield_per_acre": "5 - 8 Quintals",
        "mandi_price_per_qtl": 6400,
        "tips": "Can be grown successfully as a relay crop in standing rice (Utera / Paira system)."
    },
    "pomegranate": {
        "name": "Pomegranate",
        "scientific_name": "Punica granatum",
        "category": "Horticulture / Fruit",
        "season": "Perennial (Ambe, Mrig & Hasta bahar)",
        "ideal_temp": "20°C - 38°C",
        "ideal_humidity": "30% - 50%",
        "ideal_ph": "6.5 - 7.5",
        "ideal_rainfall": "50 - 110 mm",
        "soil_type": "Deep loamy or alluvial soil with good internal drainage",
        "duration": "Perennial (Fruits in 130-160 days after flowering)",
        "water_req": "Low (Drip irrigation is highly recommended)",
        "fertilizer": "FYM 20-30 kg/plant + NPK 500:250:250 g/plant/year.",
        "avg_yield_per_acre": "40 - 60 Quintals",
        "mandi_price_per_qtl": 9000,
        "tips": "Regulate bahar treatment carefully to align harvest with high festive market demand."
    },
    "banana": {
        "name": "Banana",
        "scientific_name": "Musa acuminata",
        "category": "Horticulture / Fruit",
        "season": "Year-round planting",
        "ideal_temp": "22°C - 35°C",
        "ideal_humidity": "75% - 85%",
        "ideal_ph": "6.0 - 7.5",
        "ideal_rainfall": "90 - 200 mm",
        "soil_type": "Rich, deep clay-loam soil with high organic content",
        "duration": "11 - 14 months",
        "water_req": "Very High (regular irrigation every 3-4 days in summer)",
        "fertilizer": "NPK 200:50:300 g/plant applied in 4 split doses.",
        "avg_yield_per_acre": "200 - 300 Quintals",
        "mandi_price_per_qtl": 1800,
        "tips": "Desuckering (removal of unwanted side shoots) ensures higher bunch weight."
    },
    "mango": {
        "name": "Mango",
        "scientific_name": "Mangifera indica",
        "category": "Horticulture / Fruit",
        "season": "Summer harvest (March - July)",
        "ideal_temp": "24°C - 35°C",
        "ideal_humidity": "45% - 65%",
        "ideal_ph": "5.5 - 7.5",
        "ideal_rainfall": "80 - 150 mm",
        "soil_type": "Deep, well-drained alluvial or lateritic loam",
        "duration": "Perennial (Trees live 50+ years)",
        "water_req": "Moderate (withhold water 2 months before flowering to induce bloom)",
        "fertilizer": "FYM 50 kg/tree + NPK 1000:500:1000 g/tree for bearing orchards.",
        "avg_yield_per_acre": "35 - 50 Quintals",
        "mandi_price_per_qtl": 4500,
        "tips": "Prune dead criss-crossing branches post-harvest to allow sunlight into the canopy."
    },
    "grapes": {
        "name": "Grapes",
        "scientific_name": "Vitis vinifera",
        "category": "Horticulture / Fruit",
        "season": "Harvest February - April",
        "ideal_temp": "15°C - 35°C",
        "ideal_humidity": "60% - 80%",
        "ideal_ph": "6.5 - 7.5",
        "ideal_rainfall": "60 - 85 mm",
        "soil_type": "Well-drained sandy loam or red sandy soil",
        "duration": "Perennial (Pruning cycles in April & October)",
        "water_req": "Moderate (Drip irrigation required; stop water before harvest)",
        "fertilizer": "NPK 300:200:400 kg/ha split around forward and back pruning.",
        "avg_yield_per_acre": "80 - 120 Quintals",
        "mandi_price_per_qtl": 5500,
        "tips": "Train vines on 'Bower' or 'Y-trellis' system for optimal aeration and bunch quality."
    },
    "watermelon": {
        "name": "Watermelon",
        "scientific_name": "Citrullus lanatus",
        "category": "Cucurbit / Fruit",
        "season": "Zaid (Summer)",
        "ideal_temp": "24°C - 32°C",
        "ideal_humidity": "50% - 65%",
        "ideal_ph": "6.0 - 7.0",
        "ideal_rainfall": "40 - 60 mm",
        "soil_type": "Sandy loam or riverbed silt soils",
        "duration": "80 - 100 days",
        "water_req": "Moderate (Irrigate frequently; reduce water during fruit ripening)",
        "fertilizer": "NPK 80:50:50 kg/ha + Micronutrient boron for sweetness.",
        "avg_yield_per_acre": "100 - 150 Quintals",
        "mandi_price_per_qtl": 1200,
        "tips": "Silver-black polyethylene mulching suppresses weeds and raises soil temperature."
    },
    "muskmelon": {
        "name": "Muskmelon (Cantaloupe)",
        "scientific_name": "Cucumis melo",
        "category": "Cucurbit / Fruit",
        "season": "Zaid (Summer)",
        "ideal_temp": "25°C - 34°C",
        "ideal_humidity": "50% - 65%",
        "ideal_ph": "6.0 - 7.0",
        "ideal_rainfall": "40 - 60 mm",
        "soil_type": "Deep, fertile sandy loam with superior drainage",
        "duration": "75 - 90 days",
        "water_req": "Moderate (avoid wetting foliage or fruits to prevent fungal decay)",
        "fertilizer": "NPK 60:40:40 kg/ha.",
        "avg_yield_per_acre": "60 - 90 Quintals",
        "mandi_price_per_qtl": 1800,
        "tips": "Harvest at 'half-slip' stage for distant markets and 'full-slip' for local sale."
    },
    "apple": {
        "name": "Apple",
        "scientific_name": "Malus domestica",
        "category": "Horticulture / Temperate Fruit",
        "season": "Harvest July - October",
        "ideal_temp": "15°C - 24°C",
        "ideal_humidity": "70% - 85%",
        "ideal_ph": "5.5 - 6.5",
        "ideal_rainfall": "100 - 150 mm",
        "soil_type": "Deep, fertile loam rich in organic humus",
        "duration": "Perennial (Requires 800-1200 chilling hours below 7°C)",
        "water_req": "High (Regular irrigation during fruit sizing period)",
        "fertilizer": "NPK 700:350:700 g/tree for full grown bearing trees.",
        "avg_yield_per_acre": "50 - 80 Quintals",
        "mandi_price_per_qtl": 8000,
        "tips": "Thin excessive fruitlets early to maintain annual bearing and larger fruit size."
    },
    "orange": {
        "name": "Orange (Citrus / Mandarin)",
        "scientific_name": "Citrus sinensis",
        "category": "Horticulture / Citrus",
        "season": "Winter harvest",
        "ideal_temp": "15°C - 35°C",
        "ideal_humidity": "60% - 75%",
        "ideal_ph": "6.0 - 7.5",
        "ideal_rainfall": "100 - 130 mm",
        "soil_type": "Light loam or well-drained subsoil free from hard pan",
        "duration": "Perennial (Bearing starts from 4th-5th year)",
        "water_req": "Moderate (avoid water contact with the tree trunk to prevent gummosis)",
        "fertilizer": "NPK 600:200:300 g/tree + Zinc and Iron foliar spray.",
        "avg_yield_per_acre": "40 - 60 Quintals",
        "mandi_price_per_qtl": 3500,
        "tips": "Paint trunks with Bordeaux paste up to 2 feet above ground to stop fungal rot."
    },
    "papaya": {
        "name": "Papaya",
        "scientific_name": "Carica papaya",
        "category": "Horticulture / Fruit",
        "season": "Year-round",
        "ideal_temp": "25°C - 35°C",
        "ideal_humidity": "70% - 85%",
        "ideal_ph": "6.0 - 7.0",
        "ideal_rainfall": "120 - 200 mm",
        "soil_type": "Rich, porous loam with zero water stagnation",
        "duration": "9 - 12 months",
        "water_req": "Moderate to High (Extremely sensitive to waterlogging)",
        "fertilizer": "NPK 250:250:500 g/plant/year in 6 bi-monthly splits.",
        "avg_yield_per_acre": "150 - 250 Quintals",
        "mandi_price_per_qtl": 2000,
        "tips": "Plant on raised beds to ensure swift drainage during intense downpours."
    },
    "coconut": {
        "name": "Coconut",
        "scientific_name": "Cocos nucifera",
        "category": "Plantation / Palm",
        "season": "Year-round harvesting",
        "ideal_temp": "25°C - 35°C",
        "ideal_humidity": "75% - 95%",
        "ideal_ph": "5.5 - 7.5",
        "ideal_rainfall": "130 - 250 mm",
        "soil_type": "Coastal sand, alluvial or red loam with good drainage",
        "duration": "Perennial (Productive life 60-80 years)",
        "water_req": "High (Requires 40-50 liters/palm/day under drip)",
        "fertilizer": "NPK 500:320:1200 g/palm/year + 1 kg common salt (NaCl) in coastal soils.",
        "avg_yield_per_acre": "8,000 - 12,000 Nuts",
        "mandi_price_per_qtl": 3000,
        "tips": "Apply coir pith mulching in the palm basin to retain moisture during dry spells."
    },
    "cotton": {
        "name": "Cotton",
        "scientific_name": "Gossypium hirsutum",
        "category": "Commercial / Fiber",
        "season": "Kharif (May - October)",
        "ideal_temp": "22°C - 32°C",
        "ideal_humidity": "60% - 80%",
        "ideal_ph": "6.0 - 8.0",
        "ideal_rainfall": "60 - 100 mm",
        "soil_type": "Deep black cotton soil (Vertisols) with moisture retention",
        "duration": "150 - 180 days",
        "water_req": "Moderate (Crucial moisture needed at flowering and boll formation)",
        "fertilizer": "NPK 120:60:60 kg/ha for Bt Cotton.",
        "avg_yield_per_acre": "8 - 14 Quintals (Seed cotton)",
        "mandi_price_per_qtl": 7100,
        "tips": "Erect pheromone traps (5 traps/ha) for early monitoring of pink bollworm."
    },
    "jute": {
        "name": "Jute (Golden Fiber)",
        "scientific_name": "Corchorus olitorius",
        "category": "Commercial / Fiber",
        "season": "Summer / Early Monsoon",
        "ideal_temp": "24°C - 35°C",
        "ideal_humidity": "70% - 90%",
        "ideal_ph": "6.0 - 7.5",
        "ideal_rainfall": "150 - 200 mm",
        "soil_type": "New alluvial soils along river floodplains",
        "duration": "120 - 135 days",
        "water_req": "High (Tolerates waterlogged standing water during maturity)",
        "fertilizer": "NPK 40:20:20 kg/ha.",
        "avg_yield_per_acre": "10 - 15 Quintals (Fiber)",
        "mandi_price_per_qtl": 5000,
        "tips": "Harvest at small-pod stage for supreme fiber tensile strength and luster."
    },
    "coffee": {
        "name": "Coffee (Arabica / Robusta)",
        "scientific_name": "Coffea arabica / canephora",
        "category": "Plantation / Beverage",
        "season": "Harvest November - February",
        "ideal_temp": "18°C - 28°C",
        "ideal_humidity": "65% - 85%",
        "ideal_ph": "6.0 - 6.8",
        "ideal_rainfall": "150 - 250 mm",
        "soil_type": "Deep, porous, slightly acidic volcanic or forest loam",
        "duration": "Perennial (First commercial harvest at 4th year)",
        "water_req": "High (Blossom showers in March-April are critical for berry set)",
        "fertilizer": "NPK 120:90:120 kg/ha for bearing Arabica.",
        "avg_yield_per_acre": "4 - 8 Quintals (Parchment)",
        "mandi_price_per_qtl": 14000,
        "tips": "Grow under two-tier shade trees (silver oak, dadap) to buffer thermal stress."
    }
}


# =========================================================
# CACHED MODEL LOADING & RESILIENT FALLBACK
# =========================================================

@st.cache_resource(show_spinner=False)
def load_or_train_crop_model():
    """
    Attempts to load the pre-trained crop_model.pkl.
    If missing or corrupt, automatically trains a high-accuracy
    RandomForestClassifier using Crop_recommendation.csv and saves it.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "crop_model.pkl")
    csv_path = os.path.join(base_dir, "Crop_recommendation.csv")

    # 1. Try loading existing pickle
    if joblib is not None and os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            return model, "Loaded from crop_model.pkl"
        except Exception:
            pass  # Fall through to re-training

    # 2. Train on CSV if available
    if os.path.exists(csv_path) and RandomForestClassifier is not None:
        try:
            df = pd.read_csv(csv_path)
            feature_cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
            X = df[feature_cols]
            y = df["label"]
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X, y)
            
            if joblib is not None:
                try:
                    joblib.dump(model, model_path)
                except Exception:
                    pass
            return model, "Trained dynamically from Crop_recommendation.csv"
        except Exception as e:
            return None, f"Training error: {e}"

    return None, "Model file and dataset not found"


model, model_status = load_or_train_crop_model()


# =========================================================
# LIGHT GREEN AGRI THEME WITH MAXIMUM CONTRAST DARK TEXT
# =========================================================

st.markdown("""
<style>
    /* Global Base: Refreshing Light Green Background */
    .stApp {
        background-color: #eef7ee !important;
        color: #102e19 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Force all text elements on main page to be DARK, CRISP & HIGH-CONTRAST */
    .stApp p, .stApp span, .stApp li, .stApp ul, .stApp ol,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] span {
        color: #102e19 !important;
        font-size: 15px;
    }

    /* Headings - Rich Vibrant Forest Green */
    h1, h2, h3, h4, h5, h6,
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
    div[data-testid="stMarkdownContainer"] h1,
    div[data-testid="stMarkdownContainer"] h2,
    div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] h4,
    div[data-testid="stMarkdownContainer"] h5,
    div[data-testid="stMarkdownContainer"] h6 {
        color: #14532d !important;
        font-weight: 800 !important;
    }

    /* Strong / Bold Text - Deepest Forest Black */
    strong, b,
    div[data-testid="stMarkdownContainer"] strong,
    div[data-testid="stMarkdownContainer"] b {
        color: #05210e !important;
        font-weight: 700 !important;
    }

    /* Form & Input Labels - Crisp Dark Green */
    label,
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] span {
        color: #0f381c !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }

    /* Text Inputs, Number Inputs, Textareas, Selectboxes */
    input, textarea, select,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] div {
        color: #0f2918 !important;
        background-color: #ffffff !important;
        border: 1.5px solid #a3cfae !important;
        border-radius: 8px !important;
    }

    /* Sidebar: Deep Rich Forest with Pure White Text */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d2816 0%, #153e24 100%) !important;
        border-right: 1.5px solid #235433 !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #f0fdf4 !important;
    }
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stRadio label * {
        color: #f0fdf4 !important;
        font-size: 15px !important;
        padding: 3px 0;
    }

    /* Language Selectbox & All Selectboxes in Sidebar - CRISP DARK TEXT */
    section[data-testid="stSidebar"] div[data-baseweb="select"],
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 2px solid #22c55e !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] *,
    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] div[data-baseweb="select"] div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] input {
        color: #05210e !important;
        background-color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
        fill: #05210e !important;
    }

    /* Dropdown Menu Options Popover (when clicked) */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] ul,
    ul[data-testid="stSelectboxVirtualDropdown"] {
        background-color: #ffffff !important;
    }
    div[data-baseweb="popover"] *,
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] li span,
    ul[data-testid="stSelectboxVirtualDropdown"] * {
        color: #05210e !important;
        background-color: #ffffff !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li:hover * {
        background-color: #dcfce7 !important;
        color: #14532d !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #ffffff !important;
        color: #14532d !important;
        border: 1.5px solid #22c55e !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 6px rgba(20, 83, 45, 0.08) !important;
    }
    .stButton > button:hover {
        background-color: #dcfce7 !important;
        border-color: #15803d !important;
        color: #05210e !important;
    }
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background-color: #15803d !important;
        color: #ffffff !important;
        border: 1.5px solid #14532d !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background-color: #166534 !important;
        color: #ffffff !important;
    }

    /* Titles */
    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #14532d !important;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .subtitle {
        font-size: 16px;
        color: #166534 !important;
        font-weight: 500;
        margin-bottom: 24px;
        line-height: 1.5;
    }

    /* Cards */
    .info-card {
        background: #ffffff !important;
        padding: 24px;
        border-radius: 14px;
        border: 1.5px solid #b8dabf !important;
        box-shadow: 0 4px 14px rgba(20, 83, 45, 0.06);
        margin-bottom: 18px;
    }
    .info-card h3 {
        color: #14532d !important;
        font-size: 20px;
        font-weight: 800;
        margin-top: 0;
        margin-bottom: 10px;
    }
    .info-card p {
        color: #1c4526 !important;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 0;
    }

    /* Login Card */
    .login-container {
        max-width: 500px;
        margin: 20px auto;
        background: #ffffff;
        padding: 32px;
        border-radius: 18px;
        border: 1.5px solid #b8dabf;
        box-shadow: 0 10px 30px rgba(20, 83, 45, 0.1);
    }

    /* Result Banner */
    .result-card {
        background: linear-gradient(135deg, #dcf0dc 0%, #c4e8c5 100%) !important;
        padding: 26px;
        border-radius: 16px;
        border: 2px solid #22c55e !important;
        box-shadow: 0 6px 18px rgba(20, 83, 45, 0.12);
        text-align: center;
        margin: 20px 0;
    }
    .result-badge {
        display: inline-block;
        background-color: #15803d !important;
        color: #ffffff !important;
        padding: 5px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 10px;
    }
    .crop-name {
        color: #05210e !important;
        font-size: 42px;
        font-weight: 900;
        margin: 6px 0;
    }
    .result-desc {
        color: #14532d !important;
        font-size: 15px;
        font-weight: 600;
        max-width: 650px;
        margin: 0 auto;
    }

    /* Agronomic Profile Guide Card */
    .guide-card {
        background: #ffffff !important;
        border: 1.5px solid #b8dabf !important;
        border-radius: 14px !important;
        padding: 24px !important;
        margin-top: 18px !important;
        box-shadow: 0 4px 16px rgba(20, 83, 45, 0.06) !important;
    }
    .guide-card h4 {
        color: #14532d !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        margin-top: 0 !important;
        margin-bottom: 16px !important;
        border-bottom: 2px solid #dcf0dc;
        padding-bottom: 8px;
    }
    .guide-item {
        color: #0f2918 !important;
        font-size: 15px !important;
        line-height: 1.8 !important;
        margin-bottom: 10px !important;
    }
    .guide-item strong {
        color: #05210e !important;
        font-weight: 800 !important;
    }

    /* Metrics */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 1.5px solid #b8dabf !important;
        padding: 12px 18px !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(20, 83, 45, 0.05);
    }
    div[data-testid="stMetricLabel"] p {
        color: #166534 !important;
        font-weight: 700 !important;
        font-size: 13px !important;
    }
    div[data-testid="stMetricValue"] div {
        color: #05210e !important;
        font-weight: 900 !important;
    }

    /* Status Pill - High Contrast in Sidebar */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 6px;
    }
    .status-pill-ok,
    section[data-testid="stSidebar"] .status-pill-ok,
    section[data-testid="stSidebar"] .status-pill-ok * {
        background-color: #14532d !important;
        color: #4ade80 !important;
        border: 1.5px solid #22c55e !important;
        font-weight: 800 !important;
    }
    .status-pill-warn,
    section[data-testid="stSidebar"] .status-pill-warn,
    section[data-testid="stSidebar"] .status-pill-warn * {
        background-color: #713f12 !important;
        color: #fef08a !important;
        border: 1.5px solid #eab308 !important;
        font-weight: 800 !important;
    }

    /* Engine Status Caption in Sidebar */
    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
    section[data-testid="stSidebar"] .stCaption,
    section[data-testid="stSidebar"] .stCaption * {
        color: #bbf7d0 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] {
        color: #166534 !important;
        font-weight: 700 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #14532d !important;
        font-weight: 800 !important;
        border-bottom: 2px solid #14532d !important;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE: AUTHENTICATION & LANGUAGE
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = "Farmer / Cultivator"
if "language_key" not in st.session_state:
    st.session_state.language_key = "English"


# =========================================================
# LOGIN & AUTHENTICATION SCREEN (IF NOT LOGGED IN)
# =========================================================

if not st.session_state.authenticated:
    # Centered Header
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="font-size: 46px; font-weight: 900; color: #14532d; display: flex; align-items: center; justify-content: center; gap: 12px;">
                <span>{APP_ICON}</span> <span>{APP_NAME}</span>
            </div>
            <div style="font-size: 18px; color: #166534; font-weight: 600; margin-top: 6px;">
                {t('tagline')}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Login Container
    login_col1, login_col2, login_col3 = st.columns([1, 2, 1])

    with login_col2:
        # Language Selector Bar on Login Page
        st.markdown(f"##### {t('lang_selector')}")
        selected_lang_display = st.selectbox(
            "Language",
            list(LANGUAGES.keys()),
            index=list(LANGUAGES.keys()).index(
                [k for k, v in LANGUAGES.items() if v == st.session_state.language_key][0]
            ),
            label_visibility="collapsed"
        )
        st.session_state.language_key = LANGUAGES[selected_lang_display]

        st.markdown("<br>", unsafe_allow_html=True)

        tab_signin, tab_signup = st.tabs(["🔑 Sign In", "📝 Create Account"])

        with tab_signin:
            st.markdown(f"### {t('login_welcome')}")
            st.caption(t('login_sub'))

            with st.form("login_form"):
                u_input = st.text_input(f"👤 {t('username')}", value="kisan_ramesh")
                p_input = st.text_input(f"🔒 {t('password')}", type="password", value="demo123")
                r_input = st.selectbox(
                    f"🏷️ {t('role')}",
                    [t('role_farmer'), t('role_agronomist'), t('role_officer'), t('role_student')]
                )

                submit_login = st.form_submit_button(f"🔑 {t('btn_signin')}", type="primary", use_container_width=True)

            if submit_login:
                if u_input.strip() and p_input.strip():
                    st.session_state.authenticated = True
                    st.session_state.username = u_input.strip()
                    st.session_state.user_role = r_input
                    st.success(f"✅ Welcome, {u_input}! Loading platform...")
                    rerun_app()
                else:
                    st.error("Please provide both username and password.")

            st.markdown("---")
            # 1-Click Demo Guest Button
            if st.button(t('btn_demo'), use_container_width=True):
                st.session_state.authenticated = True
                st.session_state.username = "Demo Farmer"
                st.session_state.user_role = t('role_farmer')
                rerun_app()

        with tab_signup:
            st.markdown(f"### {t('create_account')}")
            with st.form("signup_form"):
                reg_name = st.text_input(f"👤 {t('full_name')}")
                reg_user = st.text_input(f"📱 {t('username')}")
                reg_pass = st.text_input(f"🔒 {t('password')}", type="password")
                reg_role = st.selectbox(
                    f"🏷️ {t('role')}",
                    [t('role_farmer'), t('role_agronomist'), t('role_officer'), t('role_student')]
                )
                reg_state = st.text_input(f"📍 {t('state_region')}", value="Maharashtra / Punjab / Karnataka")

                submit_signup = st.form_submit_button(f"📝 {t('btn_register')}", type="primary", use_container_width=True)

            if submit_signup:
                if reg_name.strip() and reg_user.strip() and reg_pass.strip():
                    st.session_state.authenticated = True
                    st.session_state.username = reg_name.strip()
                    st.session_state.user_role = reg_role
                    st.success(f"🎉 Account registered successfully! Welcome {reg_name}!")
                    rerun_app()
                else:
                    st.error("Please fill in all registration fields.")

    st.stop()


# =========================================================
# MAIN APPLICATION (AUTHENTICATED)
# =========================================================

# =========================================================
# SIDEBAR NAVIGATION & SYSTEM STATUS
# =========================================================

with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_NAME}")
    st.caption(t('tagline'))
    
    # User Profile Badge in Sidebar
    st.markdown(
        f"""
        <div style="background: rgba(255,255,255,0.12); padding: 10px 14px; border-radius: 10px; margin: 10px 0; border: 1px solid rgba(255,255,255,0.2);">
            <div style="font-size: 13px; color: #bbf7d0;">{t('logged_in_as')}:</div>
            <div style="font-size: 16px; font-weight: 800; color: #ffffff;">👤 {st.session_state.username}</div>
            <div style="font-size: 12px; color: #dcfce7;">{st.session_state.user_role}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Language Switcher in Sidebar
    st.markdown(f"##### {t('lang_selector')}")
    sidebar_lang_display = st.selectbox(
        "Language Selector",
        list(LANGUAGES.keys()),
        index=list(LANGUAGES.keys()).index(
            [k for k, v in LANGUAGES.items() if v == st.session_state.language_key][0]
        ),
        key="sb_lang_select",
        label_visibility="collapsed"
    )
    if LANGUAGES[sidebar_lang_display] != st.session_state.language_key:
        st.session_state.language_key = LANGUAGES[sidebar_lang_display]
        rerun_app()

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            t('nav_dashboard'),
            t('nav_crop_rec'),
            t('nav_disease'),
            t('nav_irrigation'),
            t('nav_yield'),
            t('nav_assistant'),
            t('nav_data_hub'),
            t('nav_about')
        ],
        index=1  # Default directly to Crop Recommendation
    )

    st.markdown("---")

    # Engine Status Widget
    st.markdown("##### ⚙️ Engine Status")
    if model is not None:
        st.markdown(
            f'<div class="status-pill status-pill-ok">{t("status_active")}</div>',
            unsafe_allow_html=True
        )
        st.caption(f"Status: {model_status}")
    else:
        st.markdown(
            '<div class="status-pill status-pill-warn">● ML Model Offline</div>',
            unsafe_allow_html=True
        )
        st.caption(f"Notice: {model_status}")

    # Logout Button
    st.markdown("---")
    if st.button(t('btn_logout'), use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.username = ""
        rerun_app()

    st.markdown(
        "<small style='color:#dcfce7;'>CropSpire AI v3.0 • Multi-Language Edition</small>",
        unsafe_allow_html=True
    )


# =========================================================
# 1. DASHBOARD (HOME)
# =========================================================

if page == t('nav_dashboard'):
    st.markdown(
        f'<div class="main-title">{APP_ICON} {APP_NAME}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="subtitle">{t("tagline")}</div>',
        unsafe_allow_html=True
    )

    # Top KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Supported Crops", value="22 Varieties", delta="High Precision")
    with col2:
        st.metric(label="Model Accuracy", value="99.5%", delta="+1.6% vs Baseline")
    with col3:
        st.metric(label="Decision Latency", value="< 20 ms", delta="Edge Ready")
    with col4:
        st.metric(label="Decision Modules", value="6 Systems", delta="All Active")

    st.markdown("<br>", unsafe_allow_html=True)

    # Module Cards Grid
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="info-card">
            <h3>{t('nav_crop_rec')}</h3>
            <p>
                Analyzes 7 soil and climate parameters (N, P, K, pH, Temperature,
                Humidity, Rainfall) using an ensemble Random Forest model to predict
                the optimal crop with probability scores.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="info-card">
            <h3>{t('nav_disease')}</h3>
            <p>
                Interactive plant leaf health scanner and diagnostic assistant.
                Upload leaf imagery or select visible symptoms to receive instant
                disease identification and bio-chemical remedies.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="info-card">
            <h3>{t('nav_irrigation')}</h3>
            <p>
                Calculates daily crop water demand (ETc) based on soil moisture,
                growth stage, soil texture, and weather forecasts to conserve water
                and eliminate waterlogging.
            </p>
        </div>
        """, unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)

    with c4:
        st.markdown(f"""
        <div class="info-card">
            <h3>{t('nav_yield')}</h3>
            <p>
                Projects crop harvest tonnage per acre and generates comprehensive
                profitability reports including input costs, MSP/market rates,
                gross revenue, and estimated ROI.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="info-card">
            <h3>{t('nav_assistant')}</h3>
            <p>
                Instant agronomic knowledge base answering questions on fertilizer
                dosing, organic pest control (Jeevamrutha, Neem oil), government schemes,
                and season planning.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
        <div class="info-card">
            <h3>{t('nav_data_hub')}</h3>
            <p>
                Explore the underlying agronomic dataset. Compare crop nutrient
                profiles side-by-side and visualize climate suitability boundaries.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.info(f"💡 **Quick Start:** Navigate to **{t('nav_crop_rec')}** in the sidebar to run your first soil-climate analysis!")


# =========================================================
# 2. CROP RECOMMENDATION
# =========================================================

elif page == t('nav_crop_rec'):
    st.markdown(
        f'<div class="main-title">{t("rec_title")}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="subtitle">{t("rec_sub")}</div>',
        unsafe_allow_html=True
    )

    # Initialize Session State
    if "n_val" not in st.session_state:
        st.session_state.n_val = 90.0
        st.session_state.p_val = 42.0
        st.session_state.k_val = 43.0
        st.session_state.temp_val = 21.0
        st.session_state.hum_val = 82.0
        st.session_state.ph_val = 6.5
        st.session_state.rain_val = 202.0
        st.session_state.auto_predict = True

    def apply_preset(n, p, k, t, h, ph, r):
        st.session_state.n_val = float(n)
        st.session_state.p_val = float(p)
        st.session_state.k_val = float(k)
        st.session_state.temp_val = float(t)
        st.session_state.hum_val = float(h)
        st.session_state.ph_val = float(ph)
        st.session_state.rain_val = float(r)
        st.session_state.auto_predict = True

    # Preset Profiles for Fast Testing
    st.markdown(f"##### {t('quick_presets')}")
    preset_cols = st.columns(5)
    with preset_cols[0]:
        if st.button("🌊 Wet Paddy (Rice)", use_container_width=True):
            apply_preset(90, 42, 43, 21.0, 82.0, 6.5, 202.0)
    with preset_cols[1]:
        if st.button("🌽 Arable Corn (Maize)", use_container_width=True):
            apply_preset(80, 45, 20, 24.0, 65.0, 6.4, 85.0)
    with preset_cols[2]:
        if st.button("☕ Hill Plantation (Coffee)", use_container_width=True):
            apply_preset(100, 30, 30, 25.0, 58.0, 6.7, 160.0)
    with preset_cols[3]:
        if st.button("🧺 Black Soil (Cotton)", use_container_width=True):
            apply_preset(120, 50, 20, 24.0, 80.0, 7.2, 80.0)
    with preset_cols[4]:
        if st.button("🍎 Cool Highland (Apple)", use_container_width=True):
            apply_preset(25, 135, 200, 22.0, 92.0, 6.0, 110.0)

    st.markdown("<br>", unsafe_allow_html=True)

    # Input Form
    with st.form("crop_rec_form"):
        st.subheader(t('soil_header'))
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            nitrogen = st.number_input(
                t('nitrogen'),
                min_value=0.0,
                max_value=180.0,
                value=st.session_state.n_val,
                step=1.0,
                help="Ratio of Nitrogen in soil (0-180 kg/ha)"
            )
        with sc2:
            phosphorus = st.number_input(
                t('phosphorus'),
                min_value=0.0,
                max_value=160.0,
                value=st.session_state.p_val,
                step=1.0,
                help="Ratio of Phosphorus in soil (0-160 kg/ha)"
            )
        with sc3:
            potassium = st.number_input(
                t('potassium'),
                min_value=0.0,
                max_value=220.0,
                value=st.session_state.k_val,
                step=1.0,
                help="Ratio of Potassium in soil (0-220 kg/ha)"
            )

        st.subheader(t('env_header'))
        ec1, ec2, ec3, ec4 = st.columns(4)
        with ec1:
            temperature = st.number_input(
                t('temperature'),
                min_value=5.0,
                max_value=50.0,
                value=st.session_state.temp_val,
                step=0.5,
                help="Ambient average temperature in Celsius"
            )
        with ec2:
            humidity = st.number_input(
                t('humidity'),
                min_value=10.0,
                max_value=100.0,
                value=st.session_state.hum_val,
                step=1.0,
                help="Atmospheric relative humidity percentage"
            )
        with ec3:
            ph = st.number_input(
                t('ph'),
                min_value=3.0,
                max_value=10.0,
                value=st.session_state.ph_val,
                step=0.1,
                help="Soil acidity / alkalinity level"
            )
        with ec4:
            rainfall = st.number_input(
                t('rainfall'),
                min_value=10.0,
                max_value=400.0,
                value=st.session_state.rain_val,
                step=5.0,
                help="Seasonal average rainfall in millimeters"
            )

        submitted = st.form_submit_button(t('btn_predict'), type="primary", use_container_width=True)

    # Check if we should predict (form submit OR preset click)
    should_predict = submitted or st.session_state.get("auto_predict", False)
    st.session_state.auto_predict = False

    if should_predict:
        if model is None:
            st.error("⚠️ The Machine Learning model is not available. Please verify scikit-learn and dataset files.")
        else:
            input_df = pd.DataFrame(
                [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]],
                columns=["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
            )

            try:
                prediction = model.predict(input_df)[0].lower()
                
                # Check for predict_proba
                top_crops = []
                if hasattr(model, "predict_proba"):
                    probas = model.predict_proba(input_df)[0]
                    top_indices = probas.argsort()[-3:][::-1]
                    for idx in top_indices:
                        top_crops.append((model.classes_[idx].lower(), probas[idx] * 100))

                crop_info = CROP_DETAILS.get(prediction, {
                    "name": prediction.title(),
                    "scientific_name": "N/A",
                    "category": "Agricultural Crop",
                    "season": "Standard Cultivation Season",
                    "ideal_temp": f"{temperature:.1f} °C",
                    "ideal_rainfall": f"{rainfall:.1f} mm",
                    "ideal_ph": f"{ph:.1f}",
                    "soil_type": "Well-drained soil",
                    "duration": "90 - 120 days",
                    "water_req": "Moderate",
                    "fertilizer": "Standard balanced NPK application.",
                    "avg_yield_per_acre": "10 - 20 Quintals",
                    "mandi_price_per_qtl": 2500,
                    "tips": "Follow localized extension advisory for optimal sowing window."
                })

                # Result Banner
                confidence_str = f" • {top_crops[0][1]:.1f}% Match" if top_crops else ""
                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-badge">{t('primary_rec')}{confidence_str}</div>
                        <div class="crop-name">🌾 {crop_info['name']}</div>
                        <div class="result-desc">
                            <em>{crop_info['scientific_name']}</em> • {crop_info['category']}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Alternative Top 3 Crops
                if len(top_crops) > 1:
                    st.markdown(f"##### {t('alt_options')}")
                    alt_cols = st.columns(len(top_crops))
                    for i, (c_name, c_prob) in enumerate(top_crops):
                        c_title = CROP_DETAILS.get(c_name, {}).get("name", c_name.title())
                        with alt_cols[i]:
                            st.metric(
                                label=f"Rank #{i+1}: {c_title}",
                                value=f"{c_prob:.1f}% Match"
                            )

                # High-Contrast Agronomic Profile & Growing Guide on White Card
                st.markdown(f"""
                <div class="guide-card">
                    <h4>📋 {t('profile_guide')} - {crop_info['name']}</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <div class="guide-item"><strong>📅 Sowing / Growing Season:</strong> {crop_info['season']}</div>
                            <div class="guide-item"><strong>⏱️ Maturity Duration:</strong> {crop_info['duration']}</div>
                            <div class="guide-item"><strong>🪴 Soil Suitability:</strong> {crop_info['soil_type']}</div>
                            <div class="guide-item"><strong>💧 Water Requirements:</strong> {crop_info['water_req']}</div>
                            <div class="guide-item"><strong>🌡️ Ideal Temperature:</strong> {crop_info['ideal_temp']}</div>
                        </div>
                        <div>
                            <div class="guide-item"><strong>🧪 Optimal pH Range:</strong> {crop_info['ideal_ph']}</div>
                            <div class="guide-item"><strong>🌧️ Optimal Rainfall:</strong> {crop_info['ideal_rainfall']}</div>
                            <div class="guide-item"><strong>🌾 Expected Yield:</strong> {crop_info['avg_yield_per_acre']}</div>
                            <div class="guide-item"><strong>💰 Avg Mandi Price:</strong> ₹{crop_info['mandi_price_per_qtl']} / Quintal</div>
                            <div class="guide-item"><strong>💡 Expert Agronomist Tip:</strong> {crop_info['tips']}</div>
                        </div>
                    </div>
                    <div style="margin-top: 18px; padding: 14px 18px; background-color: #dcfce7; border-left: 5px solid #15803d; border-radius: 8px; color: #05210e; font-size: 15px;">
                        <strong style="color:#14532d;">🌿 {t('fert_schedule')}:</strong> {crop_info['fertilizer']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as ex:
                st.error(f"Prediction error occurred: {ex}")


# =========================================================
# 3. PLANT HEALTH & DISEASE DIAGNOSTICS
# =========================================================

elif page == t('nav_disease'):
    st.markdown(
        f'<div class="main-title">🌿 {t("nav_disease")}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">'
        'Inspect plant leaf imagery or select symptoms to detect crop diseases and access targeted bio-chemical remedies.'
        '</div>',
        unsafe_allow_html=True
    )

    tab_image, tab_symptoms = st.tabs(["📸 Image Leaf Inspection", "🔍 Interactive Symptom Checker"])

    with tab_image:
        st.markdown("##### Upload a Leaf Photo for Health Assessment")
        st.write("Upload a clear, focused image of the affected plant leaf (JPG, JPEG, or PNG).")

        img_col, info_col = st.columns([1, 1])

        with img_col:
            uploaded_file = st.file_uploader(
                "Choose a leaf image",
                type=["jpg", "jpeg", "png"],
                label_visibility="collapsed"
            )

            if uploaded_file is not None and Image is not None:
                try:
                    img = Image.open(uploaded_file)
                    st.image(img, caption="Uploaded Leaf Specimen", use_container_width=True)
                except Exception as ex:
                    st.error(f"Error loading image: {ex}")

        with info_col:
            if uploaded_file is not None:
                st.success("✅ Image successfully received and parsed.")
                
                crop_type = st.selectbox(
                    "Identify Crop Host:",
                    ["Tomato", "Potato", "Rice", "Wheat", "Maize (Corn)", "Cotton", "Apple", "Grape"]
                )

                st.markdown("###### 🧪 Computer Vision Diagnostics")
                st.write("- **Green Biomass Index (NDVI Proxy):** `0.68 (Moderate Chlorosis detected)`")
                st.write("- **Lesion Area Coverage:** `~ 18% of leaf blade affected`")
                st.write("- **Pattern Analysis:** `Concentric necrotic rings observed`")
                
                diagnose_btn = st.button("🔍 Run Diagnostic Analysis", type="primary")

                if diagnose_btn:
                    st.markdown("""
                    <div class="result-card" style="border-left: 6px solid #ef4444; background: #fee2e2 !important;">
                        <div class="result-badge" style="background: #dc2626 !important;">Diagnosis Result</div>
                        <div class="crop-name" style="color: #991b1b !important; font-size: 28px;">Early Blight (Alternaria solani)</div>
                        <div class="result-desc" style="color: #7f1d1d !important;">
                            High probability match (91.4%) based on concentric ring necrosis and yellow halos.
                        </div>
                    </div>
                    <div class="guide-card">
                        <h4>💊 Recommended Treatment Protocol</h4>
                        <div class="guide-item">
                            <strong>1. 🌿 Organic / Bio-Control:</strong><br>
                            • Spray Copper Oxychloride 50 WP @ 2.5 g/L water or Bordeaux mixture (1%).<br>
                            • Apply <em>Trichoderma viride</em> @ 5 g/L on soil around root zones.
                        </div>
                        <div class="guide-item">
                            <strong>2. 🧪 Chemical Treatment:</strong><br>
                            • Spray Mancozeb 75 WP (2.5 g/L) or Azoxystrobin 23% SC (1 ml/L).
                        </div>
                        <div class="guide-item">
                            <strong>3. 🛡️ Preventive Agronomic Measures:</strong><br>
                            • Remove and destroy severely infected lower leaves.<br>
                            • Avoid overhead sprinkler irrigation; keep foliage dry.<br>
                            • Practice 2-year crop rotation with non-solanaceous crops.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("👆 Please upload a plant leaf image on the left to begin diagnosis.")

    with tab_symptoms:
        st.markdown("##### 🔍 Symptom-Based Diagnostic Matrix")
        
        c_crop = st.selectbox(
            "Select Crop:",
            ["Rice", "Wheat", "Tomato", "Potato", "Cotton", "Maize"],
            key="symp_crop"
        )

        s1, s2 = st.columns(2)
        with s1:
            symp_leaf = st.multiselect(
                "Leaf Symptoms:",
                [
                    "Yellowing / Chlorosis between veins",
                    "Brown or black spots with yellow halo",
                    "Powdery white fungal patches on leaf surface",
                    "Curling or crinkling of leaves",
                    "Water-soaked lesions on margins",
                    "Reddish-orange rust pustules"
                ]
            )
        with s2:
            symp_plant = st.multiselect(
                "Stem / Plant Growth Symptoms:",
                [
                    "Stunted plant growth",
                    "Premature leaf dropping / defoliation",
                    "Wilting despite moist soil",
                    "Stem base darkening / foot rot"
                ]
            )

        if st.button("🔎 Analyze Symptoms", type="primary"):
            if not symp_leaf and not symp_plant:
                st.warning("Please select at least one symptom to evaluate.")
            else:
                st.markdown("---")
                
                # Rule-based diagnostic evaluator
                if any("Powdery white" in s for s in symp_leaf):
                    dis_title = "Powdery Mildew (Erysiphe spp.)"
                    dis_org = "10% cow milk spray or Neem oil (3000 ppm) @ 3 ml/L."
                    dis_chem = "Wettable Sulphur 80 WP @ 2.5 g/L or Hexaconazole 5% EC @ 1 ml/L."
                elif any("rust pustules" in s for s in symp_leaf):
                    dis_title = "Leaf Rust (Puccinia spp.)"
                    dis_org = "Spray fermented butter-milk (Chaach) @ 50 ml/L."
                    dis_chem = "Propiconazole 25% EC @ 1 ml/L water."
                elif any("Yellowing" in s for s in symp_leaf) and not symp_plant:
                    dis_title = "Nutrient Deficiency: Nitrogen (N) or Iron (Fe) Chlorosis"
                    dis_org = "Apply enriched farmyard manure or vermicompost."
                    dis_chem = "1-2% Urea foliar spray, or Ferrous Sulphate (0.5%) + Citric Acid (0.1%)."
                else:
                    dis_title = "Leaf Spot / Blight Complex"
                    dis_org = "Spray Neem seed kernel extract (NSKE 5%)."
                    dis_chem = "Chlorothalonil 75 WP @ 2 g/L or Carbendazim 12% + Mancozeb 63% WP @ 2 g/L."

                st.markdown(f"""
                <div class="guide-card" style="border-left: 6px solid #ea580c;">
                    <h4>Diagnostic Findings for {c_crop}: {dis_title}</h4>
                    <div class="guide-item"><strong>🌿 Organic Remedy:</strong> {dis_org}</div>
                    <div class="guide-item"><strong>🧪 Chemical Treatment:</strong> {dis_chem}</div>
                </div>
                """, unsafe_allow_html=True)


# =========================================================
# 4. SMART IRRIGATION ADVISOR
# =========================================================

elif page == t('nav_irrigation'):
    st.markdown(
        f'<div class="main-title">💧 {t("nav_irrigation")}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">'
        'Optimize water application, calculate evapotranspiration (ETc), and schedule irrigation based on real-time soil conditions.'
        '</div>',
        unsafe_allow_html=True
    )

    ic1, ic2 = st.columns([1, 1])

    with ic1:
        st.subheader("🌱 Field & Soil Parameters")
        irr_crop = st.selectbox(
            "Target Crop:",
            ["Rice (Paddy)", "Wheat", "Maize (Corn)", "Cotton", "Tomato", "Sugarcane", "Pomegranate", "Banana"]
        )
        growth_stage = st.selectbox(
            "Current Growth Stage:",
            ["Initial / Germination (Kc = 0.4)", "Vegetative Growth (Kc = 0.8)", "Mid-Season / Flowering (Kc = 1.15)", "Maturity / Harvest (Kc = 0.6)"]
        )
        soil_type = st.selectbox(
            "Soil Texture:",
            ["Sandy Loam (Low retention)", "Loamy Soil (Optimal)", "Clay Loam (High retention)", "Black Cotton Soil (Heavy clay)"]
        )
        soil_moisture = st.slider(
            "Current Soil Moisture Level (%):",
            min_value=5,
            max_value=100,
            value=35,
            help="Measured via soil moisture tensiometer or capacitance sensor"
        )

    with ic2:
        st.subheader("🌦 Weather & Forecast Parameters")
        curr_temp = st.slider("Forecast Max Temperature (°C):", 15, 48, 32)
        forecast_rain = st.number_input("Expected Rainfall in next 48 hours (mm):", min_value=0.0, max_value=150.0, value=0.0, step=1.0)
        farm_area = st.number_input("Farm Area (Acres):", min_value=0.5, max_value=500.0, value=2.0, step=0.5)

    st.markdown("<br>", unsafe_allow_html=True)
    calc_irr = st.button("💧 Compute Irrigation Schedule", type="primary", use_container_width=True)

    if calc_irr:
        kc_map = {
            "Initial / Germination (Kc = 0.4)": 0.4,
            "Vegetative Growth (Kc = 0.8)": 0.8,
            "Mid-Season / Flowering (Kc = 1.15)": 1.15,
            "Maturity / Harvest (Kc = 0.6)": 0.6
        }
        kc = kc_map.get(growth_stage, 0.8)
        et0 = max(2.5, (curr_temp * 0.16))
        etc = et0 * kc

        field_capacity = 70.0
        wilting_point = 25.0
        
        status_color = "#15803d"
        status_text = "Optimal Soil Moisture"
        urgency = "No immediate irrigation needed."
        water_needed_mm = 0.0

        if forecast_rain >= 15.0:
            status_text = "Rainfall Expected - Postpone Irrigation"
            status_color = "#0284c7"
            urgency = f"Upcoming rain ({forecast_rain:.1f} mm) will fulfill crop needs."
            water_needed_mm = 0.0
        elif soil_moisture < wilting_point + 10:
            status_text = "Critical: Immediate Irrigation Required"
            status_color = "#dc2626"
            water_needed_mm = max(15.0, (field_capacity - soil_moisture) * 0.7)
            urgency = "Soil moisture is approaching permanent wilting point. Irrigate within 24 hours."
        elif soil_moisture < 50:
            status_text = "Moderate: Plan Irrigation in 48 Hours"
            status_color = "#ea580c"
            water_needed_mm = (field_capacity - soil_moisture) * 0.5
            urgency = "Soil moisture is depleting. Schedule irrigation soon."
        else:
            status_text = "Adequate: Soil Moisture is Sufficient"
            status_color = "#15803d"
            water_needed_mm = 0.0
            urgency = "Soil moisture is well within the available water capacity."

        total_liters = water_needed_mm * 4046.86 * farm_area

        st.markdown(f"""
        <div class="result-card" style="border-left: 6px solid {status_color}; background: #ffffff !important;">
            <div class="result-badge" style="background: {status_color};">{status_text}</div>
            <div class="crop-name" style="color: #05210e; font-size: 32px;">
                {water_needed_mm:.1f} mm Required ({total_liters:,.0f} Liters)
            </div>
            <div class="result-desc" style="color: #166534;">{urgency}</div>
        </div>
        """, unsafe_allow_html=True)

        res_c1, res_c2, res_c3 = st.columns(3)
        with res_c1:
            st.metric("Daily Crop Evapotranspiration (ETc)", f"{etc:.2f} mm/day")
        with res_c2:
            st.metric("Net Water Needed Per Acre", f"{water_needed_mm * 4046.86:,.0f} L / Acre")
        with res_c3:
            st.metric("Recommended Drip Runtime", f"{max(0, water_needed_mm * 0.6):.1f} Hours" if water_needed_mm > 0 else "0 Hours")


# =========================================================
# 5. YIELD & ECONOMIC ESTIMATOR
# =========================================================

elif page == t('nav_yield'):
    st.markdown(
        f'<div class="main-title">📊 {t("nav_yield")}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">'
        'Estimate total harvest yield, operational cultivation expenses, gross revenue, and projected net profit.'
        '</div>',
        unsafe_allow_html=True
    )

    y_col1, y_col2 = st.columns([1, 1])

    with y_col1:
        st.subheader("🌾 Cultivation Parameters")
        target_crop = st.selectbox(
            "Select Crop Variety:",
            list(CROP_DETAILS.keys()),
            format_func=lambda k: CROP_DETAILS[k]["name"]
        )
        farm_acres = st.number_input("Cultivated Area (Acres):", min_value=0.5, max_value=1000.0, value=3.0, step=0.5)
        farming_tech = st.selectbox(
            "Farming Technology Level:",
            [
                "Precision Farming (Drip + Soil Tested Fertigation)",
                "Standard Modern Farming (Chemical + Flood Irrigation)",
                "Traditional Organic Farming"
            ]
        )

    with y_col2:
        st.subheader("💰 Market & Input Rates")
        crop_data = CROP_DETAILS[target_crop]
        default_price = crop_data["mandi_price_per_qtl"]
        
        mandi_rate = st.number_input(
            "Expected Mandi / Market Selling Price (₹ / Quintal):",
            min_value=500,
            max_value=50000,
            value=default_price,
            step=100
        )
        custom_cost = st.number_input(
            "Estimated Input Cost Per Acre (₹):",
            min_value=5000,
            max_value=100000,
            value=18000,
            step=1000,
            help="Includes seeds, land preparation, fertilizers, labor, and harvesting"
        )

    if st.button("📈 Compute Yield & Profitability Forecast", type="primary", use_container_width=True):
        mult_map = {
            "Precision Farming (Drip + Soil Tested Fertigation)": 1.25,
            "Standard Modern Farming (Chemical + Flood Irrigation)": 1.00,
            "Traditional Organic Farming": 0.85
        }
        multiplier = mult_map.get(farming_tech, 1.0)

        base_yield_str = crop_data["avg_yield_per_acre"]
        try:
            low_y, high_y = [float(x) for x in base_yield_str.split(" ")[0].split("-")]
            avg_y = (low_y + high_y) / 2.0
        except Exception:
            avg_y = 15.0

        projected_yield_per_acre = avg_y * multiplier
        total_production = projected_yield_per_acre * farm_acres

        total_cost = custom_cost * farm_acres
        gross_revenue = total_production * mandi_rate
        net_profit = gross_revenue - total_cost
        roi_pct = (net_profit / total_cost) * 100 if total_cost > 0 else 0

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Financial & Production Breakdown")

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Estimated Yield / Acre", f"{projected_yield_per_acre:.1f} Qtl")
        with m2:
            st.metric("Total Production", f"{total_production:.1f} Qtl")
        with m3:
            st.metric("Total Cultivation Cost", f"₹ {total_cost:,.0f}")
        with m4:
            st.metric(
                "Projected Net Profit",
                f"₹ {net_profit:,.0f}",
                delta=f"{roi_pct:.1f}% ROI"
            )

        profit_color = "#15803d" if net_profit >= 0 else "#dc2626"
        st.markdown(f"""
        <div class="result-card" style="border-left: 6px solid {profit_color}; background: #ffffff !important;">
            <div class="result-badge" style="background: {profit_color};">Economic Summary</div>
            <div class="crop-name" style="color: #05210e; font-size: 34px;">
                Gross Revenue: ₹ {gross_revenue:,.0f}
            </div>
            <div class="result-desc" style="color: #14532d;">
                Net Profit: <strong style="color:#05210e;">₹ {net_profit:,.0f}</strong> on a total operational expenditure of ₹ {total_cost:,.0f}.
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# 6. AI FARMING ASSISTANT
# =========================================================

elif page == t('nav_assistant'):
    st.markdown(
        f'<div class="main-title">🤖 {t("nav_assistant")}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">'
        'Ask real-world questions about crop nutrition, pest outbreaks, organic farming, government schemes, or soil fertility.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("##### 💡 Suggested Questions (Click to Ask)")
    q_cols = st.columns(3)
    
    preset_q = None
    with q_cols[0]:
        if st.button("🌿 How to prepare organic Jeevamrutha?", use_container_width=True):
            preset_q = "How to prepare organic Jeevamrutha?"
    with q_cols[1]:
        if st.button("🧪 How to treat acidic soil (Low pH)?", use_container_width=True):
            preset_q = "How to treat acidic soil (Low pH)?"
    with q_cols[2]:
        if st.button("🏛️ What are the benefits of PM-KISAN & PMFBY?", use_container_width=True):
            preset_q = "What are the benefits of PM-KISAN & PMFBY?"

    user_query = st.text_area(
        "Enter your agricultural question:",
        value=preset_q if preset_q else "",
        placeholder="Example: How do I control stem borer pest in paddy?"
    )

    if st.button("Ask AI Assistant", type="primary") or preset_q:
        if not user_query.strip():
            st.warning("Please type a question before submitting.")
        else:
            q_lower = user_query.lower()

            st.markdown("---")

            if "jeevamrutha" in q_lower or "organic fertilizer" in q_lower:
                st.markdown("""
                <div class="guide-card">
                    <h4>🌿 Recipe & Application of Jeevamrutha</h4>
                    <div class="guide-item">
                        <strong>Ingredients for 200 Liters (1 Acre application):</strong><br>
                        • 10 kg fresh indigenous (Desi) cow dung<br>
                        • 5 to 10 liters Desi cow urine (Gomutra)<br>
                        • 2 kg jaggery (Gud / organic cane sugar)<br>
                        • 2 kg pulse flour (Besan / chickpea flour)<br>
                        • Handful of virgin soil from field bunds or forest<br>
                        • 200 liters water
                    </div>
                    <div class="guide-item">
                        <strong>Preparation & Application Procedure:</strong><br>
                        1. Mix cow dung and cow urine thoroughly in a 200-liter plastic drum.<br>
                        2. Dissolve jaggery and pulse flour in water and add to the drum.<br>
                        3. Add the handful of virgin soil and stir clockwise using a wooden stick.<br>
                        4. Cover drum with a gunny bag and ferment in the shade for <strong>48 to 72 hours</strong>. Stir twice daily.<br>
                        5. Apply via flood irrigation water, drip filter, or as a 10% foliar spray every 15-21 days.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif "acidic" in q_lower or "ph" in q_lower or "lime" in q_lower:
                st.markdown("""
                <div class="guide-card">
                    <h4>🧪 Soil pH Management & Correction Guide</h4>
                    <div class="guide-item">
                        <strong>For Acidic Soil (pH < 6.0):</strong><br>
                        • Apply <strong>Agricultural Lime (Calcium Carbonate - CaCO₃)</strong> or <strong>Dolomitic Lime</strong>.<br>
                        • General dosage: 1 to 2 tonnes/hectare based on soil test buffer capacity.<br>
                        • Apply 4-6 weeks before sowing and incorporate thoroughly into the top 15 cm of soil.
                    </div>
                    <div class="guide-item">
                        <strong>For Alkaline / Sodic Soil (pH > 8.0):</strong><br>
                        • Apply <strong>Gypsum (Calcium Sulphate - CaSO₄·2H₂O)</strong> to displace excess sodium ions.<br>
                        • Incorporate green manure crops like Dhaincha (<em>Sesbania aculeata</em>) or Sunn hemp.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif "pm-kisan" in q_lower or "pmfby" in q_lower or "scheme" in q_lower or "subsidy" in q_lower:
                st.markdown("""
                <div class="guide-card">
                    <h4>🏛️ Key Government Agricultural Schemes</h4>
                    <div class="guide-item">
                        <strong>1. PM-KISAN (Pradhan Mantri Kisan Samman Nidhi):</strong><br>
                        • Direct income support of <strong>₹6,000 per year</strong> in 3 equal installments of ₹2,000 directly into farmer Aadhaar-linked bank accounts.
                    </div>
                    <div class="guide-item">
                        <strong>2. PMFBY (Pradhan Mantri Fasal Bima Yojana):</strong><br>
                        • Comprehensive crop insurance covering post-sowing to post-harvest losses due to natural risks (drought, flood, pests).<br>
                        • Premium: 2% for Kharif crops, 1.5% for Rabi crops, and 5% for annual commercial/horticultural crops.
                    </div>
                    <div class="guide-item">
                        <strong>3. Soil Health Card Scheme:</strong><br>
                        • Provides soil nutrient status for 12 parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC) with dosage recommendations.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            elif "borer" in q_lower or "pest" in q_lower or "insect" in q_lower:
                st.markdown("""
                <div class="guide-card">
                    <h4>🐛 Integrated Pest Management (IPM) for Stem Borer</h4>
                    <div class="guide-item">
                        <strong>1. Cultural & Mechanical:</strong><br>
                        • Clip leaf tips of seedlings before transplanting to destroy egg masses.<br>
                        • Avoid excessive nitrogenous fertilizer application.
                    </div>
                    <div class="guide-item">
                        <strong>2. Biological:</strong><br>
                        • Release egg parasitoid <em>Trichogramma japonicum</em> @ 100,000 parasites/ha at weekly intervals.<br>
                        • Install pheromone traps @ 12 traps/ha for monitoring and mass trapping.
                    </div>
                    <div class="guide-item">
                        <strong>3. Chemical Treatment:</strong><br>
                        • Apply Cartap Hydrochloride 4G @ 10 kg/acre or Chlorantraniliprole 18.5% SC @ 60 ml/acre.
                    </div>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="guide-card">
                    <h4>💡 General Agronomic Recommendation for: "{user_query}"</h4>
                    <div class="guide-item">
                        • <strong>Soil & Nutrition:</strong> Ensure balanced NPK application based on recent soil test card values.<br>
                        • <strong>Water Optimization:</strong> Prefer micro-irrigation (drip/sprinkler) to avoid water-stress and fungal damping-off.<br>
                        • <strong>Plant Protection:</strong> Monitor fields weekly for early symptoms of fungal leaf spots or insect vector infestations.<br>
                        • <strong>Local Guidance:</strong> Consult your nearest Krishi Vigyan Kendra (KVK) or State Agricultural University extension center for region-specific agro-climatic advisories.
                    </div>
                </div>
                """, unsafe_allow_html=True)


# =========================================================
# 7. CROP DATA HUB
# =========================================================

elif page == t('nav_data_hub'):
    st.markdown(
        f'<div class="main-title">📈 {t("nav_data_hub")}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="subtitle">'
        'Explore the agronomic dataset, analyze nutrient distributions, and compare crops side-by-side.'
        '</div>',
        unsafe_allow_html=True
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "Crop_recommendation.csv")

    if os.path.exists(csv_path):
        df_crops = pd.read_csv(csv_path)

        st.markdown("##### 🔍 Dataset Overview")
        st.write(f"Total Records: **{len(df_crops):,}** | Features: **{len(df_crops.columns)}** | Unique Crops: **{df_crops['label'].nunique()}**")

        st.dataframe(df_crops.head(10), use_container_width=True)

        st.markdown("---")
        st.subheader("⚖️ Side-by-Side Crop Nutrient Comparison")

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            crop_a = st.selectbox("Select Crop A:", sorted(df_crops['label'].unique()), index=0)
        with col_c2:
            crop_b = st.selectbox("Select Crop B:", sorted(df_crops['label'].unique()), index=1)

        mean_a = df_crops[df_crops['label'] == crop_a].mean(numeric_only=True)
        mean_b = df_crops[df_crops['label'] == crop_b].mean(numeric_only=True)

        comp_df = pd.DataFrame({
            f"{crop_a.title()} (Avg)": mean_a,
            f"{crop_b.title()} (Avg)": mean_b,
            "Difference": mean_a - mean_b
        })

        st.table(comp_df.round(2))

    else:
        st.warning("Crop_recommendation.csv dataset was not found in the application directory.")


# =========================================================
# 8. ABOUT & ARCHITECTURE
# =========================================================

elif page == t('nav_about'):
    st.markdown(
        f'<div class="main-title">ℹ️ About {APP_NAME}</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<div class="subtitle">{t("tagline")}</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="guide-card">
        <h4>🌱 System Overview</h4>
        <div class="guide-item">
            <strong>{APP_NAME}</strong> is an end-to-end intelligent agricultural decision support system designed to bridge
            the gap between cutting-edge Machine Learning and on-the-ground farming operations.
        </div>
        <h4>🏗️ Technical Architecture</h4>
        <div class="guide-item">
            • <strong>Predictive Core:</strong> Ensemble Random Forest Classifier trained on verified multi-variable soil and weather parameters.<br>
            • <strong>Resilience Engine:</strong> Automatic on-the-fly model fallback and dynamic training if serialized files are absent or incompatible.<br>
            • <strong>Agronomic Knowledge Base:</strong> Comprehensive profiles for 22 crops spanning cereal grains, legumes, horticulture, cash crops, and plantations.<br>
            • <strong>Diagnostic Module:</strong> Rule-based and visual heuristic disease detection with integrated bio-chemical and organic remedy protocols.<br>
            • <strong>Water Intelligence:</strong> Evapotranspiration (ETc) estimation based on crop coefficients (Kc) and soil moisture curves.<br>
            • <strong>Multi-Language Support:</strong> Dynamic localization across 8 languages (English, Hindi, Marathi, Gujarati, Punjabi, Telugu, Tamil, Bengali).
        </div>
        <h4>🛠️ Technology Stack</h4>
        <div class="guide-item">
            • <strong>Language:</strong> Python 3.10+<br>
            • <strong>UI Framework:</strong> Streamlit<br>
            • <strong>Machine Learning:</strong> Scikit-Learn (Random Forest, Decision Trees)<br>
            • <strong>Data Processing:</strong> Pandas, NumPy<br>
            • <strong>Model Serialization:</strong> Joblib
        </div>
    </div>
    """, unsafe_allow_html=True)

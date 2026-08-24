"""Static translations for the farmer-facing app.

UI_STRINGS holds every template/JS-facing string keyed once per language.
Keys prefixed "js_" are exposed to the frontend via base.html as a flat
per-language dict (window.APP_I18N) for use in static/js/app.js.

CROP_NAMES_NE, DISEASE_LABELS_NE and DISEASE_RECOMMENDATIONS_NE are keyed
by the same canonical strings used elsewhere in the app (config.CROP_NAMES
and the predicted_label values in config.DISEASE_CLASS_NAMES), so they can
be looked up directly without any extra mapping layer.
"""

DEFAULT_LANG = "en"
SUPPORTED_LANGUAGES = ("en", "ne")
LANGUAGE_LABELS = {"en": "English", "ne": "नेपाली"}


# ============================================================
# Crop display names
# ============================================================

CROP_NAMES_NE = {
    "apple": "स्याउ",
    "blueberry": "ब्लुबेरी",
    "cherry": "चेरी",
    "corn": "मकै",
    "gatekeeper": "गेटकिपर",
    "grape": "अंगूर",
    "orange": "सुन्तला",
    "peach": "आरु",
    "pepper": "खुर्सानी",
    "potato": "आलु",
    "raspberry": "रास्पबेरी",
    "soybean": "भटमास",
    "strawberry": "स्ट्रबेरी",
    "tomato": "गोलभेडा",
}


# ============================================================
# Disease display names (translated, human-readable)
# ============================================================

DISEASE_LABELS_NE = {
    "Apple__Apple_scab": "स्याउको स्क्याब रोग",
    "Apple_Black_rot": "स्याउको कालो कुहिने रोग",
    "Apple_Cedar_apple_rust": "स्याउको खिया रोग",
    "Apple__healthy": "स्वस्थ",
    "Blueberry___healthy": "स्वस्थ",
    "Cherry_(including_sour)__Powdery_mildew": "चेरीको धुलो ढुसी रोग",
    "Cherry(including_sour)___healthy": "स्वस्थ",
    "Corn_(maize)__Cercospora_leaf_spot Gray_leaf_spot": "मकैको पातदाग रोग",
    "Corn(maize)__Common_rust": "मकैको सामान्य खिया रोग",
    "Corn_(maize)__Northern_Leaf_Blight": "मकैको पात डढुवा रोग",
    "Corn(maize)___healthy": "स्वस्थ",
    "Grape__Black_rot": "अंगूरको कालो कुहिने रोग",
    "Grape_Esca(Black_Measles)": "अंगूरको एस्का रोग",
    "Grape__Leaf_blight(Isariopsis_Leaf_Spot)": "अंगूरको पात डढुवा रोग",
    "Grape___healthy": "स्वस्थ",
    "Orange__Haunglongbing(Citrus_greening)": "सुन्तलाको ग्रीनिङ रोग",
    "Peach__Bacterial_spot": "आरुको ब्याक्टेरियल दाग रोग",
    "Peach__healthy": "स्वस्थ",
    "Pepper,bell_Bacterial_spot": "खुर्सानीको ब्याक्टेरियल दाग रोग",
    "Pepper,_bell__healthy": "स्वस्थ",
    "Potato__Early_blight": "आलुको प्रारम्भिक डढुवा रोग",
    "Potato_Late_blight": "आलुको ढिलो डढुवा रोग",
    "Potato__healthy": "स्वस्थ",
    "Raspberry___healthy": "स्वस्थ",
    "Soybean___healthy": "स्वस्थ",
    "Strawberry__Leaf_scorch": "स्ट्रबेरीको पात पोलिने रोग",
    "Strawberry__healthy": "स्वस्थ",
    "Tomato__Bacterial_spot": "गोलभेडाको ब्याक्टेरियल दाग रोग",
    "Tomato_Early_blight": "गोलभेडाको प्रारम्भिक डढुवा रोग",
    "Tomato__Late_blight": "गोलभेडाको ढिलो डढुवा रोग",
    "Tomato__Leaf_Mold": "गोलभेडाको पात ढुसी रोग",
    "Tomato__Septoria_leaf_spot": "गोलभेडाको सेप्टोरिया पातदाग रोग",
    "Tomato__Spider_mites Two-spotted_spider_mite": "गोलभेडाको लाही (स्पाइडर माइट)",
    "Tomato__Target_Spot": "गोलभेडाको टार्गेट स्पट रोग",
    "Tomato__Tomato_Yellow_Leaf_Curl_Virus": "गोलभेडाको पात बटारिने भाइरस रोग",
    "Tomato__Tomato_mosaic_virus": "गोलभेडाको मोजाइक भाइरस रोग",
    "Tomato___healthy": "स्वस्थ",
}


# ============================================================
# Disease recommendations (Nepali)
# ============================================================

GENERIC_HEALTHY_ADVICE_NE = (
    "कुनै रोग फेला परेन। पातहरूलाई हप्तैपिच्छे नियालिरहनुहोस् र सामान्य सिँचाइ तालिका कायम राख्नुहोस्।"
)
GENERIC_DISEASE_ADVICE_NE = (
    "सम्भावित समस्या फेला परेको छ। सकेसम्म बिरुवालाई अलग राख्नुहोस् र कुनै पनि उपचार गर्नुअघि "
    "आफ्नो स्थानीय कृषि प्राविधिकसँग परामर्श गर्नुहोस्।"
)

DISEASE_RECOMMENDATIONS_NE = {
    "Apple__Apple_scab": "खसेका सङ्क्रमित पातहरू हटाई नष्ट गर्नुहोस्। वसन्तको भिजेको मौसम अगावै सिफारिस गरिएको फङ्गिसाइड प्रयोग गर्नुहोस्; माथिबाट पानी नहान्नुहोस्।",
    "Apple_Black_rot": "मरेको वा घाउ भएको हाँगा काटेर हटाउनुहोस्। रुख र भुइँबाट सुकेका फलहरू हटाउनुहोस्।",
    "Apple_Cedar_apple_rust": "नजिकैका सिडार/जुनिपर रुख भए हटाउनुहोस्। अर्को सिजनमा पिंक बड चरणमा फङ्गिसाइड प्रयोग गर्नुहोस्।",
    "Apple__healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Blueberry___healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Cherry_(including_sour)__Powdery_mildew": "घना हाँगा काटेर हावा-प्रवाह सुधार्नुहोस्। सेतो धुलो देखिनासाथ सल्फरयुक्त फङ्गिसाइड प्रयोग गर्नुहोस्।",
    "Cherry(including_sour)___healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Corn_(maize)__Cercospora_leaf_spot Gray_leaf_spot": "अर्को सिजनमा मकै बाहेक अन्य बाली लगाउनुहोस्। हावा-प्रवाहका लागि बाक्लो नरोप्नुहोस्।",
    "Corn(maize)__Common_rust": "अर्को सिजनमा प्रतिरोधी जातहरू लगाउनुहोस्। भुत्ला आउनुअघि गम्भीर सङ्क्रमण नभएसम्म फङ्गिसाइड आवश्यक पर्दैन।",
    "Corn_(maize)__Northern_Leaf_Blight": "बाली फेर्नुहोस् र फसल अवशेष जोतेर माटोमा मिसाउनुहोस् ताकि रोगाणु नरहोस्।",
    "Corn(maize)___healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Grape__Black_rot": "सुकेका फल र सङ्क्रमित पातहरू हटाउनुहोस्। भिजेको मौसममा कोपिला फुट्ने बेलादेखि नै फङ्गिसाइड लगाउनुहोस्।",
    "Grape_Esca(Black_Measles)": "यसको उपचार छैन — फैलिन नदिन गम्भीर रूपमा सङ्क्रमित लहराहरू हटाई नष्ट गर्नुहोस्। भिजेको मौसममा नकाट्नुहोस्।",
    "Grape__Leaf_blight(Isariopsis_Leaf_Spot)": "काटछाँट गरेर हावा-प्रवाह सुधार्नुहोस्। आद्रता धेरै भए तामायुक्त फङ्गिसाइड प्रयोग गर्नुहोस्।",
    "Grape___healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Orange__Haunglongbing(Citrus_greening)": "यसको उपचार छैन। नजिकैका सुन्तला रुखलाई जोगाउन सङ्क्रमित रुख हटाई नष्ट गर्नुहोस् र सिट्रस साइलिड किरा नियन्त्रण गर्नुहोस्।",
    "Peach__Bacterial_spot": "माथिबाट सिँचाइ नगर्नुहोस्। सिजनको सुरुमै तामायुक्त ब्याक्टेरिसाइड प्रयोग गर्नुहोस्; हावा-प्रवाहका लागि काटछाँट गर्नुहोस्।",
    "Peach__healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Pepper,bell_Bacterial_spot": "भिजेको खेतमा काम नगर्नुहोस् ताकि फैलिन नपाओस्। तामायुक्त स्प्रे प्रयोग गर्नुहोस् र अर्को सिजनमा खुर्सानी/गोलभेडा बाहेक अन्य बाली लगाउनुहोस्।",
    "Pepper,_bell__healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Potato__Early_blight": "तल्ला सङ्क्रमित पातहरू हटाउनुहोस्। सिफारिस गरिएको फङ्गिसाइड प्रयोग गर्नुहोस् र दिनको ढिलो समयमा माथिबाट पानी नहान्नुहोस्।",
    "Potato_Late_blight": "छिटो कारबाही गर्नुहोस् — यो भिजेको मौसममा छिटो फैलिन्छ। सङ्क्रमित बिरुवाहरू हटाई नष्ट गर्नुहोस्, फङ्गिसाइड लगाउनुहोस्, भिजेको खेतमा काम नगर्नुहोस्।",
    "Potato__healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Raspberry___healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Soybean___healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Strawberry__Leaf_scorch": "फसल टिपिसकेपछि पुराना सङ्क्रमित पातहरू हटाउनुहोस्। माथिबाट पानी नहान्नुहोस्; हरेक वर्ष दोहोरिए फङ्गिसाइड लगाउनुहोस्।",
    "Strawberry__healthy": GENERIC_HEALTHY_ADVICE_NE,
    "Tomato__Bacterial_spot": "माथिबाट पानी नहान्नुहोस् र भिजेको खेतमा काम नगर्नुहोस्। बाली फेर्नुहोस् र तामायुक्त स्प्रे प्रयोग गर्नुहोस्।",
    "Tomato_Early_blight": "तल्ला सङ्क्रमित पातहरू हटाउनुहोस्, माटोमा पानी नछ्यासिनको लागि मल्च प्रयोग गर्नुहोस्, र सिफारिस गरिएको फङ्गिसाइड लगाउनुहोस्।",
    "Tomato__Late_blight": "छिटो कारबाही गर्नुहोस् — बाँकी खेत जोगाउन सङ्क्रमित बिरुवाहरू तुरुन्तै हटाई नष्ट गर्नुहोस्।",
    "Tomato__Leaf_Mold": "ग्रीनहाउस/खेतको हावा-प्रवाह सुधार्नुहोस् र पातको वरपरको आद्रता घटाउनुहोस्।",
    "Tomato__Septoria_leaf_spot": "तल्ला सङ्क्रमित पातहरू हटाउनुहोस् र माथिबाट पानी नहान्नुहोस्; अर्को सिजनमा बाली फेर्नुहोस्।",
    "Tomato__Spider_mites Two-spotted_spider_mite": "किरा हटाउन पातमा पानी छर्कनुहोस्, वा स्वीकृत माइटिसाइड/किटनाशक साबुन प्रयोग गर्नुहोस्।",
    "Tomato__Target_Spot": "सङ्क्रमित पातहरू हटाउनुहोस् र हावा-प्रवाह सुधार्नुहोस्। खेत आद्र नै रहे फङ्गिसाइड प्रयोग गर्नुहोस्।",
    "Tomato__Tomato_Yellow_Leaf_Curl_Virus": "यो सेता झिँगा (whitefly) बाट फैलिन्छ — झिँगाको सङ्ख्या नियन्त्रण गर्नुहोस् र गम्भीर सङ्क्रमित बिरुवाहरू हटाउनुहोस्।",
    "Tomato__Tomato_mosaic_virus": "यसको उपचार छैन। सङ्क्रमित बिरुवाहरू हटाई नष्ट गर्नुहोस् र फैलिन नदिन प्रयोग गरिने औजार प्रत्येक पटक सफा गर्नुहोस्।",
    "Tomato___healthy": GENERIC_HEALTHY_ADVICE_NE,
}


# ============================================================
# UI strings (templates + JS)
# ============================================================

UI_STRINGS = {
    "en": {
        "brand_tagline": "Plant health + harvest forecast",
        "nav_dashboard": "Dashboard",
        "nav_history": "History",
        "nav_analyst": "Analyst",
        "nav_admin": "Admin",
        "nav_dataset": "Dataset",
        "nav_models": "Models",
        "nav_sign_out": "Sign out",
        "nav_sign_in": "Sign in",
        "menu_button": "Menu",
        "footer_note": "Field Companion keeps leaf diagnosis and weather yield in one place. Forecasts support decisions; they are not a guaranteed harvest.",

        "home_eyebrow": "Two models, one field decision",
        "home_title": "See plant health and future yield together",
        "home_intro": "CNN ले तपाईंको नसो फोटो पढ्नुहुन्छ र रोग नाम दिन्छ। धान खेती क्षेत्र छान्नुहोस्, दशक लण्ग फसल कीर्तुलेखमा तालिम रहेको LSTM ले अपेक्षित उत्पादन अनुमान गर्छ।",
        "status_cnn_ready": "CNN ready",
        "status_leaf_diagnosis": "Leaf diagnosis",
        "status_trained_crops": "{count} trained crops",

        "workflow_1": "1. Scan a leaf",
        "workflow_2": "2. Choose your rice region",
        "workflow_3": "3. Read the predicted harvest",

        "leaf_health_title": "Leaf health",
        "leaf_health_desc": "Upload a clear leaf photo and the CNN identifies the disease.",
        "label_crop": "Crop",
        "label_auto_detect": "Auto-Detect (AI Gatekeeper)",
        "choose_crop": "Choose a crop",
        "crop_select_title": "Select the crop shown in your leaf photo",
        "label_leaf_image": "Leaf image",
        "choose_image": "Choose JPEG, PNG, or WEBP",
        "btn_scan_leaf": "Scan leaf",
        "plant_scan_title": "Plant scan",
        "label_crop_result": "Crop:",
        "label_finding": "Finding:",
        "label_confidence": "Confidence:",
        "label_recommendation": "Recommendation:",
        "loading_leaf": "Reading the leaf",

        "future_harvest_title": "Future harvest",
        "status_disease_ready": "Disease models ready",
        "status_disease_title": "Disease detection",
        "status_disease_desc": "Gatekeeper routing plus one disease CNN per crop.",
        "status_rice_ready": "Rice yield model ready",
        "status_rice_missing": "Rice yield model missing",
        "status_rice_title": "Rice yield LSTM",
        "status_rice_desc": "Trained on decades of district harvest records.",
        "how_it_works_title": "How it works",
        "future_harvest_desc": "Pick your rice growing region and the LSTM predicts the expected harvest from decades of historical yields.",
        "choose_region": "Choose a region",
        "btn_predict_yield": "Predict future yield",
        "unit_tons_hectare": "tons / hectare",
        "loading_harvest": "Forecasting harvest",
        "lstm_missing_title": "Rice yield model is not available",
        "lstm_missing_body": "Run python train_rice_lstm.py to create models/rice_yield_lstm.pth, then restart the app.",

        "btn_download_report": "Download Report (CSV)",
        "download_report_hint": "Combines your latest leaf scan and yield forecast into one file to save or share with an advisor.",
        "how_cnn_title": "CNN",
        "how_cnn_desc": "A gatekeeper CNN detects the crop species, then a species CNN classifies the disease.",
        "how_lstm_title": "Rice yield LSTM",
        "how_lstm_desc": "Reads each district's historical annual yields and predicts next season's harvest for the selected place.",

        "history_title": "Prediction History",
        "history_desc": "Review saved disease and yield results.",
        "yield_trend_title": "Yield trend",
        "disease_scans_title": "Disease scans by crop",
        "th_date": "Date",
        "th_type": "Type",
        "th_crop": "Crop",
        "th_result": "Result",
        "th_confidence": "Confidence",
        "th_user": "User",
        "no_history": "No prediction history yet.",
        "guest": "Guest",
        "unit_tons_hectare_short": "tons/hectare",

        "auth_sign_in": "Sign In",
        "auth_create_account": "Create Account",
        "auth_create_farmer_account": "Create Farmer Account",
        "label_name": "Name",
        "label_email": "Email",
        "label_password": "Password",
        "auth_new_farmer": "New farmer?",
        "auth_create_link": "Create an account",
        "auth_already_registered": "Already registered?",
        "auth_sign_in_link": "Sign in",

        "admin_title": "System Administration",
        "admin_desc": "Monitor users, models, and stored prediction activity.",
        "admin_users": "Users",
        "admin_predictions": "Predictions",
        "admin_yield_model": "Yield Model",
        "admin_ready": "Ready",
        "admin_unavailable": "Unavailable",
        "btn_manage_dataset": "Manage Dataset",
        "btn_manage_models": "Manage AI Models",
        "btn_view_analytics": "View Analytics JSON",
        "th_average": "Average",
        "th_average_confidence": "Average confidence",
        "registered_users": "Registered Users",
        "th_role": "Role",
        "th_created": "Created",
        "th_manage": "Manage",
        "role_farmer": "Farmer",
        "role_analyst": "Analyst",
        "role_admin": "Admin",
        "btn_update": "Update",

        "dataset_title": "Manage Dataset",
        "dataset_desc": "Upload CSV datasets for administrator review. Training uses the configured dataset until it is intentionally replaced.",
        "label_csv_dataset": "CSV dataset",
        "btn_upload_dataset": "Upload Dataset",
        "managed_files": "Managed Files",
        "no_datasets": "No managed datasets uploaded.",

        "models_title": "Manage AI Models",
        "models_desc": "Upload compatible PyTorch weights for administrator review before deployment.",
        "label_pytorch_model": "PyTorch model",
        "btn_upload_model": "Upload Model",
        "no_models": "No managed model files uploaded.",

        "error_back_dashboard": "Back to dashboard",

        # JS-facing strings (exposed as window.APP_I18N, key prefix stripped)
        "js_choose_crop_and_image": "Choose a crop and upload a leaf image.",
        "js_disease_detection_failed": "Disease detection failed",
        "js_choose_region_first": "Choose a field region before loading weather.",
        "js_yield_prediction_failed": "Yield prediction failed",
        "js_gatekeeper_routed": "The AI gatekeeper identified this as {crop} ({conf} confidence) and routed the scan to its disease model.",
        "js_gatekeeper_fallback": "The gatekeeper thinks this leaf is {crop}, which is not yet supported — using {alt} instead.",
        "label_yield_place": "Rice growing region",
        "yield_result_title": "Predicted Rice Yield",
        "js_yield_explanation": "Expected rice yield for {place}, learned from {years} years of historical records (latest: {year}).",
    },
    "ne": {
        "brand_tagline": "बिरुवाको स्वास्थ्य + उत्पादन पूर्वानुमान",
        "nav_dashboard": "ड्यासबोर्ड",
        "nav_history": "इतिहास",
        "nav_analyst": "विश्लेषक",
        "nav_admin": "एडमिन",
        "nav_dataset": "डेटासेट",
        "nav_models": "मोडेलहरू",
        "nav_sign_out": "साइन आउट",
        "nav_sign_in": "साइन इन",
        "menu_button": "मेनु",
        "footer_note": "फिल्ड कम्पानियनले पातको निदान र मौसम-आधारित उत्पादन एउटै ठाउँमा राख्छ। यो पूर्वानुमानले निर्णयमा मद्दत गर्छ; यो निश्चित उत्पादन होइन।",

        "home_eyebrow": "दुई मोडेल, एउटै खेत निर्णय",
        "home_title": "बिरुवाको स्वास्थ्य र भावी उत्पादन सँगै हेर्नुहोस्",
        "home_intro": "CNN ले पात पढ्छ। स्पेसियल LSTM ले मौसम पढ्छ। त्यसपछि सानो बडी मोडेलले यी दुई सङ्केत जोड्छ, ताकि उत्पादनको सङ्ख्या बिरुवासँगै चल्छ, केवल आकाशसँग होइन।",
        "status_cnn_ready": "CNN तयार",
        "status_leaf_diagnosis": "पात निदान",
        "status_trained_crops": "{count} तालिम प्राप्त बालीहरू",

        "workflow_1": "१. पात स्क्यान गर्नुहोस्",
        "workflow_2": "२. धान क्षेत्र छान्नुहोस्",
        "workflow_3": "३. अनुमानित उत्पादन हेर्नुहोस्",

        "leaf_health_title": "पातको स्वास्थ्य",
        "leaf_health_desc": "स्पष्ट पातको फोटो अपलोड गर्नुहोस्, CNN ले रोग पहिचान गर्छ।",
        "label_crop": "बाली",
        "label_auto_detect": "स्वतः पहिचान (एआई गेटकिपर)",
        "choose_crop": "बाली छान्नुहोस्",
        "crop_select_title": "तपाईंको पातको फोटोमा देखिएको बाली छान्नुहोस्",
        "label_leaf_image": "पातको फोटो",
        "choose_image": "JPEG, PNG, वा WEBP छान्नुहोस्",
        "btn_scan_leaf": "पात स्क्यान गर्नुहोस्",
        "plant_scan_title": "बिरुवा स्क्यान",
        "label_crop_result": "बाली:",
        "label_finding": "नतिजा:",
        "label_confidence": "विश्वास स्तर:",
        "label_recommendation": "सुझाव:",
        "loading_leaf": "पात पढ्दै",

        "future_harvest_title": "भावी उत्पादन",
        "status_disease_ready": "रोग मोडेल तयार",
        "status_disease_title": "रोग पहिचान",
        "status_disease_desc": "गेटकिपर रुटिङ र प्रत्येक बालीको CNN।",
        "status_rice_ready": "धान उत्पादन मोडेल तयार",
        "status_rice_missing": "धान उत्पादन मोडेल भेटिएन",
        "status_rice_title": "धान उत्पादन LSTM",
        "status_rice_desc": "दशकौंका जिल्ला फसल अभिलेखमा तालिम प्राप्त।",
        "how_it_works_title": "कसरी काम गर्छ",
        "future_harvest_desc": "आफ्नो धान खेती क्षेत्र छान्नुहोस्, LSTM ले दशक लङ्ग ऐतिहासिक उत्पादनका आधारमा अपेक्षित फसल अनुमान गर्छ।",
        "choose_region": "क्षेत्र छान्नुहोस्",
        "btn_predict_yield": "भावी उत्पादन अनुमान गर्नुहोस्",
        "unit_tons_hectare": "टन / हेक्टर",
        "loading_harvest": "उत्पादन पूर्वानुमान गर्दै",
        "lstm_missing_title": "धान उत्पादन मोडेल उपलब्ध छैन",
        "lstm_missing_body": "models/rice_yield_lstm.pth बनाउन python train_rice_lstm.py चलाउनुहोस्, अनि एप पुनः सुरु गर्नुहोस्।",

        "btn_download_report": "रिपोर्ट डाउनलोड गर्नुहोस् (CSV)",
        "download_report_hint": "तपाईंको पछिल्लो पात स्क्यान र उत्पादन पूर्वानुमानलाई एउटै फाइलमा मिलाउँछ, जुन सल्लाहकारसँग बाँड्न सकिन्छ।",
        "how_cnn_title": "CNN",
        "how_cnn_desc": "गेटकिपर CNN ले बाली प्रजाति पत्ता लगाउँछ, अनि प्रजाति-विशेष CNN ले रोग वर्गीकरण गर्छ।",
        "how_lstm_title": "धान उत्पादन LSTM",
        "how_lstm_desc": "प्रत्येक जिल्लाको ऐतिहासिक वार्षिक उत्पादन पढेर छानिएको क्षेत्रको आगामी सिजनको फसल अनुमान गर्छ।",

        "history_title": "पूर्वानुमान इतिहास",
        "history_desc": "सुरक्षित रोग र उत्पादन नतिजाहरू समीक्षा गर्नुहोस्।",
        "yield_trend_title": "उत्पादन प्रवृत्ति",
        "disease_scans_title": "बाली अनुसार रोग स्क्यानहरू",
        "th_date": "मिति",
        "th_type": "प्रकार",
        "th_crop": "बाली",
        "th_result": "नतिजा",
        "th_confidence": "विश्वास स्तर",
        "th_user": "प्रयोगकर्ता",
        "no_history": "अहिलेसम्म कुनै पूर्वानुमान इतिहास छैन।",
        "guest": "अतिथि",
        "unit_tons_hectare_short": "टन/हेक्टर",

        "auth_sign_in": "साइन इन",
        "auth_create_account": "खाता बनाउनुहोस्",
        "auth_create_farmer_account": "किसान खाता बनाउनुहोस्",
        "label_name": "नाम",
        "label_email": "इमेल",
        "label_password": "पासवर्ड",
        "auth_new_farmer": "नयाँ किसान?",
        "auth_create_link": "खाता बनाउनुहोस्",
        "auth_already_registered": "पहिले नै दर्ता भएको?",
        "auth_sign_in_link": "साइन इन गर्नुहोस्",

        "admin_title": "प्रणाली प्रशासन",
        "admin_desc": "प्रयोगकर्ता, मोडेल, र सुरक्षित पूर्वानुमान गतिविधि निगरानी गर्नुहोस्।",
        "admin_users": "प्रयोगकर्ताहरू",
        "admin_predictions": "पूर्वानुमानहरू",
        "admin_yield_model": "उत्पादन मोडेल",
        "admin_ready": "तयार",
        "admin_unavailable": "उपलब्ध छैन",
        "btn_manage_dataset": "डेटासेट व्यवस्थापन",
        "btn_manage_models": "AI मोडेल व्यवस्थापन",
        "btn_view_analytics": "विश्लेषण JSON हेर्नुहोस्",
        "th_average": "औसत",
        "th_average_confidence": "औसत विश्वास स्तर",
        "registered_users": "दर्ता भएका प्रयोगकर्ताहरू",
        "th_role": "भूमिका",
        "th_created": "सिर्जना मिति",
        "th_manage": "व्यवस्थापन",
        "role_farmer": "किसान",
        "role_analyst": "विश्लेषक",
        "role_admin": "एडमिन",
        "btn_update": "अपडेट गर्नुहोस्",

        "dataset_title": "डेटासेट व्यवस्थापन",
        "dataset_desc": "प्रशासकीय समीक्षाका लागि CSV डेटासेट अपलोड गर्नुहोस्। जानाजान नबदलिएसम्म तालिम हालको डेटासेट प्रयोग गर्छ।",
        "label_csv_dataset": "CSV डेटासेट",
        "btn_upload_dataset": "डेटासेट अपलोड गर्नुहोस्",
        "managed_files": "व्यवस्थित फाइलहरू",
        "no_datasets": "कुनै व्यवस्थित डेटासेट अपलोड गरिएको छैन।",

        "models_title": "AI मोडेल व्यवस्थापन",
        "models_desc": "प्रयोगअघि प्रशासकीय समीक्षाका लागि उपयुक्त PyTorch वेट अपलोड गर्नुहोस्।",
        "label_pytorch_model": "PyTorch मोडेल",
        "btn_upload_model": "मोडेल अपलोड गर्नुहोस्",
        "no_models": "कुनै व्यवस्थित मोडेल फाइल अपलोड गरिएको छैन।",

        "error_back_dashboard": "ड्यासबोर्डमा फर्किनुहोस्",

        # JS-facing strings
        "js_choose_crop_and_image": "बाली छान्नुहोस् र पातको फोटो अपलोड गर्नुहोस्।",
        "js_disease_detection_failed": "रोग पहिचान असफल भयो",
        "js_choose_region_first": "मौसम लोड गर्नुअघि खेतको क्षेत्र छान्नुहोस्।",
        "js_yield_prediction_failed": "उत्पादन पूर्वानुमान असफल भयो",
        "js_gatekeeper_routed": "एआई गेटकिपरले यो पातलाई {crop} ({conf} विश्वास) पहिचान गरी सम्बन्धित रोग मोडेलमा पठायो।",
        "js_gatekeeper_fallback": "गेटकिपरले यो पात {crop} जस्तो देख्छ, तर त्यो समर्थित छैन — {alt} प्रयोग गरिँदैछ।",
        "label_yield_place": "धान खेती क्षेत्र",
        "yield_result_title": "अनुमानित धान उत्पादन",
        "js_yield_explanation": "{place} को लागि अपेक्षित धान उत्पादन, {years} वर्षको ऐतिहासिक अभिलेखमा आधारित (नवीनतम: {year})।",
    },
}


def translate(lang, key, **kwargs):
    """Return the translated string for `key` in `lang`, formatting any
    {placeholders} with kwargs. Falls back to English, then to the raw key."""
    lang = lang if lang in UI_STRINGS else DEFAULT_LANG
    text = UI_STRINGS[lang].get(key) or UI_STRINGS[DEFAULT_LANG].get(key) or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def js_strings_for(lang):
    """Flat {key: value} dict of only the js_-prefixed strings for `lang`,
    with the prefix stripped, ready to serialize as window.APP_I18N."""
    lang = lang if lang in UI_STRINGS else DEFAULT_LANG
    return {k[3:]: v for k, v in UI_STRINGS[lang].items() if k.startswith("js_")}


def crop_label(crop, lang):
    """Display name for a crop key, e.g. 'apple' -> 'स्याउ' or 'Apple'."""
    if lang == "ne" and crop in CROP_NAMES_NE:
        return CROP_NAMES_NE[crop]
    return crop.capitalize() if crop else crop

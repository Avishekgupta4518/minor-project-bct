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
    "Squash___Powdery_mildew": "स्क्वासको धुलो ढुसी रोग",
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
    "Squash___Powdery_mildew": "बिरुवाबीचको दूरी र हावा-प्रवाह सुधार्नुहोस्। सेतो थोप्ला देखिनासाथ सल्फर वा पोटासियम बाइकार्बोनेट स्प्रे प्रयोग गर्नुहोस्।",
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
        "home_intro": "The CNN reads the leaf. The spatial LSTM reads the weather. A small buddy model then joins those two signals so the harvest number moves with the plant, not only with the sky.",
        "status_cnn_ready": "CNN ready",
        "status_leaf_diagnosis": "Leaf diagnosis",
        "status_trained_crops": "{count} trained crops",
        "status_lstm_ready": "LSTM ready",
        "status_lstm_missing": "LSTM missing",
        "status_spatial_forecast": "Spatial paddy forecast",
        "status_12step": "12-step future weather",
        "status_buddy_ready": "Buddy ready",
        "status_buddy_train": "Train buddy",
        "status_plant_weather_link": "Plant–weather link",
        "status_cnn_lstm_fusion": "CNN + LSTM fusion",

        "workflow_1": "1. Scan a leaf",
        "workflow_2": "2. Load field weather",
        "workflow_3": "3. Read the joined forecast",

        "leaf_health_title": "Leaf health",
        "leaf_health_desc": "Upload a clear leaf photo. This CNN result is saved and later used by the yield buddy.",
        "label_crop": "Crop",
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
        "future_harvest_desc": "Use a Nepal agricultural region forecast or your own measurements. The spatial LSTM predicts weather yield; the buddy then adjusts it with plant health.",
        "label_yield_crop": "Crop for this forecast",
        "same_as_scan": "Same as leaf scan, or choose",
        "label_field_region": "Field region",
        "choose_region": "Choose a region",
        "btn_load_forecast": "Load 12-step forecast",
        "label_temperature": "Temperature (°C)",
        "tip_temperature": "Average air temperature in °C for your field right now",
        "label_rainfall": "Rainfall (mm)",
        "tip_rainfall": "Rainfall in millimeters over the recent period",
        "label_humidity": "Humidity (%)",
        "tip_humidity": "Relative air humidity as a percentage",
        "label_soil_moisture": "Soil moisture (%)",
        "tip_soil_moisture": "Soil moisture as a percentage",
        "btn_predict_yield": "Predict future yield",
        "joined_forecast_title": "Joined forecast",
        "label_weather_lstm": "Weather LSTM",
        "label_buddy_adjustment": "Buddy adjustment",
        "label_relationship": "Relationship",
        "label_coverage": "Coverage",
        "unit_tons_hectare": "tons / hectare",
        "loading_harvest": "Forecasting harvest",
        "lstm_missing_title": "Spatial LSTM is not available",
        "lstm_missing_body": "Place spatial_paddy_lstm_final.pth in the models folder and restart the app.",

        "btn_download_report": "Download Report (CSV)",
        "download_report_hint": "Combines your latest leaf scan and yield forecast into one file to save or share with an advisor.",

        "how_buddy_title": "How the buddy works",
        "how_cnn_title": "CNN",
        "how_cnn_desc": "Classifies disease from the leaf and produces a plant-health score.",
        "how_lstm_title": "Spatial LSTM",
        "how_lstm_desc": "Reads 33 features per weather step, including location, crop, and plant signals, then forecasts yield.",
        "how_fusion_title": "Buddy fusion",
        "how_fusion_desc": "A small network learns how plant stress should raise or lower the weather-only harvest number.",

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
        "admin_buddy_on": "Buddy on",
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
        "js_weather_lookup_failed": "Live weather lookup failed",
        "js_weather_loaded": "Loaded a 12-step future forecast for {location}.",
        "js_weather_manual": "Using the values you typed. Load a region forecast for a true future sequence.",
        "js_weather_source_default": "Load live weather for the coming hours, then predict the future harvest.",
        "js_enter_all_weather": "Enter all weather values or load a region forecast.",
        "js_yield_prediction_failed": "Yield prediction failed",
        "js_relationship_aligned": "Aligned",
        "js_relationship_weather_only": "Weather only",
        "js_relationship_plant_supports_weather": "Plant supports weather",
        "js_relationship_disease_reduces_yield": "Disease reduces yield",
        "js_relationship_weak_shift": "Small shift",
        "js_relationship_mixed_signals": "Mixed signals",
        "js_quality_strong": "Strong outlook.",
        "js_quality_usable": "Usable outlook.",
        "js_quality_moderate": "Moderate outlook.",
        "js_quality_low": "Low outlook.",
        "js_buddy_used_both": "The buddy used both the leaf scan and the weather LSTM.",
        "js_buddy_weather_only": "No leaf scan was attached, so this is mostly a weather forecast.",
        "js_buddy_note_healthy": "This scan looks healthy. The yield buddy will support the weather forecast.",
        "js_buddy_note_sick": "This scan found a problem. The yield buddy will lower the weather-only harvest number.",
        "js_explanation_full": "Weather LSTM estimated {lstm} t/ha. After plant health was included, the joined forecast is {fused} t/ha ({direction} {delta}). Compare this with your field notes before acting.",
        "js_explanation_weather_only": "Scan a leaf first so the buddy can move this {fused} t/ha weather forecast with actual plant health.",
        "js_direction_up": "up",
        "js_direction_down": "down",
        "js_coverage_12steps": "12 future steps",
        "js_coverage_manual": "Manual input",
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
        "status_lstm_ready": "LSTM तयार",
        "status_lstm_missing": "LSTM उपलब्ध छैन",
        "status_spatial_forecast": "स्पेसियल धान पूर्वानुमान",
        "status_12step": "१२-चरण भावी मौसम",
        "status_buddy_ready": "बडी तयार",
        "status_buddy_train": "बडी तालिम गर्नुहोस्",
        "status_plant_weather_link": "बिरुवा–मौसम सम्बन्ध",
        "status_cnn_lstm_fusion": "CNN + LSTM संयोजन",

        "workflow_1": "१. पात स्क्यान गर्नुहोस्",
        "workflow_2": "२. खेतको मौसम लोड गर्नुहोस्",
        "workflow_3": "३. संयुक्त पूर्वानुमान हेर्नुहोस्",

        "leaf_health_title": "पातको स्वास्थ्य",
        "leaf_health_desc": "स्पष्ट पातको फोटो अपलोड गर्नुहोस्। यो CNN नतिजा सुरक्षित गरिन्छ र पछि उत्पादन बडीले प्रयोग गर्छ।",
        "label_crop": "बाली",
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
        "future_harvest_desc": "नेपालको कृषि क्षेत्रको पूर्वानुमान वा आफ्नै मापन प्रयोग गर्नुहोस्। स्पेसियल LSTM ले मौसम-आधारित उत्पादन अनुमान गर्छ; त्यसपछि बडीले बिरुवाको स्वास्थ्य अनुसार समायोजन गर्छ।",
        "label_yield_crop": "यो पूर्वानुमानको लागि बाली",
        "same_as_scan": "पात स्क्यान जस्तै, वा छान्नुहोस्",
        "label_field_region": "खेतको क्षेत्र",
        "choose_region": "क्षेत्र छान्नुहोस्",
        "btn_load_forecast": "१२-चरण पूर्वानुमान लोड गर्नुहोस्",
        "label_temperature": "तापक्रम (°C)",
        "tip_temperature": "अहिले तपाईंको खेतको औसत हावा तापक्रम °C मा",
        "label_rainfall": "वर्षा (mm)",
        "tip_rainfall": "हालैको अवधिमा भएको वर्षा मिलिमिटरमा",
        "label_humidity": "आद्रता (%)",
        "tip_humidity": "सापेक्ष हावा आद्रता प्रतिशतमा",
        "label_soil_moisture": "माटोको चिस्यान (%)",
        "tip_soil_moisture": "माटोको चिस्यान प्रतिशतमा",
        "btn_predict_yield": "भावी उत्पादन अनुमान गर्नुहोस्",
        "joined_forecast_title": "संयुक्त पूर्वानुमान",
        "label_weather_lstm": "मौसम LSTM",
        "label_buddy_adjustment": "बडी समायोजन",
        "label_relationship": "सम्बन्ध",
        "label_coverage": "कभरेज",
        "unit_tons_hectare": "टन / हेक्टर",
        "loading_harvest": "उत्पादन पूर्वानुमान गर्दै",
        "lstm_missing_title": "स्पेसियल LSTM उपलब्ध छैन",
        "lstm_missing_body": "models फोल्डरमा spatial_paddy_lstm_final.pth राख्नुहोस् र एप पुनः सुरु गर्नुहोस्।",

        "btn_download_report": "रिपोर्ट डाउनलोड गर्नुहोस् (CSV)",
        "download_report_hint": "तपाईंको पछिल्लो पात स्क्यान र उत्पादन पूर्वानुमानलाई एउटै फाइलमा मिलाउँछ, जुन सल्लाहकारसँग बाँड्न सकिन्छ।",

        "how_buddy_title": "बडीले कसरी काम गर्छ",
        "how_cnn_title": "CNN",
        "how_cnn_desc": "पातबाट रोग वर्गीकरण गर्छ र बिरुवा-स्वास्थ्य स्कोर उत्पादन गर्छ।",
        "how_lstm_title": "स्पेसियल LSTM",
        "how_lstm_desc": "प्रत्येक मौसम चरणमा ३३ विशेषता पढ्छ, जसमा स्थान, बाली, र बिरुवा सङ्केत समावेश छन्, अनि उत्पादन अनुमान गर्छ।",
        "how_fusion_title": "बडी संयोजन",
        "how_fusion_desc": "सानो नेटवर्कले बिरुवाको तनावले मौसम-मात्र उत्पादन सङ्ख्यालाई कसरी बढाउने वा घटाउने भन्ने कुरा सिक्छ।",

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
        "admin_buddy_on": "बडी सक्रिय",
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
        "js_weather_lookup_failed": "प्रत्यक्ष मौसम खोजी असफल भयो",
        "js_weather_loaded": "{location} को लागि १२-चरण भावी पूर्वानुमान लोड गरियो।",
        "js_weather_manual": "तपाईंले टाइप गरेका मानहरू प्रयोग गर्दै। साँचो भावी अनुक्रमका लागि क्षेत्र पूर्वानुमान लोड गर्नुहोस्।",
        "js_weather_source_default": "आगामी घण्टाहरूको लागि प्रत्यक्ष मौसम लोड गर्नुहोस्, त्यसपछि भावी उत्पादन अनुमान गर्नुहोस्।",
        "js_enter_all_weather": "सबै मौसम मान भर्नुहोस् वा क्षेत्र पूर्वानुमान लोड गर्नुहोस्।",
        "js_yield_prediction_failed": "उत्पादन पूर्वानुमान असफल भयो",
        "js_relationship_aligned": "मिल्दो",
        "js_relationship_weather_only": "मौसम मात्र",
        "js_relationship_plant_supports_weather": "बिरुवाले मौसमलाई समर्थन गर्छ",
        "js_relationship_disease_reduces_yield": "रोगले उत्पादन घटाउँछ",
        "js_relationship_weak_shift": "सानो परिवर्तन",
        "js_relationship_mixed_signals": "मिश्रित सङ्केत",
        "js_quality_strong": "बलियो सम्भावना।",
        "js_quality_usable": "प्रयोगयोग्य सम्भावना।",
        "js_quality_moderate": "मध्यम सम्भावना।",
        "js_quality_low": "कमजोर सम्भावना।",
        "js_buddy_used_both": "बडीले पात स्क्यान र मौसम LSTM दुवै प्रयोग गर्यो।",
        "js_buddy_weather_only": "कुनै पात स्क्यान संलग्न गरिएको छैन, त्यसैले यो प्रायः मौसम-मात्र पूर्वानुमान हो।",
        "js_buddy_note_healthy": "यो स्क्यान स्वस्थ देखिन्छ। उत्पादन बडीले मौसम पूर्वानुमानलाई समर्थन गर्नेछ।",
        "js_buddy_note_sick": "यो स्क्यानमा समस्या फेला पर्यो। उत्पादन बडीले मौसम-मात्र उत्पादन सङ्ख्या घटाउनेछ।",
        "js_explanation_full": "मौसम LSTM ले {lstm} टन/हेक्टर अनुमान गर्यो। बिरुवाको स्वास्थ्य समावेश गरेपछि, संयुक्त पूर्वानुमान {fused} टन/हेक्टर हो ({direction} {delta})। कारबाही गर्नुअघि यसलाई आफ्नो खेतको नोटसँग तुलना गर्नुहोस्।",
        "js_explanation_weather_only": "बडीले यो {fused} टन/हेक्टर मौसम पूर्वानुमानलाई वास्तविक बिरुवा स्वास्थ्यसँग मिलाउन पहिले पात स्क्यान गर्नुहोस्।",
        "js_direction_up": "बढेको",
        "js_direction_down": "घटेको",
        "js_coverage_12steps": "१२ भावी चरण",
        "js_coverage_manual": "म्यानुअल इनपुट",
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

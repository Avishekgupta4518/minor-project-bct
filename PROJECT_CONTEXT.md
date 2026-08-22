> **⚠️ Superseded.** This document is the original lab-derived build specification
> (SRS/DFD/UML from Labs 1–3), kept for historical reference only. The system has since
> evolved beyond it — most notably, disease detection is a two-stage Gatekeeper→Species-CNN
> pipeline, and yield prediction now runs through a `SpatialPaddyLSTM` + `BuddyFusionNet`
> fusion, not the single plain LSTM described below. **See `README.md` for the current,
> accurate architecture and status.** Sections 12 and 13 below ("Task List" and "Known Gaps")
> describe an earlier project state and are now resolved — auth, prediction history, and
> role-based admin/analyst views are all implemented; see `IMPLEMENTATION_STATUS` history in
> git for that resolution, and `README.md` for what exists today.

---

# Project Context Document
## Smart Multi-Crop Disease Detection and Yield Prediction using CNN and LSTM Models

This document consolidates the SRS (Lab 1), DFD (Lab 2), and UML (Lab 3) into a single
build specification. It is written so that any LLM/coding agent can read it and know
exactly what to implement without needing the original lab PDFs.

---

## 1. System Overview

An AI-based agricultural decision-support web application with two independent ML
pipelines feeding into one combined dashboard:

1. **Disease Detection** — CNN classifies crop disease from an uploaded leaf image.
2. **Yield Prediction** — LSTM predicts crop yield from environmental time-series data
   (temperature, rainfall, humidity).

Results from both are aggregated and shown to the user in a web dashboard.

**Out of scope:** IoT sensor integration, automated pesticide spraying, market price
prediction, ER modeling, deployment/component diagrams, detailed DB schema.

---

## 2. Actors

| Actor | Role |
|---|---|
| **Farmer** | Primary user. Uploads leaf images, enters environmental data, views predictions, views dashboard and prediction history. |
| **Agricultural Analyst** | Analyzes prediction results and system output quality. |
| **System Administrator** | Manages datasets, AI models, users, monitors system. |

---

## 3. Features / Use Cases (from UML Use Case Diagram)

- Upload Crop/Leaf Image
- Detect Crop Disease *(includes: Upload Crop Image)*
- Enter Environmental Data
- Predict Crop Yield *(includes: Enter Environmental Data)*
- View Prediction Result *(includes: Detect Crop Disease, Predict Crop Yield)*
- View Dashboard
- View Prediction History
- Analyze Prediction Results *(Agricultural Analyst)*
- Manage Dataset *(Admin)*
- Manage AI Models *(Admin)*
- Manage Users *(Admin)*
- Monitor System *(Admin)*

---

## 4. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-1 | Accept crop leaf images as input for disease detection | High |
| FR-2 | Preprocess input images for CNN model prediction | High |
| FR-3 | Classify crop diseases using a trained CNN model | High |
| FR-4 | Display disease prediction results with confidence scores | High |
| FR-5 | Accept environmental data for yield prediction | High |
| FR-6 | Predict crop yield using an LSTM model | High |
| FR-7 | Provide a dashboard to display results and analysis | Medium |
| FR-8 | Store prediction history for future reference | Low |

## 5. Non-Functional Requirements

| ID | Requirement | Category |
|---|---|---|
| NFR-1 | Return disease prediction results within 3 seconds | Performance |
| NFR-2 | Achieve >85% prediction accuracy on trained datasets | Accuracy |
| NFR-3 | Accessible via standard web browsers, no install | Usability |
| NFR-4 | Secure handling of user input data | Security |
| NFR-5 | Scalable to support additional crop types later | Scalability |

---

## 6. Data Flow (from DFD Levels 0–2)

### Level 0 (Context)
- **Farmer → System:** crop leaf images, environmental data
- **System → Farmer:** disease classification + confidence, yield prediction, dashboard
- **Admin → System:** pretrained AI models (model upload)
- **System → Admin:** system logs & status

### Level 1 (Major sub-processes)
1. **Authenticate User** — verifies farmer/admin session (data store: `D1 DataStore`)
2. **Classify Leaf Image** — reads CNN weights (`D2 Pre-trained Weights`), runs CNN, saves result to `D3 Prediction History`
3. **Predict Crop Yield** — reads LSTM weights (`D2`), runs LSTM on weather params, saves forecast metric to `D3`
4. **Display Analytics Dashboard** — fetches past results from `D3`, presents disease + yield data to Farmer, diagnostic logs to Admin

### Level 2 (expansion of "Classify Leaf Image", i.e. CNN pipeline)
1. **2.1 Receive & Resize Image** — standardize uploaded image
2. **2.2 Convert to Numerical Array** — produce normalized/preprocessed tensor
3. **2.3 Run CNN Inference Model** — reads pretrained weights, outputs raw probability vector
4. **2.4 Map Disease Label & Confidence** — maps vector to class label, saves to Prediction History, sends label to dashboard

*(Equivalent Level 2 also exists for the LSTM pipeline: 3.1 Parse Environmental Inputs → 3.2 Scale Features & Sequences → 3.3 Run LSTM Inference → 3.4 Compile Numerical Forecast → save to Prediction History → send to dashboard.)*

**Data stores:**
- `D1` — session/auth data store
- `D2` — pretrained CNN + LSTM weights
- `D3` — prediction history (disease results + yield forecasts)

---

## 7. Class Structure (from UML Class Diagram)

```
User (base)
  -userId: int, -name, -email, -password, -role
  +login(), +logout()
  ├── Farmer
  │     -farmLocation: String, -cropType: String
  │     +uploadImage(), +enterEnvironmentalData(), +viewPrediction()
  │     ── 1:* → CropImage
  │     ── 1:* → EnvironmentalData
  │
  ├── AgriculturalAnalyst
  │     -department: String
  │     +analyzeResults(), +viewPredictionHistory()
  │     ── 1:* → PredictionResult
  │
  └── SystemAdministrator
        -adminLevel: int
        +manageDataset(), +manageAIModels(), +manageUsers()

CropImage
  -imageId: int, -imagePath: String, -uploadDate: Date
  +uploadImage()
  ── 1:* → DiseaseDetectionModel

DiseaseDetectionModel
  -modelName: String, -modelType: "CNN", -version: String
  +detectDisease()
  ── 1:* → PredictionResult

EnvironmentalData
  -temperature: float, -humidity: float, -rainfall: float, -soilMoisture: float
  +collectData()
  ── 1:* → YieldPredictionModel

YieldPredictionModel
  -modelName: String, -modelType: "LSTM", -version: String
  +predictYield()
  ── 1:* → PredictionResult

PredictionResult
  -diseaseName: String, -confidence: float, -predictedYield: float, -date: Date
  +generateReport()
```

---

## 8. Sequence of Operations (from UML Sequence Diagram)

```
Farmer -> System: login()
Farmer -> System: uploadImage()
System -> CropImage: storeImage()
CropImage -> CNNModel: detectDisease()
CNNModel -> System: returnDiseaseResult()

Farmer -> System: enterEnvironmentalData()
System -> LSTMModel: predictYield()
LSTMModel -> System: returnYieldPrediction()

System -> PredictionResult: generateResult()
PredictionResult -> System: returnResult()
System -> Farmer: displayPrediction()
```

---

## 9. Software Process Model

**Waterfall**: Requirements → System Design → Implementation → Testing → Deployment → Maintenance.
Chosen because requirements are stable and the architecture is cleanly modular (CNN module, LSTM module, integration layer, UI).

---

## 10. Technology Stack (from SRS Software Interfaces)

- **Backend:** Python, Flask (web framework)
- **ML frameworks:** PyTorch (CNN — actual implementation) + Keras/TensorFlow (LSTM — actual implementation)
- **Communication:** HTTP/HTTPS between browser client and Flask backend
- **Hardware:** standard laptop/desktop; GPU preferred for training/inference

---

## 11. Actual Implementation Status (as built, differs slightly from SRS's generic "TensorFlow/Keras for both")

- **Disease detection is two-stage, not single-CNN:**
  1. **Gatekeeper** (EfficientNet-B0, PyTorch/timm) — classifies plant **species** (14 classes) from the leaf image.
  2. **Species-specific CNN** (custom `PlantDiseaseCNN`, PyTorch) — one model per species (12 trained), classifies the **specific disease** within that species. This refines DFD Process 2.0 into two chained inference steps, not one.
- **Yield prediction:** Keras/TensorFlow LSTM, trained on temperature/rainfall/humidity sequences (`SEQ_LEN=10` timesteps).
- **Files already built:**
  - `models.py` — PyTorch model defs (`PlantDiseaseCNN`, gatekeeper loader)
  - `inference.py` — two-stage `DiseasePredictor` class (Gatekeeper → Species CNN)
  - `inference_config.json` — species/class order mapping (must be verified against notebook `class_to_idx` output before use)
  - `train_lstm_yield.py` — LSTM training script (Colab-ready, synthetic-data fallback)
  - `app.py` — Flask app wiring image upload → `DiseasePredictor`, form input → LSTM yield prediction, renders combined result
  - `templates/index.html`, `static/style.css` — dashboard UI
  - `requirements.txt`, `SETUP.md` — install/run instructions

---

## 12. Task List (for an LLM/agent picking this up fresh)

If handed only this document, here is what still needs doing, in order:

1. **Verify `inference_config.json`** against the actual notebooks (`gatekeeper-2.ipynb` cell with `class_to_idx`, `plant-disease-3.ipynb` per-species `val_loader.dataset.classes`). This is the single most likely source of silent bugs.
2. **Export all trained weights** as `.pth` files into a `weights/` folder (gatekeeper + 12 species CNNs).
3. **Run `train_lstm_yield.py`** to produce `lstm_model.h5`, `scaler_x.pkl`, `scaler_y.pkl`.
4. **Assemble the folder structure** exactly as described in `SETUP.md`.
5. **Implement authentication (`D1 DataStore` / User.login/logout)** — not yet built; currently the app has no login system, so FR/DFD's "Authenticate User" process is a gap versus the SRS/DFD if login is required for grading.
6. **Implement Prediction History (`D3`)** — not yet built; `PredictionResult` persistence (FR-8, DFD data store D3, UML class `PredictionResult`) is not implemented in `app.py`. Add a simple DB (SQLite is enough) or in-memory store if time-constrained.
7. **Implement role-based views** for Agricultural Analyst / System Administrator (`analyzeResults()`, `manageDataset()`, `manageAIModels()`, `manageUsers()`) — currently only the Farmer flow (upload image + enter env data + view result) is built.
8. **Test end-to-end**: upload a known image, confirm species+disease match; submit weather values, confirm a yield number returns without error.
9. **(Optional, if time allows)** Add dashboard visualization (charts of yield trend, disease history) to satisfy FR-7 more fully — currently the UI shows only the latest single result, not historical charts.

---

## 13. Known Gaps vs. Documentation (be upfront about these if asked)

- No login/authentication system exists yet — DFD's Process 1.0 and UML's `User.login()` are documented but not coded.
- No persistent prediction history / database — FR-8 and UML's `PredictionResult` storage are documented but not coded; only the latest prediction is shown per request.
- No Admin or Analyst UI — only the Farmer-facing upload+predict flow exists.
- LSTM is trained on synthetic data unless a real yield CSV is supplied — flag this honestly in any viva/demo.

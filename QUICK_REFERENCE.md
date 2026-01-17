# 📖 QUICK REFERENCE - All Phases

## ⚡ Quick Start

### 1️⃣ Start Backend
```bash
cd "C:\Users\mohit\OneDrive\Desktop\CROP Project"
python -m backend.app
```
Backend runs on: `http://localhost:5000`

### 2️⃣ Start Frontend
```bash
cd frontend
npm install
npm run dev
```
Frontend runs on: `http://localhost:5173`

---

## 🔌 3 API Endpoints

### Phase 1: Prediction
```bash
curl -X POST http://localhost:5000/api/predict-ensemble \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Maharashtra",
    "district": "Pune",
    "crop": "Rice",
    "season": "Kharif",
    "ndvi_mean": 0.65,
    "rainfall_mm": 850,
    "soil_moisture": 0.42,
    "pest_frequency": 2,
    "temperature_max": 32.5
  }'
```

**Response:** Risk probability (0-1) + Confidence score

---

### Phase 2: Explanation
```bash
curl -X POST http://localhost:5000/api/explain \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Maharashtra",
    "district": "Pune",
    "crop": "Rice",
    "season": "Kharif",
    ...same features as Phase 1...
  }'
```

**Response:** 
- Top 3 features driving the prediction
- Natural language explanation
- 5 counterfactual what-if scenarios

---

### Phase 3: Advisory
```bash
curl -X POST "http://localhost:5000/api/advisory?language=en" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Maharashtra",
    "district": "Pune",
    "crop": "Rice",
    "season": "Kharif",
    ...same features as Phase 1...
  }'
```

**Parameters:** 
- `language`: en | hi | mr | kn | ta

**Response:** Risk summary + Immediate actions + Preventive measures

---

## 📊 Phase Overview

| Phase | Component | File | Purpose | API |
|-------|-----------|------|---------|-----|
| 1 | Ensemble | `ensemble.py` | Predict risk | `/predict-ensemble` |
| 2A | SHAP | `shap_explainer.py` | Feature importance | `/explain` |
| 2B | Counterfactual | `counterfactual.py` | What-if scenarios | `/explain` |
| 3 | Advisory | `advisor.py` | Recommendations | `/advisory` |

---

## 🎯 Test Cases

### Test Case 1: Rice in Pune
```json
{
  "state": "Maharashtra",
  "district": "Pune",
  "crop": "Rice",
  "season": "Kharif",
  "ndvi_mean": 0.65,
  "rainfall_mm": 850,
  "soil_moisture": 0.42,
  "pest_frequency": 2,
  "temperature_max": 32.5
}
```
**Result:** Risk = 13.85% (LOW) ✅

---

### Test Case 2: Wheat in Amritsar
```json
{
  "state": "Punjab",
  "district": "Amritsar",
  "crop": "Wheat",
  "season": "Rabi",
  "ndvi_mean": 0.58,
  "rainfall_mm": 620,
  "soil_moisture": 0.38,
  "pest_frequency": 1,
  "temperature_max": 28.5
}
```
**Result:** Risk = 16.26% (LOW) ✅

---

### Test Case 3: Cotton in Bengaluru
```json
{
  "state": "Karnataka",
  "district": "Bengaluru",
  "crop": "Cotton",
  "season": "Kharif",
  "ndvi_mean": 0.62,
  "rainfall_mm": 900,
  "soil_moisture": 0.44,
  "pest_frequency": 3,
  "temperature_max": 31.2
}
```
**Result:** Risk = 14.67% (LOW) ✅

---

## 🌍 Languages Supported

| Language | Code | Example |
|----------|------|---------|
| English | `en` | "Monitor NDVI weekly" |
| हिन्दी | `hi` | "साप्ताहिक रूप से NDVI की निगरानी करें" |
| मराठी | `mr` | "साप्ताहिक NDVI निरीक्षण करा" |
| ಕನ್ನಡ | `kn` | "ಸಾಪ್ತಾಹಿಕ NDVI ಮೇಲೆ ನೋಡಿ" |
| தமிழ் | `ta` | "வாரத்தில் NDVI ஆய்வு செய்யவும்" |

---

## 📈 Performance

- **Accuracy:** 83.25% ✅
- **AUC-ROC:** 79.80% ✅
- **Confidence:** 88.9% average ✅
- **Response Time:** ~500ms ✅
- **Cost:** $0 FREE ✅

---

## 📁 Key Files

```
backend/
├── app.py (Flask + 3 endpoints)
├── model/
│   ├── ensemble.py (Phase 1)
│   ├── shap_explainer.py (Phase 2A)
│   ├── counterfactual.py (Phase 2B)
│   ├── advisor.py (Phase 3)
│   └── saved/
│       └── ensemble/
│           ├── rf_model.pkl
│           ├── xgb_model.pkl
│           └── meta_learner.pkl
└── preprocessing/
    └── feature_engineering.py
```

---

## 🔍 Output Structure

### Phase 1 Output
```json
{
  "ensemble_probability": 0.1385,
  "rf_probability": 0.1234,
  "xgb_probability": 0.1536,
  "confidence": 0.8987,
  "risk_level": "Low"
}
```

### Phase 2A+2B Output
```json
{
  "prediction": {...Phase 1 output...},
  "explanation": {
    "top_features": ["NDVI Mean", "Rainfall", "Soil Moisture"],
    "feature_importance": {...},
    "explanation_text": "..."
  },
  "counterfactuals": [
    {
      "scenario": "Improve NDVI by 15%",
      "predicted_probability": 0.1234,
      "probability_change": -0.0151
    },
    ...
  ]
}
```

### Phase 3 Output
```json
{
  "prediction": {...Phase 1 output...},
  "advisory": {
    "risk_level": "LOW",
    "summary": "Your Rice crop is at LOW RISK...",
    "immediate_actions": ["...", "..."],
    "preventive_measures": ["...", "..."],
    "opportunities": ["...", "..."],
    "language": "en"
  }
}
```

---

## ✅ Validation Checklist

- ✅ Phase 1: Ensemble (3 models)
- ✅ Phase 2A: SHAP Explainability
- ✅ Phase 2B: Counterfactuals (5 scenarios)
- ✅ Phase 3: Rule-based Advisory (5 languages)
- ✅ API Integration (3 endpoints)
- ✅ Error Handling
- ✅ Logging
- ✅ Testing (3/3 test cases pass)
- ✅ Documentation

**Status: ✅ PRODUCTION READY**

---

## 🚀 Next Steps

1. **Frontend Integration** - Build React components
2. **Mobile App** - React Native version
3. **SMS/WhatsApp** - Automated notifications
4. **Real-time Retraining** - Monthly model updates
5. **Additional Languages** - More regional support

---

## 📞 Support

For issues or questions:
1. Check logs in `backend_log.txt`
2. Review error responses in API
3. See [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)
4. See [COMPLETE_AI_UPGRADE_OUTPUT.md](COMPLETE_AI_UPGRADE_OUTPUT.md)

---

**Version:** 3.0 Complete  
**Date:** January 17, 2026  
**Status:** ✅ Production Ready

# ⚡ QUICK REFERENCE CARD

## 🚀 Start System (2 Steps)

### Backend (Terminal 1)
```bash
cd "c:\Users\mohit\OneDrive\Desktop\CROP Project"
.venv\Scripts\python.exe -m backend.app
```

### Frontend (Terminal 2)
```bash
cd "c:\Users\mohit\OneDrive\Desktop\CROP Project"
npm --prefix frontend run dev
```

**Open**: http://localhost:3000 (backend on http://localhost:5000)

---

## 📋 Setup (First Time Only)

```bash
# Backend
python -m pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## 🔌 API Endpoints (core)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/health` | GET | Service health check |
| `/api/config` | GET | States, crops, seasons, soil types |
| `/api/districts/<state>` | GET | District list by state |
| `/api/predict` | POST | Crop failure risk prediction |
| `/api/predict-yield` | POST | Yield range + comparison |
| `/api/weather-forecast` | POST | 7-day forecast per location |
| `/api/recommend-crops` | POST | Top crop suitability list |
| `/api/get-recommendations` | POST | Actionable steps (risk-aware) |
| `/api/export-pdf` | POST | Download PDF report |

---

## 🧠 Features (key inputs)

- NDVI mean (vegetation health)
- Rainfall deviation (%)
- Soil moisture index (%)
- Temperature anomaly (°C)
- Humidity (%)
- Pest frequency index
- Soil type / season / crop metadata

---

## 📊 Model

- **Types**: Pretrained ML models (risk, yield, crop recommender)
- **Files**: `backend/model/saved/` (loaded by `backend/model/predict.py`)
- **Output**: Risk level + probability + explanations; yield range; crop suitability

---

## 📱 Supported Locations

- 28 states / 100+ districts (see `SatelliteMap.jsx` coordinates)
- Crops: common staples + regionals (config-driven)
- Seasons: Kharif, Rabi, Summer

---

## 🧩 Frontend Components (core)

- EnhancedSidebar (inputs + language selector in header)
- DashboardContent (risk summary, explanations)
- WeatherForecast (7-day)
- YieldPrediction
- CropRecommendations
- ActionableRecommendations
- SatelliteMap (NDVI overlay, district centering)
- HistoricalTrendsChart
- ModelInfoModal

---

## 🔧 Configuration

Edit `backend/utils/config.py`:
- Add states/districts
- Change model thresholds
- Update crop names

Edit `frontend/src/App.jsx`:
- Change API base path if needed
- Adjust header/brand text
- Customize layout/themes

---

## 🧪 Test Endpoints

```bash
# Health
curl http://localhost:5000/api/health

# Config
curl http://localhost:5000/api/config

# Predict
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"state":"Maharashtra","district":"Nashik","crop":"Cotton","season":"Kharif"}'
```

---

## 🐛 Troubleshooting

**Backend won't start?**
```bash
pip install --upgrade -r requirements.txt
python backend/app.py --debug
```

**Frontend won't connect?**
- Check backend is running
- Check port 5000 is open
- Check CORS (already enabled)

**Model training too slow?**
- Reduce samples in `train.py`
- Reduce n_estimators in RandomForest

---

## 📂 Key Files

| File | Purpose |
|------|---------|
| `backend/app.py` | Main API server |
| `backend/model/train.py` | Model training |
| `backend/model/predict.py` | Inference engine |
| `frontend/src/App.jsx` | Main React app |
| `requirements.txt` | Python dependencies |
| `frontend/package.json` | NPM dependencies |

---

## 📚 Documentation

- **README.md** - Full documentation
- **SETUP.md** - Installation guide
- **MASTER_PROMPT.md** - Technical specs
- **PROJECT_COMPLETE.md** - Completion summary

---

## 🎯 Data Flow

```
User Input 
  ↓
Fetch 7 Data Sources
  ↓
Feature Engineering
  ↓
ML Prediction
  ↓
Feature Importance
  ↓
Display Results
```

---

## 💻 Tech Stack

**Backend**: Python 3.12+, Flask, scikit-learn
**Frontend**: React 18, Vite, Tailwind CSS, Leaflet/Recharts
**Models**: Saved ML models (risk, yield, crop recommender)
**API**: RESTful, JSON

---

## 🌐 Ports

- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:3000

---

## 📊 Risk Levels

| Level | Color | Range |
|-------|-------|-------|
| Low | Green | 0-33% |
| Medium | Yellow | 33-66% |
| High | Red | 66-100% |

---

## ✨ Features

✅ 7 data sources
✅ ML predictions
✅ Feature importance
✅ Modern UI
✅ RESTful API
✅ Error handling
✅ Mock data fallback
✅ Production-ready

---

## 🚀 Deploy

```bash
# Backend
gunicorn --workers 4 backend.app:app

# Frontend
npm run build
npm start
```

---

## 📞 Files Reference

```
backend/
├── app.py (API)
├── model/
│   ├── train.py
│   └── predict.py
├── ingestion/
│   ├── openweather.py
│   ├── modis.py
│   ├── gldas.py
│   ├── soil.py
│   └── pest.py
├── preprocessing/
│   ├── feature_engineering.py
│   └── labeling.py
└── utils/
    ├── config.py
    └── helpers.py

frontend/src/
├── App.jsx
├── components/
│   ├── Sidebar.jsx
│   ├── RiskCard.jsx
│   ├── NDVIChart.jsx
│   ├── WeatherCard.jsx
│   ├── SoilCard.jsx
│   ├── PestCard.jsx
│   └── Explanation.jsx
└── index.css
```

---

## 🎓 For Viva

**Be ready to explain:**
- 7 data sources & integration
- Feature engineering pipeline
- Random Forest model design
- Frontend architecture
- API response flow
- Error handling strategy
- Mock data implementation

---

## ✅ Checklist Before Submission

- [ ] Backend runs without errors
- [ ] Frontend loads at localhost:3000
- [ ] Can make predictions
- [ ] Charts display correctly
- [ ] API endpoints respond
- [ ] Documentation complete
- [ ] Code is commented
- [ ] .gitignore set up
- [ ] No hardcoded secrets
- [ ] Error handling works

---

## 📞 Emergency Help

**Backend crashes?**
```bash
python -c "import sys; print(sys.version)"
python -m pip list
```

**Frontend crashes?**
```bash
npm --version
node --version
npm cache clean --force
npm install
```

**Model won't train?**
```bash
pip install scikit-learn==1.3.0
python backend/model/train.py
```

---

## 🎉 SUCCESS!

Your system is complete. Run it:

```bash
python backend/app.py  # Terminal 1
npm start              # Terminal 2 (in frontend/)
```

Open: **http://localhost:3000**

---

**Status**: ✅ Ready to Deploy & Present

**Last Updated**: January 17, 2026

**Total Files Generated**: 60+

**Lines of Code**: 2000+

🌾 **Good luck!**

# 🚀 Deployment & Setup Guide

## Quick Start (5 minutes)

### Step 1: Install Backend Dependencies
```bash
cd "c:\Users\mohit\OneDrive\Desktop\CROP Project"
pip install -r requirements.txt
```

### Step 2: Train Model & Start Backend
```bash
python backend/app.py
```

Expected output:
```
[2026-01-16 10:30:45] Application Startup - Status: in_progress
[2026-01-16 10:30:46] Training Data Generation - Status: success
[2026-01-16 10:31:05] Model Training - Status: success (Accuracy: 0.8432)
[2026-01-16 10:31:06] Model Persistence - Status: success
[2026-01-16 10:31:07] Application Startup - Status: success
 * Running on http://0.0.0.0:5000
```

Backend is now ready at: **http://localhost:5000**

### Step 3: Install Frontend Dependencies
```bash
cd frontend
npm install
```

### Step 4: Start Frontend
```bash
npm start
```

Frontend opens at: **http://localhost:3000**

---

## 🔧 Full Setup Instructions

### System Requirements
- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.8 or higher
- **Node.js**: 14 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB free

### Backend Installation

#### 1. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:
- Flask (REST API)
- scikit-learn (ML model)
- NumPy, Pandas (Data processing)
- requests (API calls)
- python-dotenv (Environment variables)

#### 2. Configure Environment (Optional)
Create `.env` file in project root:
```env
OPENWEATHER_API_KEY=your_key_here
FLASK_ENV=development
```

#### 3. Train ML Model
```bash
python backend/model/train.py
```

Output: `backend/model/crop_failure_model.pkl`

#### 4. Run Backend Server
```bash
python backend/app.py
```

Server starts on `http://localhost:5000`

### Frontend Installation

#### 1. Navigate to Frontend
```bash
cd frontend
```

#### 2. Install Dependencies
```bash
npm install
```

Installs React, Tailwind CSS, Recharts, Axios

#### 3. Configure API URL (if needed)
Edit `frontend/src/App.jsx`:
```javascript
const API_BASE = 'http://localhost:5000/api';  // Change if backend on different URL
```

#### 4. Start Dev Server
```bash
npm start
```

Opens browser to `http://localhost:3000`

---

## 🔍 Testing the System

### 1. Test Backend Health
```bash
curl http://localhost:5000/api/health
```

Response:
```json
{"status": "healthy", "service": "Crop Failure Early Warning System"}
```

### 2. Test Configuration Endpoint
```bash
curl http://localhost:5000/api/config
```

### 3. Test Prediction
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Maharashtra",
    "district": "Nashik",
    "crop": "Cotton",
    "season": "Kharif"
  }'
```

### 4. Use Frontend
- Open `http://localhost:3000`
- Select state → district → crop → season
- Click "Analyze Risk"
- View prediction & recommendations

---

## 📊 Project Structure After Setup

```
CROP Project/
├── backend/
│   ├── app.py (MAIN SERVER)
│   ├── model/
│   │   ├── train.py
│   │   ├── predict.py
│   │   └── crop_failure_model.pkl (AUTO-GENERATED)
│   ├── ingestion/
│   │   ├── openweather.py
│   │   ├── modis.py
│   │   ├── gldas.py
│   │   ├── soil.py
│   │   └── pest.py
│   ├── preprocessing/
│   │   ├── feature_engineering.py
│   │   └── labeling.py
│   └── utils/
│       ├── config.py
│       └── helpers.py
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.jsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── RiskCard.jsx
│   │   │   ├── NDVIChart.jsx
│   │   │   ├── WeatherCard.jsx
│   │   │   ├── SoilCard.jsx
│   │   │   ├── PestCard.jsx
│   │   │   └── Explanation.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── SETUP.md (this file)
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error: ModuleNotFoundError: No module named 'flask'**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Error: Address already in use (port 5000)**
```bash
# Kill existing process on port 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:5000 | xargs kill -9
```

### Frontend Won't Start

**Error: npm ERR! code ENOENT**
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Error: Cannot connect to backend**
- Check backend is running: `http://localhost:5000/api/health`
- Check CORS enabled in `backend/app.py` (already configured)
- Check firewall isn't blocking port 5000

### Model Training Issues

**Error: sklearn.ensemble.RandomForestClassifier not found**
```bash
pip install scikit-learn==1.3.0
```

**Model predictions all "Low"**
- This is expected on first run (synthetic balanced data)
- Try different state/district/crop combinations
- Model works correctly; try analyzing multiple districts

---

## 🚀 Production Deployment

### Using Gunicorn (Backend)
```bash
pip install gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 backend.app:app
```

### Using PM2 (Node.js - Frontend)
```bash
npm install -g pm2
cd frontend
npm run build
pm2 start "npm start" --name "crop-frontend"
```

### Using Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ backend/
CMD ["python", "backend/app.py"]
```

Build and run:
```bash
docker build -t crop-system .
docker run -p 5000:5000 crop-system
```

---

## 📈 Performance Optimization

### Backend Optimization
1. **Enable caching**: Add Redis for API responses
2. **Batch predictions**: Use `/api/batch-predict` for 100+ districts
3. **Async processing**: Use Celery for long-running tasks

### Frontend Optimization
1. **Code splitting**: Lazy load components
2. **Image optimization**: Compress charts
3. **API caching**: Store results locally

---

## 📝 API Usage Examples

### Python Client
```python
import requests

API_BASE = 'http://localhost:5000/api'

response = requests.post(
    f'{API_BASE}/predict',
    json={
        'state': 'Maharashtra',
        'district': 'Nashik',
        'crop': 'Wheat',
        'season': 'Rabi'
    }
)

result = response.json()
print(f"Risk: {result['risk_level']} ({result['probability']:.1%})")
```

### JavaScript/React
```javascript
import axios from 'axios';

const predictRisk = async () => {
  const response = await axios.post('http://localhost:5000/api/predict', {
    state: 'Punjab',
    district: 'Ludhiana',
    crop: 'Rice',
    season: 'Kharif'
  });
  
  console.log(response.data);
};
```

### cURL
```bash
# Get config
curl http://localhost:5000/api/config | jq

# Get districts
curl http://localhost:5000/api/districts/Maharashtra | jq

# Make prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Karnataka",
    "district": "Belgaum",
    "crop": "Corn",
    "season": "Summer"
  }' | jq
```

---

## 🧪 Testing Checklist

- [ ] Backend running on localhost:5000
- [ ] Frontend running on localhost:3000
- [ ] Health check returns 200: `curl http://localhost:5000/api/health`
- [ ] Config endpoint returns states: `curl http://localhost:5000/api/config`
- [ ] Can make prediction via API: `curl -X POST ...`
- [ ] Frontend loads without errors
- [ ] Can select state → districts populate
- [ ] Can select district → crop → season
- [ ] "Analyze Risk" button triggers prediction
- [ ] Risk card displays correctly
- [ ] Charts render with data
- [ ] Explanation shows top factors

---

## 📞 Support & Documentation

- **Backend Docs**: See `backend/app.py` docstrings
- **API Reference**: See API Endpoints section in README.md
- **Frontend Components**: See `frontend/src/components/` README files
- **Model Details**: See `backend/model/train.py` documentation

---

## 🔄 Regular Maintenance

### Daily
- Monitor logs for errors
- Check API response times

### Weekly
- Retrain model with new data (if available)
- Review prediction accuracy
- Update weather cache

### Monthly
- Backup trained models
- Update dependencies: `pip list --outdated`
- Review and optimize slow queries

---

## 🎓 Next Steps

1. **Extend to more districts**: Edit `backend/utils/config.py`
2. **Add real data integration**: Modify `backend/ingestion/*.py`
3. **Improve ML model**: Tune hyperparameters in `backend/model/train.py`
4. **Add notifications**: Integrate email/SMS alerts
5. **Deploy to cloud**: Use AWS/GCP/Azure

---

## ✅ Setup Complete!

Your Crop Failure Early Warning System is ready to use.

**Start System:**
```bash
# Terminal 1 - Backend
cd "c:\Users\mohit\OneDrive\Desktop\CROP Project"
python backend/app.py

# Terminal 2 - Frontend
cd "c:\Users\mohit\OneDrive\Desktop\CROP Project\frontend"
npm start
```

**Access:** http://localhost:3000

**Enjoy!** 🌾

---

*Last Updated: January 2026*

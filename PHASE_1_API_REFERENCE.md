# PHASE 1: ENSEMBLE API REFERENCE

## Endpoint Details

### Request Format

```bash
POST http://localhost:5000/api/predict-ensemble
Content-Type: application/json

{
  "state": "Maharashtra",
  "district": "Pune",
  "crop": "Rice",
  "season": "Kharif"
}
```

### Response Format (Success - 200)

```json
{
  "state": "Maharashtra",
  "district": "Pune",
  "crop": "Rice",
  "season": "Kharif",
  "risk_level": "Low",
  "ensemble_probability": 0.1056,
  "rf_probability": 0.1326,
  "xgb_probability": 0.0244,
  "confidence": 0.9013,
  "models_used": 2,
  "raw_features": {
    "ndvi_mean": 0.687,
    "ndvi_trend": 0.012,
    "ndvi_variance": 0.031,
    "rainfall_deviation": 5.2,
    "temperature_anomaly": 1.1,
    "soil_moisture_index": 0.68,
    "soil_type_encoded": 3,
    "pest_frequency": 0.15
  },
  "normalized_features": {
    "ndvi_mean": 0.512,
    "ndvi_trend": 0.645,
    "ndvi_variance": -0.123,
    "rainfall_deviation": 0.234,
    "temperature_anomaly": 0.156,
    "soil_moisture_index": 0.423,
    "soil_type_encoded": 0.801,
    "pest_frequency": 0.089
  }
}
```

### Response Format (Error - 400/500)

```json
{
  "error": "Missing required fields"
}
```

---

## Field Descriptions

### Input Fields

| Field | Type | Required | Example | Notes |
|-------|------|----------|---------|-------|
| state | string | Yes | Maharashtra | Must exist in config |
| district | string | Yes | Pune | Must be in state's district list |
| crop | string | Yes | Rice | Must be in CROPS config |
| season | string | Yes | Kharif | Must be Kharif/Rabi/Summer |

### Output Fields

| Field | Type | Range | Meaning |
|-------|------|-------|---------|
| risk_level | string | "Low"/"Medium"/"High" | Final risk classification |
| ensemble_probability | float | 0.0 - 1.0 | Combined RF + XGB score (via meta-learner) |
| rf_probability | float | 0.0 - 1.0 OR null | Random Forest individual score |
| xgb_probability | float | 0.0 - 1.0 OR null | XGBoost individual score |
| confidence | float | 0.5 - 0.95 | Model agreement confidence |
| models_used | int | 1-2 | Number of base models that succeeded |
| raw_features | dict | - | Original scaled features from data sources |
| normalized_features | dict | -1 to +3 | Standardized features (z-score normalized) |

---

## Risk Level Thresholds

```python
if ensemble_probability < 0.33:
    risk_level = "Low"       # ✓ Safe to plant/continue
elif ensemble_probability < 0.67:
    risk_level = "Medium"    # ⚠ Monitor closely, take precautions
else:
    risk_level = "High"      # ✗ High failure risk, recommend alternatives
```

---

## Confidence Scoring

**How is confidence calculated?**

```python
if both_rf_and_xgb_available:
    # Measure agreement between models
    agreement = 1 - abs(rf_prob - xgb_prob)
    confidence = min(0.95, 0.5 + 0.45 * agreement)
elif one_model_available:
    # Single model prediction
    confidence = 0.75
else:
    # No models available (rare)
    confidence = 0.50
```

**Interpretation:**
- **0.90+**: Excellent (both models strongly agree)
- **0.85-0.90**: Good (models generally aligned)
- **0.75-0.85**: Fair (one model or moderate disagreement)
- **0.50-0.75**: Low (limited information)

---

## Error Codes

| Code | Error | Cause | Fix |
|------|-------|-------|-----|
| 400 | Missing required fields | JSON missing state/district/crop/season | Check payload |
| 400 | Invalid state | State not in config | Check STATES list |
| 400 | Invalid crop | Crop not in CROPS list | Check CROPS list |
| 400 | Invalid season | Season not Kharif/Rabi/Summer | Use correct season |
| 500 | Ensemble prediction failed | Unexpected backend error | Check logs |

---

## Testing with cURL

```bash
# Test 1: Low Risk Scenario
curl -X POST http://localhost:5000/api/predict-ensemble \
  -H "Content-Type: application/json" \
  -d '{"state":"Punjab","district":"Amritsar","crop":"Wheat","season":"Rabi"}'

# Test 2: Different Crop/Season
curl -X POST http://localhost:5000/api/predict-ensemble \
  -H "Content-Type: application/json" \
  -d '{"state":"Karnataka","district":"Bengaluru Rural","crop":"Cotton","season":"Kharif"}'
```

---

## Testing with Python

```python
import requests
import json

url = "http://localhost:5000/api/predict-ensemble"
payload = {
    "state": "Maharashtra",
    "district": "Pune",
    "crop": "Rice",
    "season": "Kharif"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Risk: {result['risk_level']}")
print(f"Probability: {result['ensemble_probability']:.3f}")
print(f"Confidence: {result['confidence']:.3f}")
print(f"Models Used: {result['models_used']}/2")
```

---

## Performance Metrics

### Prediction Time
- **Feature Engineering**: ~2 seconds (API calls)
- **Ensemble Inference**: ~0.1 seconds (model predictions)
- **Total**: ~2.1 seconds per request

### Accuracy on Test Set
- **Ensemble**: 83.25% (AUC: 0.7980)
- **RF**: 82.50% (AUC: 0.7988)
- **XGB**: 83.50% (AUC: 0.7911)

### Model File Sizes
```
rf_model.pkl           ~85 MB
xgb_model.pkl          ~45 MB
meta_learner.pkl       <1 MB
scaler.pkl             <1 MB
scaler_meta.pkl        <1 MB
─────────────────────────────
Total                  ~131 MB
```

---

## Troubleshooting

### Issue: "Models not loaded"
**Solution:** Restart backend; ensemble trains automatically on first use

### Issue: "Both rf_probability and xgb_probability are null"
**Solution:** Both base models failed (very rare); system falls back to 0.5

### Issue: "confidence is 0.75"
**Solution:** Only one model succeeded; confidence is reduced but prediction still valid

### Issue: "Prediction takes >5 seconds"
**Solution:** MODIS API or OpenWeather API is slow; no action needed (design limitation)

---

## Integration with Frontend

### Recommended Frontend Updates

```jsx
// Use ensemble endpoint instead of regular predict
const response = await fetch('/api/predict-ensemble', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    state, district, crop, season
  })
});

const result = await response.json();

// Display ensemble result with confidence
<RiskCard 
  riskLevel={result.risk_level}
  probability={result.ensemble_probability}
  confidence={result.confidence}
  modelScores={{
    rf: result.rf_probability,
    xgb: result.xgb_probability
  }}
/>
```

---

**Version:** 1.0 (Phase 1 Complete)  
**Date:** January 17, 2026  
**Status:** ✅ Production Ready

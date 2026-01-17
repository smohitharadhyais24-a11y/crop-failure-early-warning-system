"""
Rule-Based AI Advisory Module - Natural Language Recommendations

Generates farmer-friendly, actionable recommendations based on:
- Risk level
- Feature analysis (SHAP)
- Counterfactual scenarios
- Best practices

NO LLM - fully rule-driven, deterministic, multilingual
"""

from backend.utils.helpers import setup_logger, log_step

logger = setup_logger(__name__)


class AdvisoryEngine:
    """Rule-based advisory system for farmer recommendations."""
    
    def __init__(self):
        """Initialize advice templates and rules."""
        self.language = 'en'  # Default to English
        
        # Risk-based templates
        self.risk_templates = {
            'Low': {
                'en': "Your crop has LOW failure risk. Current conditions are favorable.",
                'hi': "आपकी फसल पर कम जोखिम है। वर्तमान स्थितियां अनुकूल हैं।",
                'mr': "तुमच्या पिकीला कमी जोखीम आहे. वर्तमान परिस्थिती अनुकूल आहेत.",
                'kn': "ನಿಮ್ಮ ಬೆಳೆಗೆ ಕಡಿಮೆ ಅಪಾಯವಿದೆ. ಪ್ರಸ್ತುತ ಪರಿಸ್ಥಿತಿಗಳು ಅನುಕೂಲವಾಗಿವೆ.",
                'ta': "உங்கள் பயிர் குறைந்த ஆபத்தில் உள்ளது. நடப்பு நிலைமைகள் சாதகமாக உள்ளன."
            },
            'Medium': {
                'en': "Your crop has MEDIUM failure risk. Monitor closely and take precautions.",
                'hi': "आपकी फसल पर मध्यम जोखिम है। बारीकी से निगरानी करें और सावधानियां बरतें।",
                'mr': "तुमच्या पिकीला मध्यम जोखीम आहे. बारकाईने निरीक्षण करा आणि सावधानी घ्या.",
                'kn': "ನಿಮ್ಮ ಬೆಳೆಗೆ ಮಧ್ಯಮ ಅಪಾಯವಿದೆ. ನಿಕಟವಾಗಿ ನೋಂದಾಯಿಸಿ ಮತ್ತು ಜಾಗರೂಕತೆ ವಹಿಸಿ.",
                'ta': "உங்கள் பயிர் நடுத்தர ஆபத்தில் உள்ளது. நெருக்கமாக கண்காணிக்கவும் மற்றும் எச்சரிக்கை மெறுவும்."
            },
            'High': {
                'en': "Your crop has HIGH failure risk. Urgent action required!",
                'hi': "आपकी फसल पर उच्च जोखिम है। तत्काल कार्रवाई आवश्यक है!",
                'mr': "तुमच्या पिकीला उच्च जोखीम आहे. तातडीने कार्रवाई आवश्यक आहे!",
                'kn': "ನಿಮ್ಮ ಬೆಳೆಗೆ ಹೆಚ್ಚಿನ ಅಪಾಯವಿದೆ. ತುರ್ತು ಕ್ರಮ ಅವಶ್ಯಕ!",
                'ta': "உங்கள் பயிர் அதிக ஆபத்தில் உள்ளது. உடனடி நடவடிக்கை தேவை!"
            }
        }
        
        # Feature-specific recommendations
        self.feature_recommendations = {
            'ndvi_mean': {
                'en': 'Improve vegetation health through irrigation, fertilization, and pest management.',
                'hi': 'सिंचाई, उर्वरीकरण और कीट प्रबंधन के माध्यम से वनस्पति स्वास्थ्य में सुधार करें।',
                'mr': 'सिंचन, खतिज आणि कीटक व्यवस्थापन माध्यमातून वनस्पती आरोग्य सुधार करा.',
                'kn': 'ನೀರಾವರ, ಸಾರಜನಕ ಸಮೃದ್ಧಿ ಮತ್ತು ಕೀಟ ನಿರ್ವಹಣೆ ಮೂಲಕ ಸಸ್ಯ ಆರೋಗ್ಯ ಸುಧಾರಿಸಿ.',
                'ta': 'நீர்ப்பாசனம், உரം மற்றும் பூச்சி நிர்வாहம் மூலம் தாவರ ஆரோக்கியம் மேம்படுத்தவும்.'
            },
            'rainfall_deviation': {
                'en': 'Manage water stress: use drip irrigation, mulching, and water conservation techniques.',
                'hi': 'जल तनाव का प्रबंधन करें: ड्रिप सिंचाई, मल्चिंग और जल संरक्षण तकनीकों का उपयोग करें।',
                'mr': 'पाणी ताणाची व्यवस्थापना: ड्रिप सिंचन, मल्चिंग आणि जल संरक्षण तंत्र वापरा.',
                'kn': 'ಜಲ ಒತ್ತಡ ನಿರ್ವಹಿಸಿ: ಸೂಕ್ಷ್ಮ ನೀರಾವರ, ಮಲ್ಚಿಂಗ್ ಮತ್ತು ಜಲ ಸಂರಕ್ಷಣ ತಂತ್ರ ಬಳಸಿ.',
                'ta': 'நீர் அழுத்தத்தை நிர்வகிக்கவும்: சொட்டு நீர்ப்பாசனம், முல்ச்ஞ் மற்றும் நீர் சேமிப்பு நுட்ப ஐ பயன்படுத்தவும்.'
            },
            'soil_moisture_index': {
                'en': 'Increase soil moisture: optimize irrigation schedule, add organic matter, use mulch.',
                'hi': 'मिट्टी की नमी बढ़ाएं: सिंचाई कार्यक्रम को अनुकूलित करें, जैविक पदार्थ जोड़ें, मल्च का उपयोग करें।',
                'mr': 'मातीची ओलावा वाढवा: सिंचन वेळापत्रक अनुकूलित करा, जैविक पदार्थ जोडा, मल्च वापरा.',
                'kn': 'ಮಣ್ಣಿನ ಆರ್ದ್ರತೆ ಹೆಚ್ಚಿಸಿ: ನೀರಾವರ ವೇಳಾಪಟ್ಟಿ ಉತ್ತಮ ಮಾಡಿ, ಜೈವಿಕ ವಸ್ತು ಸೇರಿಸಿ, ಮಲ್ಚ್ ಬಳಸಿ.',
                'ta': 'மண் ஈரப்பதம் அதிகரிக்கவும்: பாசனம் அட்டவணை மேம்படுத்தவும், இயற்கை பொருள் சேர்க்கவும், முல்ச் பயன்படுத்தவும்.'
            },
            'pest_frequency': {
                'en': 'Control pests: use integrated pest management (IPM), crop rotation, natural predators.',
                'hi': 'कीटों पर नियंत्रण: एकीकृत कीट प्रबंधन (IPM), फसल चक्र, प्राकृतिक शिकारियों का उपयोग करें।',
                'mr': 'कीटांवर नियंत्रण: संकलित कीटक व्यवस्थापन (IPM), पिक परिवर्तन, नैसर्गिक शिकारी वापरा.',
                'kn': 'ಕೀಟಗಳನ್ನು ನಿಯಂತ್ರಿಸಿ: ಸಂಯೋಜಿತ ಕೀಟ ನಿರ್ವಹಣೆ (IPM), ಫಸಲ್ ತಿರುವು, ನೈಸರ್ಗಿಕ ಶಿಕಾರಿಗಳನ್ನು ಬಳಸಿ.',
                'ta': 'பூச்சிகளைக் கட்டுப்படுத்தவும்: ஒருங்கிணைந்த பூச்சி நிர்வாहம் (IPM), பயிர் சுழற்சி, இயற்கை வேட்டைக்கார ஐ பயன்படுத்தவும்.'
            },
            'temperature_anomaly': {
                'en': 'Mitigate heat stress: select heat-tolerant varieties, adjust sowing dates, use shade netting.',
                'hi': 'गर्मी के तनाव को कम करें: गर्मी-सहिष्णु किस्में चुनें, बुवाई की तारीख समायोजित करें, छाया नेट का उपयोग करें।',
                'mr': 'उष्णता ताण कमी करा: उष्णता-सहन करणारी वर्गणे निवडा, बुवाई तारीख समायोजित करा, सावळी जाळी वापरा.',
                'kn': 'ಶಾಖ ಒತ್ತಡ ತಗ್ಗಿಸಿ: ಶಾಖ-ಸಹಿಷ್ಣು ಭೇದಗಳನ್ನು ಆಯ್ಕೆ ಮಾಡಿ, ಬಿತ್ತನೆ ದಿನಾಂಕ ಸರಿಹೊಂದಿಸಿ, ನೆರಳು ನೆಟ್ಟಿಂಗ ಬಳಸಿ.',
                'ta': 'வெப்ப அழுத்தத்தைக் குறைக்கவும்: வெப்பம்-சகிப்புத்தன்மையுள்ள ཛ种்கள் தேர்ந்தெடுக்கவும், விதை நாட்கள் சரிசெய்யவும், நிழல் வலை பயன்படுத்தவும்.'
            }
        }
    
    def generate_advisory(self, prediction, explanation, counterfactuals, language='en'):
        """
        Generate comprehensive advisory for farmer.
        
        Returns:
            {
                'summary': 'Risk assessment and current situation',
                'immediate_actions': ['Action 1', 'Action 2', ...],
                'preventive_measures': ['Measure 1', 'Measure 2', ...],
                'opportunities': ['If NDVI improves, risk reduces...', ...],
                'contact_info': 'Extension officer details',
                'language': 'en'
            }
        """
        try:
            log_step("Advisory Generation", "in_progress")
            
            self.language = language
            risk_level = prediction['risk_level']
            probability = prediction['ensemble_probability']
            top_features = explanation['feature_importance'][:3]
            
            # Summary based on risk level
            summary = self.risk_templates[risk_level].get(language, self.risk_templates[risk_level]['en'])
            
            # Immediate actions
            immediate_actions = []
            if risk_level == 'High':
                immediate_actions = [
                    self._get_translation(
                        'Consult local agricultural extension officer immediately',
                        {
                            'en': 'Consult local agricultural extension officer immediately',
                            'hi': 'तुरंत स्थानीय कृषि विस्तार अधिकारी से सलाह लें',
                            'mr': 'ताशकरीने स्थानिक कृषी विस्तार अधिकाऱ्यांचा सल्ला घ्या',
                            'kn': 'ತಕ್ಷಣವೇ ಸ್ಥಳೀಯ ಕೃষಿ ವಿಸ್ತರಣ ಅಧಿಕಾರಿಗೆ ಸಂಪರ್ಕಿಸಿ',
                            'ta': 'உடனடியாக ஸ்தानीய கृषि விस्तार அधिकारีyoto ಸಂಪರ್ಕಿಸಿ'
                        }, language
                    ),
                    self._get_translation(
                        'Increase monitoring frequency to every 2-3 days',
                        {
                            'en': 'Increase monitoring frequency to every 2-3 days',
                            'hi': 'निगरानी की आवृत्ति को हर 2-3 दिन में बढ़ाएं',
                            'mr': 'निरीक्षणाची वारंवारता २-३ दिनांत वाढवा',
                            'kn': 'ಪ್ರತಿ ೨-೩ ದಿನಗಳಿಗೊಮ್ಮೆ ನಿಗಾ ಆವೃತ್ತಿ ಹೆಚ್ಚಿಸಿ',
                            'ta': 'கண்காணிப்பு அதிர frequency 2-3 நாட்களிற்கு அதிகரிக்கவும்'
                        }, language
                    )
                ]
            elif risk_level == 'Medium':
                immediate_actions = [
                    self._get_translation(
                        'Monitor crop condition every 3-5 days',
                        {
                            'en': 'Monitor crop condition every 3-5 days',
                            'hi': 'हर 3-5 दिन में फसल की स्थिति की निगरानी करें',
                            'mr': 'प्रत्येक ३-५ दिनांत पिकीची स्थिति निरीक्षण करा',
                            'kn': 'ಪ್ರತಿ ೩-೫ ದಿನಗಳಿಗೊಮ್ಮೆ ಬೆಳೆಯ ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಿ',
                            'ta': 'ஒவ್வொரு 3-5 நாட்களிற்கு பயிர் நிலையை கண்காணிக்கவும்'
                        }, language
                    )
                ]
            else:
                immediate_actions = [
                    self._get_translation(
                        'Continue normal farming practices',
                        {
                            'en': 'Continue normal farming practices',
                            'hi': 'सामान्य कृषि प्रथाओं को जारी रखें',
                            'mr': 'सामान्य शेतकरी पद्धती सुरू ठेवा',
                            'kn': 'ಸಾಮಾನ್ಯ ಕೃಷಿ ಅಭ್ಯಾಸ ಮುಂದುವರಿಸಿ',
                            'ta': 'சாதாரண விவசாய நடைமுறை தொடரவும்'
                        }, language
                    )
                ]
            
            # Preventive measures based on top risk features
            preventive_measures = []
            for feature_info in top_features:
                feature = feature_info['feature'].lower()
                if 'ndvi' in feature:
                    rec = self.feature_recommendations['ndvi_mean'].get(language)
                elif 'rainfall' in feature:
                    rec = self.feature_recommendations['rainfall_deviation'].get(language)
                elif 'moisture' in feature:
                    rec = self.feature_recommendations['soil_moisture_index'].get(language)
                elif 'pest' in feature:
                    rec = self.feature_recommendations['pest_frequency'].get(language)
                elif 'temperature' in feature:
                    rec = self.feature_recommendations['temperature_anomaly'].get(language)
                else:
                    continue
                
                if rec and rec not in preventive_measures:
                    preventive_measures.append(rec)
            
            # Opportunities from counterfactuals
            opportunities = []
            for cf in counterfactuals[:3]:
                opportunity_text = self._get_translation(
                    f"{cf['scenario']}: {cf['actionable']} (Risk: {cf['new_risk_level']})",
                    {
                        'en': f"{cf['scenario']}: {cf['actionable']} (Risk: {cf['new_risk_level']})",
                        'hi': f"{cf['scenario']}: {cf['actionable']} (जोखिम: {cf['new_risk_level']})",
                        'mr': f"{cf['scenario']}: {cf['actionable']} (जोखीम: {cf['new_risk_level']})",
                        'kn': f"{cf['scenario']}: {cf['actionable']} (ಅಪಾಯ: {cf['new_risk_level']})",
                        'ta': f"{cf['scenario']}: {cf['actionable']} (ஆபத்து: {cf['new_risk_level']})"
                    }, language
                )
                opportunities.append(opportunity_text)
            
            # Contact info (template)
            contact_info = self._get_translation(
                'Contact your local agricultural extension office for personalized guidance.',
                {
                    'en': 'Contact your local agricultural extension office for personalized guidance.',
                    'hi': 'व्यक्तिगत मार्गदर्शन के लिए अपने स्थानीय कृषि विस्तार कार्यालय से संपर्क करें।',
                    'mr': 'व्यक्तिगत मार्गदर्शनासाठी आपल्या स्थानिक कृषी विस्तार कार्यालयांचा संपर्क साधा.',
                    'kn': 'ವ್ಯಕ್ತಿಗತ ಮಾರ್ಗದರ್ಶನಕ್ಕಾಗಿ ನಿಮ್ಮ ಸ್ಥಳೀಯ ಕೃಷಿ ವಿಸ್ತರಣ ಕಚೇರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ.',
                    'ta': 'ஆளுக்ற கार्यदर्शनಕ್ಕಾಗಿ ನಿಮ್ಮ ಸ್ಥಳೀಯ कृषि विস्तार कार्यालयाशी संपर्क साधा.'
                }, language
            )
            
            result = {
                'summary': summary,
                'immediate_actions': immediate_actions,
                'preventive_measures': preventive_measures,
                'opportunities': opportunities,
                'contact_info': contact_info,
                'language': language,
                'confidence': prediction.get('confidence', 0.5)
            }
            
            log_step("Advisory Generation", "success")
            
            return result
            
        except Exception as e:
            logger.error(f"Advisory generation failed: {e}")
            raise
    
    def _get_translation(self, english_text, translation_dict, language):
        """Get translated text or fallback to English."""
        return translation_dict.get(language, translation_dict.get('en', english_text))


# Singleton instance
_advisory_engine = None


def get_advisory_engine():
    """Get or create singleton advisory engine."""
    global _advisory_engine
    if _advisory_engine is None:
        _advisory_engine = AdvisoryEngine()
    return _advisory_engine


def generate_advisory(prediction, explanation, counterfactuals, language='en'):
    """Unified advisory generation API."""
    engine = get_advisory_engine()
    return engine.generate_advisory(prediction, explanation, counterfactuals, language)

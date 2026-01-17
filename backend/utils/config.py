import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', 'c7fd644019a4b438e47cbcf6932faaa8')
MODIS_API_KEY = os.getenv('MODIS_API_KEY', 'demo_key')

# Model Configuration
MODEL_PATH = 'backend/model/crop_failure_model.pkl'
FEATURE_IMPORTANCE_PATH = 'backend/model/feature_importance.pkl'

# Database paths
DATA_DIR = 'data/'

# District and crop mappings (Expanded with all major districts)
STATES = {
    'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Kurnool', 'Kadapa', 'Anantapur', 'Chittoor', 'Prakasam', 'East Godavari', 'West Godavari', 'Krishna', 'Srikakulam'],
    'Arunachal Pradesh': ['Itanagar', 'Tawang', 'Pasighat', 'Ziro', 'Bomdila', 'Tezu', 'Changlang', 'Seppa', 'Naharlagun'],
    'Assam': ['Guwahati', 'Jorhat', 'Silchar', 'Dibrugarh', 'Tezpur', 'Nagaon', 'Barpeta', 'Dhubri', 'Tinsukia', 'Goalpara', 'Sivasagar'],
    'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Darbhanga', 'Purnia', 'Arrah', 'Begusarai', 'Katihar', 'Munger', 'Saharsa', 'Chapra'],
    'Chhattisgarh': ['Raipur', 'Bilaspur', 'Durg', 'Korba', 'Rajnandgaon', 'Jagdalpur', 'Raigarh', 'Bhilai', 'Ambikapur', 'Janjgir'],
    'Delhi': ['New Delhi', 'North Delhi', 'South Delhi', 'West Delhi', 'East Delhi', 'Central Delhi', 'North East Delhi', 'North West Delhi', 'South West Delhi'],
    'Goa': ['Panaji', 'Margao', 'Mapusa', 'Vasco da Gama', 'Ponda', 'Bicholim', 'Curchorem', 'Sanquelim'],
    'Gujarat': ['Ahmedabad', 'Surat', 'Rajkot', 'Vadodara', 'Bhavnagar', 'Jamnagar', 'Junagadh', 'Gandhinagar', 'Anand', 'Mehsana', 'Nadiad', 'Bharuch', 'Vapi'],
    'Haryana': ['Gurugram', 'Faridabad', 'Karnal', 'Hisar', 'Panipat', 'Ambala', 'Rohtak', 'Sonipat', 'Yamunanagar', 'Panchkula', 'Bhiwani'],
    'Himachal Pradesh': ['Shimla', 'Mandi', 'Solan', 'Kangra', 'Una', 'Hamirpur', 'Kullu', 'Bilaspur', 'Chamba', 'Dharamshala'],
    'Jammu & Kashmir': ['Srinagar', 'Jammu', 'Anantnag', 'Baramulla', 'Udhampur', 'Kathua', 'Pulwama', 'Kupwara', 'Rajouri', 'Poonch'],
    'Jharkhand': ['Ranchi', 'Dhanbad', 'Jamshedpur', 'Hazaribagh', 'Bokaro', 'Deoghar', 'Giridih', 'Dumka', 'Chaibasa', 'Ramgarh'],
    'Karnataka': ['Bengaluru Urban', 'Bengaluru Rural', 'Mysuru', 'Belagavi', 'Mangaluru', 'Hubballi', 'Dharwad', 'Kalaburagi', 'Vijayapura', 'Raichur', 'Ballari', 'Shivamogga', 'Davangere', 'Tumakuru', 'Chitradurga', 'Hassan', 'Mandya', 'Udupi', 'Chikkamagaluru', 'Kodagu', 'Bidar', 'Gadag', 'Bagalkot', 'Haveri', 'Koppal', 'Chamarajanagar', 'Chikkaballapura', 'Ramanagara', 'Yadgir'],
    'Kerala': ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Palakkad', 'Thrissur', 'Kollam', 'Kannur', 'Alappuzha', 'Malappuram', 'Kottayam', 'Pathanamthitta', 'Idukki', 'Wayanad', 'Kasaragod'],
    'Madhya Pradesh': ['Bhopal', 'Indore', 'Gwalior', 'Jabalpur', 'Ujjain', 'Sagar', 'Dewas', 'Satna', 'Ratlam', 'Rewa', 'Katni', 'Singrauli', 'Burhanpur'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nashik', 'Solapur', 'Nagpur', 'Thane', 'Aurangabad', 'Kolhapur', 'Ahmednagar', 'Amravati', 'Sangli', 'Jalgaon', 'Akola', 'Latur', 'Satara', 'Nanded', 'Parbhani', 'Ratnagiri', 'Chandrapur', 'Beed'],
    'Manipur': ['Imphal', 'Thoubal', 'Churachandpur', 'Ukhrul', 'Bishnupur', 'Senapati', 'Tamenglong', 'Chandel'],
    'Meghalaya': ['Shillong', 'Jowai', 'Tura', 'Nongpoh', 'Williamnagar', 'Baghmara', 'Nongstoin'],
    'Mizoram': ['Aizawl', 'Lunglei', 'Champhai', 'Serchhip', 'Kolasib', 'Saiha', 'Lawngtlai', 'Mamit'],
    'Nagaland': ['Kohima', 'Dimapur', 'Mokokchung', 'Tuensang', 'Wokha', 'Zunheboto', 'Phek', 'Mon'],
    'Odisha': ['Bhubaneswar', 'Cuttack', 'Sambalpur', 'Berhampur', 'Rourkela', 'Puri', 'Balasore', 'Bhadrak', 'Baripada', 'Jeypore', 'Angul', 'Jharsuguda'],
    'Punjab': ['Amritsar', 'Ludhiana', 'Sangrur', 'Moga', 'Jalandhar', 'Patiala', 'Bathinda', 'Hoshiarpur', 'Mohali', 'Pathankot', 'Firozpur', 'Mansa', 'Fazilka'],
    'Rajasthan': ['Jaipur', 'Jodhpur', 'Bikaner', 'Barmer', 'Udaipur', 'Kota', 'Ajmer', 'Alwar', 'Bhilwara', 'Sikar', 'Pali', 'Jaisalmer', 'Chittorgarh', 'Jhunjhunu'],
    'Sikkim': ['Gangtok', 'Gyalshing', 'Mangan', 'Namchi', 'Rangpo', 'Jorethang'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Thanjavur', 'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Tiruppur', 'Vellore', 'Erode', 'Kancheepuram', 'Dindigul', 'Cuddalore', 'Nagapattinam', 'Karur'],
    'Telangana': ['Hyderabad', 'Warangal', 'Karimnagar', 'Nizamabad', 'Khammam', 'Nalgonda', 'Mahbubnagar', 'Adilabad', 'Rangareddy', 'Medak', 'Sangareddy'],
    'Tripura': ['Agartala', 'Udaipur', 'Khowai', 'Dharmanagar', 'Kailashahar', 'Belonia', 'Ambassa', 'Teliamura'],
    'Uttar Pradesh': ['Agra', 'Meerut', 'Kanpur', 'Lucknow', 'Varanasi', 'Allahabad', 'Bareilly', 'Aligarh', 'Moradabad', 'Ghaziabad', 'Saharanpur', 'Gorakhpur', 'Noida', 'Firozabad', 'Mathura', 'Jhansi', 'Muzaffarnagar'],
    'Uttarakhand': ['Dehradun', 'Haridwar', 'Nainital', 'Rudrapur', 'Haldwani', 'Roorkee', 'Kashipur', 'Rishikesh', 'Pithoragarh', 'Almora'],
    'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Malda', 'Siliguri', 'Asansol', 'Bardhaman', 'Jalpaiguri', 'Darjeeling', 'Murshidabad', 'Nadia', 'Cooch Behar', 'Midnapore']
}

CROPS = ['Rice', 'Wheat', 'Corn', 'Cotton', 'Sugarcane', 'Soybean', 'Pulses', 'Millet', 'Barley', 'Groundnut', 'Mustard', 'Jowar', 'Bajra']

SEASONS = ['Kharif', 'Rabi', 'Zaid']

# Thresholds
NDVI_STRESS_THRESHOLD = 0.3
RAINFALL_DEVIATION_THRESHOLD = 20  # percentage
SOIL_MOISTURE_CRITICAL = 30  # percentage
PEST_CRITICAL_COUNT = 5

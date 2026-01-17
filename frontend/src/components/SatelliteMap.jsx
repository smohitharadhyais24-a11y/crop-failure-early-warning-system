import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Rectangle, CircleMarker, useMap, Popup } from 'react-leaflet';
import { Satellite, X, Maximize2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import 'leaflet/dist/leaflet.css';

const SatelliteMap = ({ district, state, ndviValue }) => {
  const { t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [mapCenter, setMapCenter] = useState([12.9716, 77.5946]); // Default: Bangalore
  
  // Comprehensive district coordinates mapping - 100+ Indian districts
  const districtCoordinates = {
    // Karnataka
    'Bengaluru Urban': [12.9716, 77.5946],
    'Bengaluru Rural': [13.2172, 77.3800],
    'Mysuru': [12.2958, 76.6394],
    'Mandya': [12.5311, 76.1648],
    'Tumkur': [13.2184, 75.2263],
    'Kolar': [13.1439, 78.1304],
    'Chikballapur': [13.4330, 77.8141],
    'Ramanagara': [12.7667, 77.2833],
    'Davanagere': [14.4644, 75.9185],
    'Belgaum': [15.8497, 75.6193],
    'Vijayapura': [16.8149, 75.7118],
    'Gadag': [15.4167, 75.3333],
    'Bagalkot': [16.1667, 75.8333],
    'Uttara Kannada': [14.5, 74.9],
    'Udupi': [13.3344, 74.7421],
    'Dakshina Kannada': [12.8764, 75.3736],
    'Kodagu': [12.3381, 75.7522],
    'Chitradurga': [14.2267, 75.7421],
    'Hassan': [13.9976, 75.9597],
    'Shimoga': [13.9299, 75.5681],
    'Shivamogga': [13.9299, 75.5681],
    
    // Arunachal Pradesh
    'Pasighat': [28.0667, 93.8167],
    'Itanagar': [28.1700, 93.6170],
    'Tawang': [27.5868, 91.3662],
    'Papum Pare': [28.1000, 93.6500],
    'East Kameng': [27.7000, 92.4000],
    'Lohit': [28.8167, 94.2333],
    'Changlang': [28.5, 94.5],
    'Dibang Valley': [28.7, 94.4],
    'Upper Dibang Valley': [29.0, 94.6],
    'Kra Daadi': [29.1, 94.0],
    'Namsai': [28.3667, 94.1667],
    'Siang': [29.0, 93.5],
    'Lepa Rada': [28.8, 93.2],
    'Kurung Kumey': [29.3, 92.8],
    'Upper Siang': [29.9, 93.5],
    
    // Maharashtra
    'Pune': [18.5204, 73.8567],
    'Mumbai': [19.0760, 72.8777],
    'Nagpur': [21.1458, 79.0882],
    'Aurangabad': [19.8762, 75.3433],
    'Nashik': [19.9975, 73.7898],
    'Thane': [19.2183, 73.0027],
    'Raigad': [18.6298, 73.4567],
    'Ratnagiri': [17.1667, 73.3167],
    'Satara': [17.6829, 73.9243],
    'Sangli': [16.8553, 74.5677],
    'Solapur': [17.6599, 75.9064],
    'Kolhapur': [16.7050, 73.7421],
    'Ahmednagar': [19.0975, 74.7421],
    'Jalna': [19.8427, 75.8847],
    'Buldhana': [20.5333, 76.1667],
    'Akola': [20.7280, 77.0056],
    'Amravati': [20.9314, 77.7763],
    'Wardha': [20.7523, 78.6050],
    'Chandrapur': [19.2822, 79.3050],
    'Gondia': [21.4604, 80.2046],
    'Bhandara': [21.1833, 79.3167],
    'Washim': [20.1061, 77.5306],
    'Yavatmal': [20.4042, 78.1334],
    
    // Delhi
    'Delhi': [28.7041, 77.1025],
    'Central Delhi': [28.6326, 77.2197],
    'North Delhi': [28.8000, 77.2000],
    'East Delhi': [28.6000, 77.3500],
    'West Delhi': [28.6500, 76.9500],
    'South Delhi': [28.5500, 77.1500],
    
    // Uttar Pradesh
    'Meerut': [28.9845, 77.7064],
    'Agra': [27.1767, 78.0081],
    'Mathura': [27.4924, 77.6737],
    'Aligarh': [27.8974, 77.8864],
    'Bulandshahr': [28.4089, 77.8338],
    'Kanpur': [26.4499, 80.3319],
    'Lucknow': [26.8467, 80.9462],
    'Varanasi': [25.3200, 82.9789],
    'Allahabad': [25.4358, 81.8463],
    'Jaunpur': [25.7436, 82.6889],
    'Azamgarh': [26.0746, 83.1853],
    'Ghazipur': [25.5308, 84.4290],
    'Saharanpur': [29.9683, 77.5517],
    'Muzaffarnagar': [29.4680, 77.7068],
    'Bijnor': [29.3862, 78.1330],
    'Bareilly': [28.3670, 79.4304],
    'Pilbhit': [29.0841, 79.8075],
    'Shahjahanpur': [27.8774, 79.6420],
    'Kheri': [27.7264, 80.6475],
    'Sitapur': [27.5654, 80.4856],
    'Raebareli': [26.2185, 81.2355],
    'Sultanpur': [26.2602, 81.9098],
    'Pratapgarh': [25.8930, 81.9938],
    
    // Himachal Pradesh
    'Shimla': [31.7724, 77.1064],
    'Mandi': [31.5885, 76.9270],
    'Kangra': [32.2206, 76.2606],
    'Chamba': [32.2254, 76.0146],
    'Himachal Pradesh': [31.7894, 77.1243],
    'Solan': [30.9064, 77.1607],
    'Bilaspur_HP': [31.2818, 76.7675],
    'Una': [31.4822, 75.9650],
    'Hamirpur': [31.6865, 76.5225],
    'Kinnaur': [31.5094, 78.4409],
    'Lahaul Spiti': [32.7000, 77.5000],
    
    // Punjab
    'Amritsar': [31.6340, 74.8723],
    'Ludhiana': [30.9010, 75.8573],
    'Jalandhar': [31.7264, 75.5761],
    'Patiala': [30.3398, 76.3869],
    'Mohali': [30.6394, 76.8217],
    'Hoshiarpur': [31.5349, 75.9125],
    'Moga': [30.8134, 75.2158],
    'Bathinda': [30.2156, 74.9498],
    'Ferozepur': [30.9462, 74.5964],
    'Sangrur': [30.2659, 75.5360],
    'Barnala': [30.9983, 75.6028],
    'Kapurthala': [31.3958, 75.3844],
    'Gurdaspur': [32.1708, 75.4937],
    'Pathankot': [32.2702, 75.6440],
    'Nainital': [29.3820, 79.4556],
    
    // Haryana
    'Faridabad': [28.4089, 77.3178],
    'Gurgaon': [28.4595, 77.0266],
    'Hisar': [29.1539, 75.7388],
    'Rohtak': [28.8996, 76.5641],
    'Karnal': [29.6200, 76.9938],
    'Ambala': [30.3745, 76.7753],
    'Yamunanagar': [30.1214, 77.2667],
    'Panipat': [29.3910, 77.0940],
    'Sonipat': [28.9926, 77.6116],
    'Kaithal': [29.1850, 76.3980],
    'Jind': [29.3044, 75.8369],
    'Bhiwani': [28.8102, 75.6500],
    'Sirsa': [29.5389, 75.0308],
    'Panchkula': [30.3933, 76.8541],
    
    // Rajasthan
    'Jaipur': [26.9124, 75.7873],
    'Jodhpur': [26.2389, 73.0243],
    'Udaipur': [24.5854, 73.7125],
    'Ajmer': [26.4499, 74.6399],
    'Pushkar': [26.4898, 74.5571],
    'Bikaner': [28.0229, 71.8325],
    'Churu': [27.8437, 74.6500],
    'Sikar': [27.6119, 75.1306],
    'Jhunjhunu': [27.9258, 75.3637],
    'Alwar': [27.5735, 76.6250],
    'Bhilwara': [25.3397, 74.6050],
    'Chittorgarh': [24.8935, 74.6299],
    'Kota': [25.2138, 75.8648],
    'Bundi': [25.3938, 75.6244],
    'Barmer': [25.7497, 71.3986],
    'Jaisalmer': [26.9124, 70.9055],
    'Nagaur': [27.1805, 74.7197],
    'Pali': [25.7797, 73.3237],
    'Rajsamand': [25.3897, 73.8729],
    
    // Goa
    'North Goa': [15.5942, 73.8279],
    'South Goa': [14.9955, 73.8107],
    
    // Gujarat
    'Ahmedabad': [23.0225, 72.5714],
    'Vadodara': [22.3072, 73.1812],
    'Surat': [21.1702, 72.8311],
    'Rajkot': [22.3039, 70.7839],
    'Kutch': [23.8103, 69.8780],
    'Junagadh': [21.5250, 70.4539],
    'Bhavnagar': [21.7645, 71.9413],
    'Anand': [22.5697, 72.9289],
    'Kheda': [22.9732, 72.9487],
    'Panchmahal': [22.5958, 73.8990],
    'Dahod': [22.7725, 74.2497],
    'Narmada': [21.8667, 73.7667],
    'Tapi': [21.1961, 73.1975],
    'Valsad': [20.6318, 72.9289],
    'Navsari': [20.9367, 72.9139],
    
    // Tamil Nadu
    'Chennai': [13.0827, 80.2707],
    'Coimbatore': [11.0026, 76.9655],
    'Madurai': [9.9252, 78.1198],
    'Salem': [11.6643, 78.1460],
    'Tiruppur': [11.1085, 77.3411],
    'Erode': [11.3919, 77.7172],
    'Tiruchirappalli': [10.7905, 78.7047],
    'Thanjavur': [10.7870, 79.1378],
    'Tirunelveli': [8.7642, 77.7567],
    'Kanyakumari': [8.0883, 77.5385],
    'Villupuram': [12.9689, 79.8962],
    'Vellore': [12.9689, 79.1288],
    'Ranipet': [12.9408, 79.3544],
    'Tirupathur': [12.2208, 79.3622],
    'Kanchipuram': [12.8342, 79.7029],
    
    // Telangana & Andhra Pradesh
    'Hyderabad': [17.3850, 78.4867],
    'Warangal': [17.9689, 78.6294],
    'Vijayawada': [16.5062, 80.6480],
    'Machilipatnam': [15.7942, 80.1426],
    'Tenali': [15.3061, 80.1015],
    'Eluru': [16.7140, 81.1079],
    'Ongole': [14.6349, 79.6294],
    
    // Kerala
    'Kochi': [9.9312, 76.2673],
    'Thiruvananthapuram': [8.5241, 76.9366],
    'Kozhikode': [11.2588, 75.7804],
    'Kottayam': [9.6410, 76.7638],
    'Pathanamthitta': [9.2713, 76.7497],
    'Idukki': [10.3089, 76.9972],
    'Ernakulam': [10.0333, 76.3833],
    'Thrissur': [10.5276, 76.2144],
    'Malappuram': [11.0076, 76.0764],
    'Kannur': [11.8745, 75.3704],
    'Kasaragod': [12.5036, 75.3404],
    'Kollam': [8.8932, 76.5997],
    'Alappuzha': [9.4981, 76.3388],
    'Wayanad': [11.5957, 75.8994],
    
    // Odisha
    'Bhubaneswar': [20.2961, 85.8245],
    'Cuttack': [20.4625, 85.8830],
    'Rourkela': [22.2265, 84.8585],
    'Sambalpur': [21.4670, 83.9833],
    'Balasore': [21.4975, 87.0671],
    'Keonjhar': [21.6393, 85.2152],
    'Jajpur': [20.8440, 85.8540],
    'Dhenkanal': [20.6931, 85.5917],
    'Sundargarh': [21.9412, 84.0239],
    'Bargarh': [21.7969, 83.6667],
    'Bolangir': [20.4989, 83.4581],
    'Kalahandi': [19.8330, 83.3167],
    'Koraput': [18.8203, 82.6975],
    'Malkangiri': [18.3333, 82.2167],
    'Bhadrak': [20.9706, 86.5023],
    'Mayurbhanj': [22.4122, 85.6631],
    
    // Jharkhand
    'Ranchi': [23.3441, 85.3096],
    'Dhanbad': [23.7957, 86.4304],
    'Jamshedpur': [22.8046, 86.1829],
    'Hazaribagh': [23.9956, 85.3614],
    'Deoghar': [24.4831, 86.6639],
    'Giridih': [24.1766, 85.1956],
    'Bokaro': [23.6718, 85.3720],
    'Purnia': [25.6661, 87.4750],
    'Katihar': [25.5305, 87.5326],
    
    // Bihar
    'Patna': [25.5941, 85.1376],
    'Gaya': [24.7941, 84.9534],
    'Bhagalpur': [25.2677, 86.4904],
    'Darbhanga': [26.1551, 85.8791],
    'Madhubani': [26.3793, 86.5233],
    'Muzaffarpur': [26.1209, 85.3927],
    'Sitamarhi': [26.6162, 85.4833],
    'East Champaran': [26.8046, 84.9004],
    'West Champaran': [26.8046, 84.3500],
    'Araria': [26.2333, 87.4833],
    'Kishanganj': [25.9000, 87.9667],
    'Supaul': [26.1333, 86.5333],
    'Saharsa': [25.8833, 86.3167],
    'Khagaria': [25.4833, 86.4500],
    'Lakhisarai': [25.1333, 86.1333],
    'Jamui': [24.4833, 86.2000],
    'Munger': [25.3833, 86.4667],
    'Sheikhpura': [25.1500, 85.7833],
    'Nalanda': [25.1333, 85.6167],
    'Biharsharif': [25.1833, 85.5333],
    'Jehanabad': [25.2167, 84.9833],
    'Arrah': [25.5667, 84.6667],
    'Sasaram': [24.9500, 84.0333],
    'Rohtas': [24.8833, 83.9667],
    'Kaimur': [25.0333, 84.3000],
    'Buxar': [25.5667, 83.9667],
    'Gopalganj': [26.4667, 84.4333],
    'Saran': [26.1333, 85.2333],
    'Vaishali': [25.9333, 85.5000],
    'Siwan': [26.1833, 84.8667],
    
    // Assam
    'Guwahati': [26.1445, 91.7362],
    'Assam': [26.1445, 91.7362],
    'Nagaon': [26.3167, 92.0667],
    'Sonitpur': [26.5, 92.8167],
    'Lakhimpur': [27.2500, 94.2167],
    'Dhemaji': [27.5000, 94.3333],
    'Tinsukia': [27.4833, 95.3667],
    'Dibrugarh': [27.4833, 94.9167],
    'Sivasagar': [26.9667, 94.6333],
    'Charaideo': [26.8500, 94.3333],
    'Golaghat': [26.5333, 93.9667],
    'Jorhat': [26.7500, 94.2000],
    'Majuli': [27.0000, 93.5000],
    
    // West Bengal
    'Kolkata': [22.5726, 88.3639],
    'Darjeeling': [27.0410, 88.2663],
    'Siliguri': [26.7271, 88.3953],
    'Jalpaiguri': [26.5159, 88.7267],
    'Malda': [25.9788, 88.5355],
    'Murshidabad': [24.1800, 88.2900],
    'Nadia': [24.0596, 88.6854],
    'Hooghly': [22.8979, 88.3888],
    'Howrah': [22.5958, 88.2636],
    'Medinipur': [22.4425, 87.3073],
    'Bankura': [23.2500, 87.0667],
    'Birbhum': [24.0953, 87.8677],
    'Purulia': [23.4833, 86.3667],
    'Barddhaman': [23.2270, 87.8622],
    'Burdwan': [23.2270, 87.8622],
    
    // Meghalaya
    'Shillong': [25.5788, 91.8933],
    'Tura': [25.5167, 90.2500],
    'Jowai': [25.4667, 92.3833],
    
    // Manipur
    'Imphal': [24.8170, 94.7885],
    'Ukhrul': [24.7333, 94.8167],
    
    // Mizoram
    'Aizawl': [23.1815, 92.7879],
    'Lunglei': [22.8833, 92.7667],
    
    // Nagaland
    'Kohima': [25.6816, 94.1084],
    'Dimapur': [25.9067, 93.7211],
    
    // Sikkim
    'Gangtok': [27.5330, 88.6170],
    'Tadong': [27.5330, 88.6170],
    
    // Tripura
    'Agartala': [23.8103, 91.2868],
    
    // Chhattisgarh
    'Raipur': [21.2514, 81.6296],
    'Bilaspur': [22.0796, 82.1581],
    'Durg': [21.1935, 81.2845],
    'Rajnandgaon': [21.9333, 81.0333],
    'Balaghat': [21.8833, 80.1667],
    
    // Madhya Pradesh
    'Indore': [22.7196, 75.8577],
    'Bhopal': [23.1815, 77.4104],
    'Gwalior': [26.2183, 78.1629],
    'Jabalpurur': [23.1815, 79.9864],
    'Ujjain': [23.1797, 75.7708],
    'Ratlam': [23.3330, 75.0480],
    'Mandsaur': [24.6555, 75.0822],
    'Neemuch': [24.4426, 75.3426],
    'Dhar': [22.5659, 75.2939],
    'Khargone': [21.8128, 75.6289],
    'Khandwa': [21.8279, 76.3506],
    'Burhanpur': [21.3066, 76.2261],
    'Betul': [21.8166, 77.9166],
    'Chhindwara': [22.0595, 78.9375],
    'Seoni': [22.1666, 79.1333],
    'Mandla': [22.5863, 80.6455],
    'Dindori': [22.8833, 81.0333],
    'Umaria': [23.5333, 80.8333],
    'Anuppur': [23.0833, 81.4167],
    'Shahdol': [23.4833, 81.3333],
    'Sidhi': [24.1833, 81.8833],
    'Singrauli': [24.1833, 82.6667],
    'Jhabua': [22.8333, 74.8333],
    'Alirajpur': [22.0833, 74.5000],
    'Morena': [26.5028, 78.0081],
    'Chambal': [25.6666, 78.8333],
    'Sheopur': [26.6333, 77.8167],
    'Guna': [25.0166, 77.3166],
    'Ashoknagar': [24.5166, 77.6666],
    'Shivpuri': [25.4333, 77.7333],
    'Datia': [25.6833, 78.5833],
    'Tikamgarh': [25.0166, 78.8666],
    'Chhatarpur': [24.9166, 79.2500],
    'Panna': [24.7333, 80.0833],
    'Damoh': [23.8333, 79.6333],
    'Sagar': [23.8366, 79.5847],
    'Raisen': [23.1666, 77.8333],
    'Vidisha': [23.5166, 77.8166],
    'Sehore': [23.1666, 77.1333],
    'Rajgarh': [23.8333, 75.6333],
    'Dewas': [22.9833, 75.8666],
    'Shajapur': [22.6333, 75.5000],
    'Agar Malwa': [22.7166, 75.0500],
    'Mhow': [22.5500, 75.5666],
    'Khandesh': [21.2160, 75.4180],
    'West Nimar': [22.1210, 75.2638],
    
    // default
    'default': [28.7, 77.1]
  };

  useEffect(() => {
    // Handle districts that share names across states
    if (district === 'Bilaspur' && state === 'Himachal Pradesh' && districtCoordinates['Bilaspur_HP']) {
      setMapCenter(districtCoordinates['Bilaspur_HP']);
    } else if (district === 'Bilaspur' && state === 'Chhattisgarh' && districtCoordinates['Bilaspur']) {
      setMapCenter(districtCoordinates['Bilaspur']);
    } else if (district && districtCoordinates[district]) {
      setMapCenter(districtCoordinates[district]);
    } else if (state && districtCoordinates[state]) {
      setMapCenter(districtCoordinates[state]);
    } else {
      // Fallback to neutral center when no match is found
      setMapCenter(districtCoordinates['default']);
    }
  }, [district, state]);

  const getNDVIColor = (ndvi) => {
    if (ndvi > 0.6) return { color: '#00ff00', fillColor: '#00ff00', opacity: 0.5 }; // Green - healthy
    if (ndvi > 0.4) return { color: '#ffff00', fillColor: '#ffff00', opacity: 0.5 }; // Yellow - moderate
    if (ndvi > 0.2) return { color: '#ff9900', fillColor: '#ff9900', opacity: 0.5 }; // Orange - stressed
    return { color: '#ff0000', fillColor: '#ff0000', opacity: 0.5 }; // Red - critical
  };

  const MapOverlay = () => {
    const map = useMap();
    
    useEffect(() => {
      map.setView(mapCenter, 11);
    }, [map, mapCenter]);
    
    const ndviColor = getNDVIColor(ndviValue || 0.5);
    
    // Create rectangle bounds around district (approximately 20km radius)
    const bounds = [
      [mapCenter[0] - 0.15, mapCenter[1] - 0.15],
      [mapCenter[0] + 0.15, mapCenter[1] + 0.15]
    ];
    
    return (
      <>
        <Rectangle
          bounds={bounds}
          pathOptions={{
            color: ndviColor.color,
            weight: 3,
            fillColor: ndviColor.fillColor,
            fillOpacity: ndviColor.opacity
          }}
        >
          <Popup>
            <div className="text-sm">
              <p className="font-bold">{district}</p>
              <p>NDVI: {(ndviValue || 0.5).toFixed(3)}</p>
            </div>
          </Popup>
        </Rectangle>
        
        {/* Add center marker */}
        <CircleMarker
          center={mapCenter}
          radius={8}
          pathOptions={{
            color: ndviColor.color,
            weight: 2,
            fillColor: ndviColor.fillColor,
            fillOpacity: 0.8
          }}
        >
          <Popup>
            <div className="text-sm font-bold">{district}</div>
          </Popup>
        </CircleMarker>
      </>
    );
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all shadow-md"
      >
        <Satellite size={20} />
        {t('satellite.viewMap')}
      </button>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-6xl h-[80vh] flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-t-lg flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Satellite className="w-6 h-6" />
            <div>
              <h2 className="text-xl font-bold">{t('satellite.ndviMap')}</h2>
              <p className="text-sm text-blue-100">
                {district}, {state}
              </p>
            </div>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="p-2 hover:bg-white hover:bg-opacity-20 rounded-full transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* NDVI Legend */}
        <div className="p-4 bg-gray-50 border-b border-gray-200">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <p className="text-sm font-semibold text-gray-700">
                {t('satellite.vegetation')}
              </p>
              <p className="text-xs text-gray-500">
                NDVI: {(ndviValue || 0.5).toFixed(3)}
              </p>
            </div>
            
            <div className="flex items-center gap-3 flex-wrap">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-red-500 rounded border border-red-700"></div>
                <span className="text-xs text-gray-600">{t('satellite.critical')}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-orange-500 rounded border border-orange-700"></div>
                <span className="text-xs text-gray-600">{t('satellite.stressed')}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-yellow-500 rounded border border-yellow-700"></div>
                <span className="text-xs text-gray-600">{t('satellite.moderate')}</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-green-500 rounded border border-green-700"></div>
                <span className="text-xs text-gray-600">{t('satellite.healthy')}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Map */}
        <div className="flex-1 relative bg-gray-100">
          <MapContainer
            center={mapCenter}
            zoom={11}
            style={{ height: '100%', width: '100%' }}
            className="z-0"
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <MapOverlay />
          </MapContainer>
          
          {/* Info overlay */}
          <div className="absolute bottom-4 left-4 bg-white rounded-lg shadow-lg p-4 z-10">
            <p className="text-sm font-semibold text-gray-700">
              📍 {t('satellite.lastUpdated')}
            </p>
            <p className="text-xs text-gray-500">
              {new Date().toLocaleDateString()}
            </p>
            <p className="text-xs text-gray-400 mt-2 max-w-xs">
              {t('satellite.overlayNote')}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SatelliteMap;

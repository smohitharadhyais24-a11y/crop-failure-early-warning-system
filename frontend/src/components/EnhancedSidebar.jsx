import React, { useState, useEffect } from 'react';
import { ChevronDown, Play, MapPin, Sprout } from 'lucide-react';
import axios from 'axios';

function EnhancedSidebar({ onAnalyze, loading }) {
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [crops, setCrops] = useState([]);
  const [seasons, setSeasons] = useState([]);

  const [selected, setSelected] = useState({
    state: '',
    district: '',
    crop: '',
    season: '',
    soilType: 'loamy',
    landType: 'irrigated',
    sowingMonth: 6,
    farmSize: 2
  });

  const API_BASE = '/api';

  // Fallback data (matches backend expanded districts)
  const FALLBACK_STATES = [
    'Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh',
    'Jammu & Kashmir','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland',
    'Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal'
  ];

  const FALLBACK_DISTRICTS = {
    'Maharashtra': ['Mumbai','Pune','Nashik','Solapur','Nagpur','Thane','Aurangabad','Kolhapur','Ahmednagar','Amravati'],
    'Gujarat': ['Ahmedabad','Surat','Rajkot','Vadodara','Bhavnagar','Jamnagar','Junagadh','Gandhinagar','Anand','Mehsana'],
    'Karnataka': ['Bengaluru Urban','Bengaluru Rural','Mysuru','Belagavi','Mangaluru','Hubballi','Dharwad','Kalaburagi','Vijayapura','Raichur','Ballari','Shivamogga','Davangere','Tumakuru','Chitradurga','Hassan','Mandya','Udupi','Chikkamagaluru','Kodagu'],
    'Tamil Nadu': ['Chennai','Coimbatore','Madurai','Thanjavur','Tiruchirappalli','Salem','Tirunelveli','Tiruppur','Vellore','Erode'],
    'Telangana': ['Hyderabad','Warangal','Karimnagar','Nizamabad','Khammam','Nalgonda','Mahbubnagar','Adilabad','Rangareddy','Medak'],
    'Uttar Pradesh': ['Agra','Meerut','Kanpur','Lucknow','Varanasi','Allahabad','Bareilly','Aligarh','Moradabad','Ghaziabad'],
    'Rajasthan': ['Jaipur','Jodhpur','Bikaner','Barmer','Udaipur','Kota','Ajmer','Alwar','Bhilwara','Sikar'],
    'Punjab': ['Amritsar','Ludhiana','Sangrur','Moga','Jalandhar','Patiala','Bathinda','Hoshiarpur','Mohali','Pathankot'],
    'West Bengal': ['Kolkata','Howrah','Durgapur','Malda','Siliguri','Asansol','Bardhaman','Jalpaiguri','Darjeeling','Murshidabad'],
    'Kerala': ['Thiruvananthapuram','Kochi','Kozhikode','Palakkad','Thrissur','Kollam','Kannur','Alappuzha','Malappuram','Kottayam'],
  };

  const SOIL_TYPES = ['Sandy', 'Loamy', 'Clay', 'Red Soil', 'Black Soil', 'Alluvial'];
  const LAND_TYPES = ['Irrigated', 'Rainfed', 'Mixed'];
  const MONTHS = [
    { val: 1, name: 'Jan' }, { val: 2, name: 'Feb' }, { val: 3, name: 'Mar' },
    { val: 4, name: 'Apr' }, { val: 5, name: 'May' }, { val: 6, name: 'Jun' },
    { val: 7, name: 'Jul' }, { val: 8, name: 'Aug' }, { val: 9, name: 'Sep' },
    { val: 10, name: 'Oct' }, { val: 11, name: 'Nov' }, { val: 12, name: 'Dec' }
  ];
  const FARM_SIZES = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5];

  useEffect(() => {
    const fetchConfig = async () => {
      try {
        const response = await axios.get(`${API_BASE}/config`);
        setStates(response.data.states);
        setCrops(response.data.crops);
        setSeasons(response.data.seasons);
      } catch (error) {
        console.error('Failed to fetch config:', error);
        setStates(FALLBACK_STATES);
        setCrops(['Rice','Wheat','Corn','Cotton','Sugarcane','Soybean','Pulses','Millet','Barley','Groundnut','Mustard','Jowar','Bajra']);
        setSeasons(['Kharif','Rabi','Zaid']);
      }
    };
    fetchConfig();
  }, []);

  useEffect(() => {
    if (selected.state) {
      const fetchDistricts = async () => {
        try {
          const response = await axios.get(`${API_BASE}/districts/${selected.state}`);
          setDistricts(response.data.districts);
        } catch (error) {
          console.error('Failed to fetch districts:', error);
          setDistricts(FALLBACK_DISTRICTS[selected.state] || []);
        }
      };
      fetchDistricts();
    }
  }, [selected.state]);

  const handleSelectChange = (field, value) => {
    setSelected(prev => ({
      ...prev,
      [field]: value,
      ...(field === 'state' && { district: '' })
    }));
  };

  const handleAnalyze = () => {
    if (selected.state && selected.district && selected.crop && selected.season) {
      onAnalyze(selected);
    }
  };

  const isComplete = selected.state && selected.district && selected.crop && selected.season;

  return (
    <div className="w-96 bg-gradient-to-b from-white to-green-50 border-r border-gray-200 shadow-xl p-6 flex flex-col h-screen sticky top-0 overflow-y-auto">
      <div className="flex-1">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <Sprout className="text-green-600" size={28} />
          Analysis Panel
        </h2>

        {/* Essential Inputs */}
        <div className="mb-8 p-4 bg-green-50 rounded-lg border border-green-200">
          <h3 className="font-semibold text-gray-800 mb-4 text-sm">ESSENTIAL INPUTS</h3>
          
          {/* State */}
          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📍 State
            </label>
            <select
              value={selected.state}
              onChange={(e) => handleSelectChange('state', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
            >
              <option value="">-- Select State --</option>
              {states.map(state => (
                <option key={state} value={state}>{state}</option>
              ))}
            </select>
          </div>

          {/* District */}
          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🏘️ District
            </label>
            <select
              value={selected.district}
              onChange={(e) => handleSelectChange('district', e.target.value)}
              disabled={!selected.state}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-500 text-sm disabled:bg-gray-100"
            >
              <option value="">-- Select District --</option>
              {districts.map(dist => (
                <option key={dist} value={dist}>{dist}</option>
              ))}
            </select>
          </div>

          {/* Crop */}
          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🌾 Crop
            </label>
            <select
              value={selected.crop}
              onChange={(e) => handleSelectChange('crop', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
            >
              <option value="">-- Select Crop --</option>
              {crops.map(crop => (
                <option key={crop} value={crop}>{crop}</option>
              ))}
            </select>
          </div>

          {/* Season */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🌦️ Season
            </label>
            <select
              value={selected.season}
              onChange={(e) => handleSelectChange('season', e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
            >
              <option value="">-- Select Season --</option>
              {seasons.map(season => (
                <option key={season} value={season}>{season}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Farmer Inputs */}
        <div className="mb-8 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <h3 className="font-semibold text-gray-800 mb-4 text-sm">FARM DETAILS</h3>

          {/* Soil Type */}
          <div className="mb-3">
            <label className="block text-xs font-semibold text-gray-700 mb-1">
              Soil Type
            </label>
            <select
              value={selected.soilType}
              onChange={(e) => handleSelectChange('soilType', e.target.value)}
              className="w-full px-2 py-1 border border-gray-300 rounded-lg bg-white text-xs"
            >
              {SOIL_TYPES.map(soil => (
                <option key={soil} value={soil}>{soil}</option>
              ))}
            </select>
          </div>

          {/* Land Type */}
          <div className="mb-3">
            <label className="block text-xs font-semibold text-gray-700 mb-1">
              Land Type
            </label>
            <select
              value={selected.landType}
              onChange={(e) => handleSelectChange('landType', e.target.value)}
              className="w-full px-2 py-1 border border-gray-300 rounded-lg bg-white text-xs"
            >
              {LAND_TYPES.map(land => (
                <option key={land} value={land}>{land}</option>
              ))}
            </select>
          </div>

          {/* Sowing Month */}
          <div className="mb-3">
            <label className="block text-xs font-semibold text-gray-700 mb-1">
              Sowing Month
            </label>
            <select
              value={selected.sowingMonth}
              onChange={(e) => handleSelectChange('sowingMonth', parseInt(e.target.value))}
              className="w-full px-2 py-1 border border-gray-300 rounded-lg bg-white text-xs"
            >
              {MONTHS.map(month => (
                <option key={month.val} value={month.val}>{month.name}</option>
              ))}
            </select>
          </div>

          {/* Farm Size */}
          <div>
            <label className="block text-xs font-semibold text-gray-700 mb-1">
              Farm Size (acres)
            </label>
            <select
              value={selected.farmSize}
              onChange={(e) => handleSelectChange('farmSize', parseFloat(e.target.value))}
              className="w-full px-2 py-1 border border-gray-300 rounded-lg bg-white text-xs"
            >
              {FARM_SIZES.map(size => (
                <option key={size} value={size}>{size}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={!isComplete || loading}
        className={`w-full py-3 px-4 rounded-lg font-bold transition flex items-center justify-center gap-2 mb-4 ${
          isComplete && !loading
            ? 'bg-gradient-to-r from-green-600 to-green-500 text-white hover:from-green-700 hover:to-green-600 shadow-lg'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        <Play size={18} />
        {loading ? 'Analyzing...' : 'Analyze Risk'}
      </button>

      {/* Info */}
      <div className="text-xs text-gray-600 bg-gray-50 p-3 rounded-lg">
        <p className="font-semibold mb-2">ℹ️ This system uses:</p>
        <ul className="space-y-1">
          <li>• Real-time satellite NDVI data</li>
          <li>• Live weather & soil moisture</li>
          <li>• ML-based risk prediction</li>
        </ul>
      </div>
    </div>
  );
}

export default EnhancedSidebar;

import React, { useState, useEffect } from 'react';
import { ChevronDown, Play } from 'lucide-react';
import axios from 'axios';

function Sidebar({ onAnalyze, loading }) {
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [crops, setCrops] = useState([]);
  const [seasons, setSeasons] = useState([]);

  const [selected, setSelected] = useState({
    state: '',
    district: '',
    crop: '',
    season: ''
  });

  // Use relative API base to work with Vite proxy (/api -> backend)
  const API_BASE = '/api';

  useEffect(() => {
    // Fetch configuration
    const fetchConfig = async () => {
      try {
        const response = await axios.get(`${API_BASE}/config`);
        setStates(response.data.states);
        setCrops(response.data.crops);
        setSeasons(response.data.seasons);
      } catch (error) {
        console.error('Failed to fetch config:', error);
        // Fallback options if backend is unavailable
        setStates([
          'Maharashtra','Gujarat','Karnataka','Tamil Nadu','Telangana','Uttar Pradesh','Rajasthan','Punjab','West Bengal','Kerala'
        ]);
        setCrops(['Rice','Wheat','Corn','Cotton','Sugarcane','Soybean','Pulses']);
        setSeasons(['Kharif','Rabi','Summer']);
      }
    };
    fetchConfig();
  }, []);

  useEffect(() => {
    // Fetch districts when state changes
    if (selected.state) {
      const fetchDistricts = async () => {
        try {
          const response = await axios.get(`${API_BASE}/districts/${selected.state}`);
          setDistricts(response.data.districts);
        } catch (error) {
          console.error('Failed to fetch districts:', error);
          // Basic fallbacks for common states
          const FALLBACK = {
            'Maharashtra': ['Mumbai','Pune','Nashik','Solapur'],
            'Gujarat': ['Ahmedabad','Surat','Rajkot','Vadodara'],
            'Karnataka': ['Bengaluru','Mysuru','Belagavi','Kalaburagi'],
            'Tamil Nadu': ['Chennai','Coimbatore','Madurai','Thanjavur'],
            'Telangana': ['Hyderabad','Warangal','Karimnagar','Nizamabad'],
            'Uttar Pradesh': ['Agra','Meerut','Kanpur','Lucknow'],
            'Rajasthan': ['Jaipur','Jodhpur','Bikaner','Barmer'],
            'Punjab': ['Amritsar','Ludhiana','Sangrur','Moga'],
            'West Bengal': ['Kolkata','Howrah','Durgapur','Malda'],
            'Kerala': ['Thiruvananthapuram','Kochi','Kozhikode','Palakkad']
          };
          setDistricts(FALLBACK[selected.state] || []);
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
    <div className="w-80 bg-white border-r border-gray-200 shadow-md p-6 flex flex-col h-screen sticky top-20">
      <div className="flex-1">
        <h2 className="text-xl font-bold text-gray-800 mb-6 flex items-center gap-2">
          <span className="text-2xl">⚙️</span> Analysis Panel
        </h2>

        <div className="space-y-5">
          {/* State Selector */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              📍 Select State
            </label>
            <div className="relative">
              <select
                value={selected.state}
                onChange={(e) => handleSelectChange('state', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg appearance-none bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
              >
                <option value="">-- Choose a state --</option>
                {states.map(state => (
                  <option key={state} value={state}>{state}</option>
                ))}
              </select>
              <ChevronDown size={18} className="absolute right-3 top-3.5 text-gray-500 pointer-events-none" />
            </div>
          </div>

          {/* District Selector */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🏘️ Select District
            </label>
            <div className="relative">
              <select
                value={selected.district}
                onChange={(e) => handleSelectChange('district', e.target.value)}
                disabled={!selected.state}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg appearance-none bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition disabled:bg-gray-100 disabled:text-gray-500"
              >
                <option value="">-- Choose a district --</option>
                {districts.map(district => (
                  <option key={district} value={district}>{district}</option>
                ))}
              </select>
              <ChevronDown size={18} className="absolute right-3 top-3.5 text-gray-500 pointer-events-none" />
            </div>
          </div>

          {/* Crop Selector */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🌾 Select Crop
            </label>
            <div className="relative">
              <select
                value={selected.crop}
                onChange={(e) => handleSelectChange('crop', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg appearance-none bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
              >
                <option value="">-- Choose a crop --</option>
                {crops.map(crop => (
                  <option key={crop} value={crop}>{crop}</option>
                ))}
              </select>
              <ChevronDown size={18} className="absolute right-3 top-3.5 text-gray-500 pointer-events-none" />
            </div>
          </div>

          {/* Season Selector */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              🌦️ Select Season
            </label>
            <div className="relative">
              <select
                value={selected.season}
                onChange={(e) => handleSelectChange('season', e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg appearance-none bg-white cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent transition"
              >
                <option value="">-- Choose a season --</option>
                {seasons.map(season => (
                  <option key={season} value={season}>{season}</option>
                ))}
              </select>
              <ChevronDown size={18} className="absolute right-3 top-3.5 text-gray-500 pointer-events-none" />
            </div>
          </div>
        </div>
      </div>

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={!isComplete || loading}
        className={`w-full py-3 px-4 rounded-lg font-semibold transition flex items-center justify-center gap-2 ${
          isComplete && !loading
            ? 'bg-gradient-to-r from-green-600 to-green-500 text-white hover:from-green-700 hover:to-green-600 shadow-lg'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        <Play size={18} />
        {loading ? 'Analyzing...' : 'Analyze Risk'}
      </button>

      {/* Info Box */}
      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-xs text-blue-800">
        <p className="font-semibold mb-2">💡 How it works:</p>
        <ul className="space-y-1 text-blue-700">
          <li>• Analyzes satellite NDVI data</li>
          <li>• Factors in weather patterns</li>
          <li>• Considers soil conditions</li>
          <li>• Evaluates pest risks</li>
        </ul>
      </div>
    </div>
  );
}

export default Sidebar;

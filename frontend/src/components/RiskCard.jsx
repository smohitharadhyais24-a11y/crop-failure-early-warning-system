import React from 'react';
import { AlertTriangle, CheckCircle, AlertCircle } from 'lucide-react';

function RiskCard({ riskLevel, probability }) {
  const getRiskColor = () => {
    switch(riskLevel) {
      case 'Low': return { bg: 'bg-green-100', border: 'border-green-300', text: 'text-green-800', icon: 'text-green-600' };
      case 'Medium': return { bg: 'bg-yellow-100', border: 'border-yellow-300', text: 'text-yellow-800', icon: 'text-yellow-600' };
      case 'High': return { bg: 'bg-red-100', border: 'border-red-300', text: 'text-red-800', icon: 'text-red-600' };
      default: return { bg: 'bg-gray-100', border: 'border-gray-300', text: 'text-gray-800', icon: 'text-gray-600' };
    }
  };

  const getRiskIcon = () => {
    switch(riskLevel) {
      case 'Low': return <CheckCircle size={48} />;
      case 'High': return <AlertTriangle size={48} />;
      default: return <AlertCircle size={48} />;
    }
  };

  const colors = getRiskColor();

  return (
    <div className={`${colors.bg} ${colors.border} border-2 rounded-lg shadow-lg p-8 text-center`}>
      <div className={`${colors.icon} flex justify-center mb-4`}>
        {getRiskIcon()}
      </div>
      <h2 className={`${colors.text} text-4xl font-bold mb-2`}>
        {riskLevel} Risk
      </h2>
      <p className={`${colors.text} text-lg mb-4`}>
        Probability of Crop Failure
      </p>
      <div className="text-5xl font-bold mb-2">
        <span className={`${colors.text}`}>{(probability * 100).toFixed(1)}%</span>
      </div>
      <div className={`${colors.text} text-sm mt-4`}>
        {riskLevel === 'Low' && '✓ Conditions appear favorable for crop growth'}
        {riskLevel === 'Medium' && '⚠️ Monitor weather and soil conditions closely'}
        {riskLevel === 'High' && '⚠️ Take preventive measures immediately'}
      </div>
    </div>
  );
}

export default RiskCard;

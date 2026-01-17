import React from 'react';
import { useTranslation } from 'react-i18next';
import { Globe } from 'lucide-react';

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const languages = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
    { code: 'kn', name: 'ಕನ್ನಡ', flag: '🇮🇳' }
  ];

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    localStorage.setItem('preferredLanguage', lng);
  };

  return (
    <div className="relative group">
      <button className="flex items-center gap-2 px-4 py-2 bg-white rounded-lg shadow hover:shadow-lg transition-all border border-gray-200">
        <Globe size={20} className="text-green-600" />
        <span className="font-medium text-gray-700">
          {languages.find(l => l.code === i18n.language)?.flag || '🌐'}
        </span>
      </button>
      
      <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-xl border border-gray-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
        {languages.map((lang) => (
          <button
            key={lang.code}
            onClick={() => changeLanguage(lang.code)}
            className={`w-full px-4 py-3 text-left hover:bg-green-50 transition-colors flex items-center gap-3 ${
              i18n.language === lang.code ? 'bg-green-100' : ''
            }`}
          >
            <span className="text-2xl">{lang.flag}</span>
            <div>
              <div className="font-medium text-gray-800">{lang.name}</div>
              {i18n.language === lang.code && (
                <div className="text-xs text-green-600">✓ Active</div>
              )}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

export default LanguageSwitcher;

import React from 'react';
import { Leaf, BarChart3, AlertCircle, Users, Zap, TrendingUp, ArrowRight } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from '../components/LanguageSwitcher';

function LandingPage({ onLaunch }) {
  const { t } = useTranslation();
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Leaf className="text-green-600" size={32} />
            <h1 className="text-2xl font-bold text-gray-900">{t('app.brand')}</h1>
          </div>
          <div className="flex items-center gap-4">
            <p className="text-gray-600 text-sm hidden sm:block">{t('app.tagline')}</p>
            <LanguageSwitcher />
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
        <h2 className="text-5xl font-bold text-gray-900 mb-4">
          {t('app.heroTitle')}
        </h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          {t('app.heroSubtitle')}
        </p>
      </section>

      {/* Objectives Section */}
      <section className="bg-white py-16 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h3 className="text-3xl font-bold text-gray-900 mb-12 text-center">
            {t('app.whyTitle')}
          </h3>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="p-6 border-l-4 border-green-600 bg-green-50 rounded-lg">
              <AlertCircle className="text-green-600 mb-4" size={28} />
              <h4 className="font-bold text-lg text-gray-900 mb-2">{t('app.whyEarlyWarning')}</h4>
              <p className="text-gray-600">{t('app.whyEarlyWarningDesc')}</p>
            </div>

            <div className="p-6 border-l-4 border-blue-600 bg-blue-50 rounded-lg">
              <TrendingUp className="text-blue-600 mb-4" size={28} />
              <h4 className="font-bold text-lg text-gray-900 mb-2">{t('app.whyReduceLosses')}</h4>
              <p className="text-gray-600">{t('app.whyReduceLossesDesc')}</p>
            </div>

            <div className="p-6 border-l-4 border-orange-600 bg-orange-50 rounded-lg">
              <BarChart3 className="text-orange-600 mb-4" size={28} />
              <h4 className="font-bold text-lg text-gray-900 mb-2">{t('app.whySmartRecs')}</h4>
              <p className="text-gray-600">{t('app.whySmartRecsDesc')}</p>
            </div>

            <div className="p-6 border-l-4 border-purple-600 bg-purple-50 rounded-lg">
              <Zap className="text-purple-600 mb-4" size={28} />
              <h4 className="font-bold text-lg text-gray-900 mb-2">{t('app.whyRealtime')}</h4>
              <p className="text-gray-600">{t('app.whyRealtimeDesc')}</p>
            </div>

            <div className="p-6 border-l-4 border-red-600 bg-red-50 rounded-lg">
              <Users className="text-red-600 mb-4" size={28} />
              <h4 className="font-bold text-lg text-gray-900 mb-2">{t('app.whyFarmerCentric')}</h4>
              <p className="text-gray-600">{t('app.whyFarmerCentricDesc')}</p>
            </div>

            <div className="p-6 border-l-4 border-indigo-600 bg-indigo-50 rounded-lg">
              <BarChart3 className="text-indigo-600 mb-4" size={28} />
              <h4 className="font-bold text-lg text-gray-900 mb-2">{t('app.whyExplainable')}</h4>
              <p className="text-gray-600">{t('app.whyExplainableDesc')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Who Should Use Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h3 className="text-3xl font-bold text-gray-900 mb-12 text-center">{t('app.whoTitle')}</h3>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-lg shadow-md text-center hover:shadow-lg transition">
            <div className="text-4xl mb-4">👨‍🌾</div>
            <h4 className="font-bold text-lg text-gray-900 mb-2">{t('app.whoFarmers')}</h4>
            <p className="text-gray-600">{t('app.whoFarmersDesc')}</p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-md text-center hover:shadow-lg transition">
            <div className="text-4xl mb-4">🏛️</div>
            <h4 className="font-bold text-lg text-gray-900 mb-2">{t('app.whoOfficers')}</h4>
            <p className="text-gray-600">{t('app.whoOfficersDesc')}</p>
          </div>

          <div className="bg-white p-8 rounded-lg shadow-md text-center hover:shadow-lg transition">
            <div className="text-4xl mb-4">📊</div>
            <h4 className="font-bold text-lg text-gray-900 mb-2">{t('app.whoNGO')}</h4>
            <p className="text-gray-600">{t('app.whoNGODesc')}</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-green-600 to-emerald-600 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h3 className="text-3xl font-bold mb-4">{t('app.ctaTitle')}</h3>
          <p className="text-lg mb-8 text-green-100">
            {t('app.ctaSubtitle')}
          </p>
          <button
            onClick={onLaunch}
            className="bg-white text-green-600 px-8 py-4 rounded-lg font-bold text-lg hover:bg-green-50 transition inline-flex items-center gap-2 shadow-lg"
          >
            {t('app.heroCTA')} <ArrowRight size={24} />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p>{t('app.footer')}</p>
        </div>
      </footer>
    </div>
  );
}

export default LandingPage;

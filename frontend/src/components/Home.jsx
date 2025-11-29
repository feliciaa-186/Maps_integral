import React from 'react';
import { Link } from 'react-router-dom';
import { MapPin, TrendingUp, BarChart3, Target } from 'lucide-react';

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-12">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-800 mb-4 animate-fade-in">
            Welcome to Maps Integral
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Your comprehensive platform for competitor analysis and business feasibility 
            studies in Delhi. Make data-driven decisions with AI-powered insights.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto mb-16">
          <Link to="/competitors" className="group">
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-2xl transition-all transform hover:-translate-y-2 duration-300 border-t-4 border-blue-600">
              <div className="flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl mb-6 group-hover:scale-110 transition-transform">
                <MapPin className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-3xl font-bold text-gray-800 mb-4">
                Competitors Analysis
              </h2>
              <p className="text-gray-600 text-lg leading-relaxed">
                Leverage AI to analyze competitor locations, identify market gaps, and discover 
                strategic opportunities using Google Gemini integration.
              </p>
              <div className="mt-6 flex items-center text-blue-600 font-semibold group-hover:gap-3 gap-2 transition-all">
                Explore Analysis <span className="text-2xl">→</span>
              </div>
            </div>
          </Link>

          <Link to="/business-feasibility" className="group">
            <div className="bg-white rounded-xl shadow-lg p-8 hover:shadow-2xl transition-all transform hover:-translate-y-2 duration-300 border-t-4 border-green-600">
              <div className="flex items-center justify-center w-20 h-20 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl mb-6 group-hover:scale-110 transition-transform">
                <TrendingUp className="w-10 h-10 text-white" />
              </div>
              <h2 className="text-3xl font-bold text-gray-800 mb-4">
                Business Feasibility
              </h2>
              <p className="text-gray-600 text-lg leading-relaxed">
                Explore Delhi's business landscape with detailed area analysis, risk scoring, 
                and 10-year success projections.
              </p>
              <div className="mt-6 flex items-center text-green-600 font-semibold group-hover:gap-3 gap-2 transition-all">
                Start Analysis <span className="text-2xl">→</span>
              </div>
            </div>
          </Link>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-10 max-w-5xl mx-auto">
          <h3 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            Platform Features
          </h3>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                  <BarChart3 className="w-8 h-8 text-blue-600" />
                </div>
              </div>
              <h4 className="font-semibold text-lg text-gray-800 mb-2">AI-Powered Insights</h4>
              <p className="text-gray-600">
                Leverage Google Gemini AI for intelligent competitor analysis and market research
              </p>
            </div>
            
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                  <MapPin className="w-8 h-8 text-green-600" />
                </div>
              </div>
              <h4 className="font-semibold text-lg text-gray-800 mb-2">Interactive Maps</h4>
              <p className="text-gray-600">
                Visualize data with advanced MapLibre GL maps and geospatial analysis
              </p>
            </div>
            
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center">
                  <Target className="w-8 h-8 text-purple-600" />
                </div>
              </div>
              <h4 className="font-semibold text-lg text-gray-800 mb-2">Risk Assessment</h4>
              <p className="text-gray-600">
                Calculate risk scores with 10-year projections and alternative recommendations
              </p>
            </div>
          </div>
        </div>

        <div className="mt-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-10 max-w-5xl mx-auto text-white shadow-2xl">
          <div className="text-center">
            <h3 className="text-3xl font-bold mb-4">Ready to Get Started?</h3>
            <p className="text-lg mb-8 opacity-90">
              Choose your analysis type and unlock powerful business intelligence
            </p>
            <div className="flex gap-4 justify-center">
              <Link 
                to="/competitors" 
                className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition shadow-lg"
              >
                Analyze Competitors
              </Link>
              <Link 
                to="/business-feasibility" 
                className="bg-transparent border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white/10 transition"
              >
                Check Feasibility
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

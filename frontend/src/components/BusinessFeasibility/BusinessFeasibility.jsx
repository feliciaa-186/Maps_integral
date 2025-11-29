import React, { useState } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, Legend 
} from 'recharts';
import { 
  TrendingUp, TrendingDown, MapPin, AlertTriangle, 
  Loader2, Search, CheckCircle, XCircle 
} from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const BusinessFeasibility = () => {
  const [formData, setFormData] = useState({
    businessType: '',
    location: '',
    pincode: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/api/feasibility/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Failed to analyze business feasibility');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (riskScore) => {
    if (riskScore < 30) return 'text-green-600';
    if (riskScore < 50) return 'text-yellow-600';
    if (riskScore < 70) return 'text-orange-600';
    return 'text-red-600';
  };

  const getRiskBgColor = (riskScore) => {
    if (riskScore < 30) return 'bg-green-50 border-green-200';
    if (riskScore < 50) return 'bg-yellow-50 border-yellow-200';
    if (riskScore < 70) return 'bg-orange-50 border-orange-200';
    return 'bg-red-50 border-red-200';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Business Feasibility Analysis
          </h1>
          <p className="text-gray-600">
            Analyze business viability with risk scoring and 10-year projections
          </p>
        </div>

        {/* Input Form */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Business Type *
                </label>
                <input
                  type="text"
                  required
                  value={formData.businessType}
                  onChange={(e) => setFormData({...formData, businessType: e.target.value})}
                  placeholder="e.g., Restaurant, Cafe, Retail"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location/Area *
                </label>
                <input
                  type="text"
                  required
                  value={formData.location}
                  onChange={(e) => setFormData({...formData, location: e.target.value})}
                  placeholder="e.g., Connaught Place"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Pincode (Optional)
                </label>
                <input
                  type="text"
                  value={formData.pincode}
                  onChange={(e) => setFormData({...formData, pincode: e.target.value})}
                  placeholder="e.g., 110001"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-green-600 to-green-700 text-white py-4 rounded-lg font-semibold hover:from-green-700 hover:to-green-800 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  Analyze Feasibility
                </>
              )}
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-8 flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5" />
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {/* Results */}
        {result && (
          <div className="space-y-8 animate-fade-in">
            {/* Risk Score Card */}
            <div className={`${getRiskBgColor(result.riskScore)} border-2 rounded-xl p-8`}>
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-2xl font-bold text-gray-800 mb-1">
                    Risk Assessment
                  </h2>
                  <p className="text-sm text-gray-600">
                    {result.location.area} • {result.location.pincode || 'N/A'}
                  </p>
                </div>
                <div className="text-right">
                  <div className={`text-5xl font-bold ${getRiskColor(result.riskScore)}`}>
                    {result.riskScore}%
                  </div>
                  <div className={`text-sm font-semibold ${getRiskColor(result.riskScore)}`}>
                    {result.riskLevel} Risk
                  </div>
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4 mt-6">
                <div className="flex items-center gap-3">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="text-gray-700">
                    <strong>{result.positiveCount}</strong> Positive Factors
                  </span>
                </div>
                <div className="flex items-center gap-3">
                  <XCircle className="w-5 h-5 text-red-600" />
                  <span className="text-gray-700">
                    <strong>{result.negativeCount}</strong> Negative Factors
                  </span>
                </div>
              </div>
            </div>

            {/* 10-Year Projection Chart */}
            <div className="bg-white rounded-xl shadow-lg p-8">
              <h3 className="text-2xl font-bold text-gray-800 mb-6">
                10-Year Success Projection
              </h3>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={result.projectionData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="year" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="probability" 
                    stroke="#10b981" 
                    strokeWidth={3}
                    name="Success Probability (%)"
                  />
                  <Line 
                    type="monotone" 
                    dataKey="risk" 
                    stroke="#ef4444" 
                    strokeWidth={3}
                    name="Risk (%)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            {/* Events Impact */}
            {result.events && result.events.length > 0 && (
              <div className="bg-white rounded-xl shadow-lg p-8">
                <h3 className="text-2xl font-bold text-gray-800 mb-6">
                  Impacting Events ({result.events.length})
                </h3>
                <div className="space-y-4">
                  {result.events.map((event, idx) => (
                    <div 
                      key={idx}
                      className={`p-4 rounded-lg border-l-4 ${
                        event.impact.sentiment === 'POSITIVE' 
                          ? 'bg-green-50 border-green-500' 
                          : 'bg-red-50 border-red-500'
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="font-semibold text-gray-800 mb-1">
                            {event.name}
                          </h4>
                          <p className="text-sm text-gray-600 mb-2">
                            {event.description}
                          </p>
                          <div className="flex items-center gap-4 text-xs text-gray-500">
                            <span className="flex items-center gap-1">
                              <MapPin className="w-3 h-3" />
                              {event.distance_meters ? 
                                `${(event.distance_meters / 1000).toFixed(1)} km away` 
                                : 'Sector-matched'}
                            </span>
                            <span>
                              Impact: {event.impact.score > 0 ? '+' : ''}{event.impact.score}
                            </span>
                          </div>
                        </div>
                        <div className="ml-4">
                          {event.impact.sentiment === 'POSITIVE' ? (
                            <TrendingUp className="w-6 h-6 text-green-600" />
                          ) : (
                            <TrendingDown className="w-6 h-6 text-red-600" />
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Alternative Recommendations */}
            {result.alternatives && result.alternatives.length > 0 && (
              <div className="grid md:grid-cols-2 gap-8">
                <div className="bg-white rounded-xl shadow-lg p-8">
                  <h3 className="text-xl font-bold text-gray-800 mb-4">
                    Alternative Locations
                  </h3>
                  <div className="space-y-3">
                    {result.alternatives.map((alt, idx) => (
                      <div key={idx} className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-semibold text-gray-800">{alt.area}</h4>
                          <span className="text-sm font-bold text-blue-600">
                            {alt.risk}% Risk
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mb-1">{alt.reason}</p>
                        <p className="text-xs text-gray-500">Pincode: {alt.pincode}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {result.alternateBusiness && result.alternateBusiness.length > 0 && (
                  <div className="bg-white rounded-xl shadow-lg p-8">
                    <h3 className="text-xl font-bold text-gray-800 mb-4">
                      Alternative Business Types
                    </h3>
                    <div className="space-y-3">
                      {result.alternateBusiness.map((alt, idx) => (
                        <div key={idx} className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                          <h4 className="font-semibold text-gray-800 mb-2">{alt.type}</h4>
                          <p className="text-sm text-gray-600">{alt.reason}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Formula Explanation */}
            <div className="bg-gray-50 rounded-lg p-6 border border-gray-200">
              <h4 className="font-semibold text-gray-700 mb-2">Risk Calculation Formula</h4>
              <code className="text-sm text-gray-600">{result.formula}</code>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default BusinessFeasibility;

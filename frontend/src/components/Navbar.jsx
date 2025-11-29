import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { MapPin } from 'lucide-react';

const Navbar = () => {
  const location = useLocation();
  
  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-700 text-white shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2 text-xl font-bold hover:text-blue-200 transition">
            <MapPin className="w-6 h-6" />
            Maps Integral
          </Link>
          <div className="flex space-x-1">
            <Link
              to="/"
              className={`px-4 py-2 rounded-md transition ${
                isActive('/') 
                  ? 'bg-blue-800 text-white' 
                  : 'hover:bg-blue-700/50'
              }`}
            >
              Home
            </Link>
            <Link
              to="/competitors"
              className={`px-4 py-2 rounded-md transition ${
                isActive('/competitors') 
                  ? 'bg-blue-800 text-white' 
                  : 'hover:bg-blue-700/50'
              }`}
            >
              Competitors Analysis
            </Link>
            <Link
              to="/business-feasibility"
              className={`px-4 py-2 rounded-md transition ${
                isActive('/business-feasibility') 
                  ? 'bg-blue-800 text-white' 
                  : 'hover:bg-blue-700/50'
              }`}
            >
              Business Feasibility
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;

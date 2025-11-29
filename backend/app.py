from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import math
import os
from datetime import datetime

app = Flask(__name__)

# Configure CORS for multiple origins
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "http://localhost:5173",
            "https://maps-reimagined-frontend.onrender.com",
            "https://*.onrender.com"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# ==================== UTILITY FUNCTIONS ====================

def load_json_file(filepath):
    """Load JSON file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON decode error in {filepath}: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Error loading {filepath}: {e}")
        return None

def save_json_file(filepath, data):
    """Save JSON data to file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving {filepath}: {e}")
        return False

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in meters"""
    R = 6371000  # Earth's radius in meters
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

# ==================== DATA INITIALIZATION ====================

def initialize_data():
    """Initialize all datasets"""
    print("=" * 60)
    print("INITIALIZING MAPS INTEGRAL API")
    print("=" * 60)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Initialize future events
    future_events = load_json_file('data/delhi_future_events.json') or []
    print(f"✓ Future events: {len(future_events)}")
    
    # Fallback Delhi areas
    delhi_areas = [
        {'name': 'Connaught Place', 'lat': 28.6315, 'lng': 77.2167},
        {'name': 'Karol Bagh', 'lat': 28.6519, 'lng': 77.1900},
        {'name': 'Saket', 'lat': 28.5244, 'lng': 77.2066},
        {'name': 'Dwarka', 'lat': 28.5921, 'lng': 77.0460},
        {'name': 'Rohini', 'lat': 28.7496, 'lng': 77.0669},
        {'name': 'Lajpat Nagar', 'lat': 28.5677, 'lng': 77.2433},
        {'name': 'Nehru Place', 'lat': 28.5494, 'lng': 77.2501},
        {'name': 'Chandni Chowk', 'lat': 28.6506, 'lng': 77.2303},
        {'name': 'Hauz Khas', 'lat': 28.5494, 'lng': 77.2001},
        {'name': 'Rajouri Garden', 'lat': 28.6414, 'lng': 77.1211},
    ]
    print(f"✓ Delhi areas: {len(delhi_areas)}")
    
    # Fallback pincodes
    delhi_pincodes = [
        {'pincode': '110001', 'area': 'Connaught Place', 'lat': 28.6315, 'lng': 77.2167},
        {'pincode': '110005', 'area': 'Karol Bagh', 'lat': 28.6519, 'lng': 77.1900},
        {'pincode': '110017', 'area': 'Saket', 'lat': 28.5244, 'lng': 77.2066},
        {'pincode': '110075', 'area': 'Dwarka', 'lat': 28.5921, 'lng': 77.0460},
        {'pincode': '110085', 'area': 'Rohini', 'lat': 28.7496, 'lng': 77.0669},
        {'pincode': '110024', 'area': 'Lajpat Nagar', 'lat': 28.5677, 'lng': 77.2433},
        {'pincode': '110019', 'area': 'Nehru Place', 'lat': 28.5494, 'lng': 77.2501},
        {'pincode': '110006', 'area': 'Chandni Chowk', 'lat': 28.6506, 'lng': 77.2303},
        {'pincode': '110016', 'area': 'Hauz Khas', 'lat': 28.5494, 'lng': 77.2001},
        {'pincode': '110027', 'area': 'Rajouri Garden', 'lat': 28.6414, 'lng': 77.1211},
    ]
    print(f"✓ Delhi pincodes: {len(delhi_pincodes)}")
    
    # Initialize competitors
    competitors_file = 'data/competitors.json'
    if not os.path.exists(competitors_file):
        save_json_file(competitors_file, [])
        print("✓ Created competitors.json")
    competitors = load_json_file(competitors_file) or []
    print(f"✓ Competitors: {len(competitors)}")
    
    print("=" * 60)
    
    return future_events, delhi_areas, delhi_pincodes, competitors

# Load data on startup
FUTURE_EVENTS, DELHI_AREAS, DELHI_PINCODES, COMPETITORS = initialize_data()

# ==================== ROOT & HEALTH ENDPOINTS ====================

@app.route('/')
def home():
    """Root endpoint"""
    return jsonify({
        'status': 'online',
        'message': 'Maps Integral API - Combined Business Intelligence Platform',
        'version': '2.0',
        'datasets': {
            'future_events': len(FUTURE_EVENTS),
            'areas': len(DELHI_AREAS),
            'pincodes': len(DELHI_PINCODES),
            'competitors': len(COMPETITORS)
        },
        'endpoints': {
            'business_feasibility': {
                'analyze': '/api/feasibility/analyze (POST)',
                'events': '/api/feasibility/events (GET)',
                'geocode': '/api/feasibility/geocode (GET)'
            },
            'competitors': {
                'list': '/api/competitors (GET)',
                'create': '/api/competitors (POST)',
                'get': '/api/competitors/<id> (GET)',
                'update': '/api/competitors/<id> (PUT)',
                'delete': '/api/competitors/<id> (DELETE)',
                'search': '/api/competitors/search (GET)',
                'nearby': '/api/competitors/nearby (GET)',
                'categories': '/api/competitors/categories (GET)',
                'stats': '/api/competitors/stats (GET)'
            },
            'health': '/api/health (GET)'
        }
    }), 200

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'datasets': {
            'future_events': len(FUTURE_EVENTS),
            'areas': len(DELHI_AREAS),
            'pincodes': len(DELHI_PINCODES),
            'competitors': len(COMPETITORS)
        }
    }), 200

# ==================== BUSINESS FEASIBILITY ENDPOINTS ====================

def geocode_location(area_name, pincode):
    """Get coordinates from area name or pincode"""
    area_name_lower = area_name.lower()
    
    # Try to find in areas database
    for area in DELHI_AREAS:
        if area_name_lower in area['name'].lower() or area['name'].lower() in area_name_lower:
            return area['lat'], area['lng']
    
    # Try to find by pincode
    if pincode:
        for pin_data in DELHI_PINCODES:
            if pin_data['pincode'] == str(pincode):
                return pin_data['lat'], pin_data['lng']
    
    # Default to Delhi center
    return 28.7041, 77.1025

def calculate_risk_score(positive_impacts, negative_impacts, business_type, location_factors):
    """Calculate risk score using formula"""
    base_risk = 50
    
    avg_positive = sum([abs(e['impact']['score']) for e in positive_impacts]) / len(positive_impacts) if positive_impacts else 0
    avg_negative = sum([abs(e['impact']['score']) for e in negative_impacts]) / len(negative_impacts) if negative_impacts else 0
    
    risk = base_risk + (avg_negative * 40) - (avg_positive * 30) + location_factors
    return max(0, min(100, round(risk, 2)))

def generate_10year_projection(events, business_type, base_success_rate=60):
    """Generate 10-year success probability projection"""
    current_year = datetime.now().year
    projection = []
    
    for year_offset in range(11):
        year = current_year + year_offset
        success_prob = base_success_rate
        
        for event in events:
            impact_year = datetime.fromisoformat(event['timelines']['impact_start'].replace('Z', '')).year
            
            if year >= impact_year:
                years_after_impact = year - impact_year
                decay_factor = math.exp(-0.1 * years_after_impact)
                impact_contribution = event['impact']['score'] * 30 * decay_factor
                success_prob += impact_contribution
        
        success_prob = max(20, min(95, success_prob))
        
        projection.append({
            'year': year,
            'probability': round(success_prob, 1),
            'risk': round(100 - success_prob, 1)
        })
    
    return projection

def find_alternative_locations(business_type, current_risk):
    """Suggest alternative locations with lower risk"""
    potential_areas = [
        {'name': 'Connaught Place', 'pincode': '110001', 'base_risk': 25, 'reason': 'High footfall, established commercial hub'},
        {'name': 'Saket', 'pincode': '110017', 'base_risk': 30, 'reason': 'Affluent residential area with strong retail demand'},
        {'name': 'Dwarka Sector 10', 'pincode': '110075', 'base_risk': 28, 'reason': 'New residential development, growing population'},
        {'name': 'Hauz Khas', 'pincode': '110016', 'base_risk': 32, 'reason': 'Young demographic, vibrant nightlife'},
        {'name': 'Nehru Place', 'pincode': '110019', 'base_risk': 35, 'reason': 'IT hub with high office worker population'},
        {'name': 'Lajpat Nagar', 'pincode': '110024', 'base_risk': 33, 'reason': 'Busy market area, excellent metro connectivity'}
    ]
    
    alternatives = [area for area in potential_areas if area['base_risk'] < current_risk]
    return sorted(alternatives, key=lambda x: x['base_risk'])[:3]

def suggest_alternative_businesses(business_type):
    """Suggest alternative business types"""
    business_alternatives = {
        'cafe': [
            {'type': 'Cloud Kitchen', 'reason': 'Lower overhead, delivery-focused model'},
            {'type': 'Co-working Space', 'reason': 'Growing remote work culture'}
        ],
        'restaurant': [
            {'type': 'Quick Service Restaurant (QSR)', 'reason': 'Faster turnover, lower staffing needs'},
            {'type': 'Ghost Kitchen', 'reason': 'Multi-brand delivery model'}
        ],
        'gym': [
            {'type': 'Yoga Studio', 'reason': 'Lower equipment costs, wellness trend'},
            {'type': 'Boutique Fitness Studio', 'reason': 'Premium pricing, loyal membership base'}
        ],
        'retail': [
            {'type': 'E-commerce Fulfillment Center', 'reason': 'Growing online shopping trend'},
            {'type': 'Experience Store', 'reason': 'Showroom + online sales model'}
        ],
        'default': [
            {'type': 'Service-based Business', 'reason': 'Lower inventory costs, flexible operations'},
            {'type': 'Franchise Opportunity', 'reason': 'Established brand, proven model'}
        ]
    }
    
    business_lower = business_type.lower()
    for key in business_alternatives:
        if key in business_lower:
            return business_alternatives[key]
    
    return business_alternatives['default']

@app.route('/api/feasibility/analyze', methods=['POST'])
def analyze_feasibility():
    """Business feasibility analysis endpoint"""
    try:
        data = request.json
        business_type = data.get('businessType', '')
        area_name = data.get('location', '')
        pincode = data.get('pincode', '')
        
        if not business_type or not area_name:
            return jsonify({'error': 'Business type and location are required'}), 400
        
        # Get coordinates
        lat, lng = geocode_location(area_name, pincode)
        
        # Find relevant future events
        relevant_events = []
        for event in FUTURE_EVENTS:
            distance = haversine_distance(lat, lng, event['location']['lat'], event['location']['lng'])
            
            if distance <= event['impact']['radius_meters']:
                event_copy = event.copy()
                event_copy['distance_meters'] = round(distance, 2)
                relevant_events.append(event_copy)
        
        # Check for sector-matched events
        for event in FUTURE_EVENTS:
            if event not in relevant_events:
                sectors = [s.lower() for s in event['impact']['affected_sectors']]
                if any(business_type.lower() in sector or sector in business_type.lower() for sector in sectors):
                    event_copy = event.copy()
                    event_copy['distance_meters'] = haversine_distance(lat, lng, event['location']['lat'], event['location']['lng'])
                    relevant_events.append(event_copy)
        
        # Separate positive and negative impacts
        positive_impacts = [e for e in relevant_events if e['impact']['sentiment'] == 'POSITIVE']
        negative_impacts = [e for e in relevant_events if e['impact']['sentiment'] == 'NEGATIVE']
        
        # Calculate risk score
        risk_score = calculate_risk_score(positive_impacts, negative_impacts, business_type, 0)
        
        # Generate projection
        projection_data = generate_10year_projection(relevant_events, business_type)
        
        # Generate alternatives if high risk
        alternatives = []
        alternate_businesses = []
        
        if risk_score > 40:
            alternatives = find_alternative_locations(business_type, risk_score)
            alternate_businesses = suggest_alternative_businesses(business_type)
        
        return jsonify({
            'riskScore': risk_score,
            'riskLevel': 'Low' if risk_score < 30 else 'Moderate' if risk_score < 50 else 'High' if risk_score < 70 else 'Very High',
            'location': {'lat': lat, 'lng': lng, 'area': area_name, 'pincode': pincode},
            'events': relevant_events,
            'positiveCount': len(positive_impacts),
            'negativeCount': len(negative_impacts),
            'projectionData': projection_data,
            'alternatives': alternatives,
            'alternateBusiness': alternate_businesses,
            'formula': 'Risk = 50 + (Avg_Negative × 40) - (Avg_Positive × 30) + Location_Factor'
        }), 200
        
    except Exception as e:
        print(f"Error in analysis: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/feasibility/events', methods=['GET'])
def get_all_events():
    """Get all future events"""
    return jsonify(FUTURE_EVENTS), 200

@app.route('/api/feasibility/geocode', methods=['GET'])
def geocode():
    """Geocode a location"""
    area = request.args.get('area', '')
    pincode = request.args.get('pincode', '')
    
    if not area and not pincode:
        return jsonify({'error': 'Area or pincode required'}), 400
    
    lat, lng = geocode_location(area, pincode)
    return jsonify({'lat': lat, 'lng': lng, 'area': area, 'pincode': pincode}), 200

# ==================== COMPETITORS ENDPOINTS ====================

@app.route('/api/competitors', methods=['GET'])
def get_competitors():
    """Get all competitors"""
    return jsonify({
        'success': True,
        'count': len(COMPETITORS),
        'data': COMPETITORS
    }), 200

@app.route('/api/competitors', methods=['POST'])
def create_competitor():
    """Create a new competitor"""
    try:
        data = request.json
        
        required_fields = ['name', 'lat', 'lng']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        new_id = max([c.get('id', 0) for c in COMPETITORS], default=0) + 1
        
        new_competitor = {
            'id': new_id,
            'name': data['name'],
            'lat': float(data['lat']),
            'lng': float(data['lng']),
            'address': data.get('address', ''),
            'category': data.get('category', 'Other'),
            'rating': data.get('rating', 0),
            'phone': data.get('phone', ''),
            'website': data.get('website', ''),
            'description': data.get('description', ''),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        COMPETITORS.append(new_competitor)
        save_json_file('data/competitors.json', COMPETITORS)
        
        return jsonify({'success': True, 'message': 'Competitor created', 'data': new_competitor}), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/competitors/<int:competitor_id>', methods=['GET'])
def get_competitor(competitor_id):
    """Get specific competitor"""
    competitor = next((c for c in COMPETITORS if c.get('id') == competitor_id), None)
    
    if competitor:
        return jsonify({'success': True, 'data': competitor}), 200
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.route('/api/competitors/<int:competitor_id>', methods=['PUT'])
def update_competitor(competitor_id):
    """Update a competitor"""
    try:
        data = request.json
        idx = next((i for i, c in enumerate(COMPETITORS) if c.get('id') == competitor_id), None)
        
        if idx is None:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        
        competitor = COMPETITORS[idx]
        competitor.update({
            'name': data.get('name', competitor.get('name')),
            'lat': float(data.get('lat', competitor.get('lat'))),
            'lng': float(data.get('lng', competitor.get('lng'))),
            'address': data.get('address', competitor.get('address', '')),
            'category': data.get('category', competitor.get('category', 'Other')),
            'rating': data.get('rating', competitor.get('rating', 0)),
            'phone': data.get('phone', competitor.get('phone', '')),
            'website': data.get('website', competitor.get('website', '')),
            'description': data.get('description', competitor.get('description', '')),
            'updated_at': datetime.now().isoformat()
        })
        
        COMPETITORS[idx] = competitor
        save_json_file('data/competitors.json', COMPETITORS)
        
        return jsonify({'success': True, 'message': 'Updated', 'data': competitor}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/competitors/<int:competitor_id>', methods=['DELETE'])
def delete_competitor(competitor_id):
    """Delete a competitor"""
    try:
        global COMPETITORS
        original_len = len(COMPETITORS)
        COMPETITORS = [c for c in COMPETITORS if c.get('id') != competitor_id]
        
        if len(COMPETITORS) == original_len:
            return jsonify({'success': False, 'error': 'Not found'}), 404
        
        save_json_file('data/competitors.json', COMPETITORS)
        return jsonify({'success': True, 'message': 'Deleted'}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/competitors/search', methods=['GET'])
def search_competitors():
    """Search competitors"""
    query = request.args.get('query', '').lower()
    
    if not query:
        return jsonify({'success': False, 'error': 'Query required'}), 400
    
    results = [
        c for c in COMPETITORS
        if query in c.get('name', '').lower()
        or query in c.get('category', '').lower()
        or query in c.get('address', '').lower()
    ]
    
    return jsonify({'success': True, 'count': len(results), 'data': results}), 200

@app.route('/api/competitors/nearby', methods=['GET'])
def get_nearby_competitors():
    """Get competitors within radius"""
    try:
        lat = float(request.args.get('lat'))
        lng = float(request.args.get('lng'))
        radius = float(request.args.get('radius', 5))
        
        nearby = []
        for competitor in COMPETITORS:
            distance = haversine_distance(lat, lng, competitor.get('lat', 0), competitor.get('lng', 0)) / 1000  # Convert to km
            
            if distance <= radius:
                comp_copy = competitor.copy()
                comp_copy['distance'] = round(distance, 2)
                nearby.append(comp_copy)
        
        nearby.sort(key=lambda x: x['distance'])
        
        return jsonify({
            'success': True,
            'count': len(nearby),
            'data': nearby,
            'center': {'lat': lat, 'lng': lng},
            'radius': radius
        }), 200
        
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid coordinates'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/competitors/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = list(set(c.get('category', 'Other') for c in COMPETITORS))
    categories.sort()
    return jsonify({'success': True, 'data': categories}), 200

@app.route('/api/competitors/stats', methods=['GET'])
def get_competitor_stats():
    """Get competitor statistics"""
    total = len(COMPETITORS)
    
    categories = {}
    total_rating = 0
    rated_count = 0
    
    for comp in COMPETITORS:
        cat = comp.get('category', 'Other')
        categories[cat] = categories.get(cat, 0) + 1
        
        rating = comp.get('rating', 0)
        if rating > 0:
            total_rating += rating
            rated_count += 1
    
    avg_rating = round(total_rating / rated_count, 2) if rated_count > 0 else 0
    
    return jsonify({
        'success': True,
        'data': {
            'total_competitors': total,
            'categories': categories,
            'average_rating': avg_rating,
            'rated_competitors': rated_count
        }
    }), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

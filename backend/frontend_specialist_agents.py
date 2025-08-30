#!/usr/bin/env python3
"""
IME Hub Maritime AI - Frontend Specialist Agents
Standalone file for Next.js frontend integration
"""

import json
import math
from datetime import datetime
from typing import Dict, Any, List
import google.generativeai as genai

# Hardcoded CSV data (same as in general captain)
PORTS_DATA = [
    {"port": "Singapore", "lat": 1.3521, "lon": 103.8198},
    {"port": "Durban", "lat": -29.8579, "lon": 31.0292},
    {"port": "Rotterdam", "lat": 51.9225, "lon": 4.47917},
    {"port": "Richards Bay", "lat": -28.7830, "lon": 32.0377},
    {"port": "Tubarão", "lat": -20.2707, "lon": -40.2647},
    {"port": "Qingdao", "lat": 36.0671, "lon": 120.3826},
    {"port": "New Orleans", "lat": 29.9511, "lon": -90.0715},
    {"port": "Alexandria", "lat": 31.2001, "lon": 29.9187}
]

BUNKER_PRICES = [
    {"port": "Singapore", "price_usd_per_ton": 600},
    {"port": "Rotterdam", "price_usd_per_ton": 580},
    {"port": "Durban", "price_usd_per_ton": 610},
    {"port": "Qingdao", "price_usd_per_ton": 590},
    {"port": "New Orleans", "price_usd_per_ton": 605}
]

VESSELS_DATA = [
    {"vessel_id": 1, "name": "Ocean Star", "dwt": 76000, "location": "Singapore", "laycan_start": "2025-09-05", "laycan_end": "2025-09-10", "speed": 14, "consumption": 25, "gear": "gearless"},
    {"vessel_id": 2, "name": "Pacific Trader", "dwt": 82000, "location": "Durban", "laycan_start": "2025-09-06", "laycan_end": "2025-09-12", "speed": 13, "consumption": 28, "gear": "cranes"},
    {"vessel_id": 3, "name": "Atlantic Carrier", "dwt": 100000, "location": "Rotterdam", "laycan_start": "2025-09-08", "laycan_end": "2025-09-15", "speed": 15, "consumption": 30, "gear": "gearless"}
]

CARGOS_DATA = [
    {"cargo_id": 1, "commodity": "Coal", "size": 70000, "load_port": "Richards Bay", "discharge_port": "Rotterdam", "laycan_start": "2025-09-05", "laycan_end": "2025-09-10", "freight_rate": 18, "requirements": "gearless"},
    {"cargo_id": 2, "commodity": "Iron Ore", "size": 80000, "load_port": "Tubarão", "discharge_port": "Qingdao", "laycan_start": "2025-09-06", "laycan_end": "2025-09-12", "freight_rate": 20, "requirements": "draft<18m"},
    {"cargo_id": 3, "commodity": "Grain", "size": 65000, "load_port": "New Orleans", "discharge_port": "Alexandria", "laycan_start": "2025-09-07", "laycan_end": "2025-09-14", "freight_rate": 22, "requirements": "cranes"}
]

WEATHER_DATA = [
    {"Port/Route": "Singapore", "Sea State": "Calm", "Wind": "Light Breeze", "Visibility": "Good"},
    {"Port/Route": "Rotterdam", "Sea State": "Moderate", "Wind": "Moderate Breeze", "Visibility": "Moderate"},
    {"Port/Route": "Durban", "Sea State": "Rough", "Wind": "Strong Breeze", "Visibility": "Poor"},
    {"Port/Route": "Richards Bay", "Sea State": "Moderate", "Wind": "Moderate Breeze", "Visibility": "Good"},
    {"Port/Route": "Tubarão", "Sea State": "Calm", "Wind": "Light Breeze", "Visibility": "Good"}
]

MARKET_TRENDS = [
    {"Year": 2021, "Freight Rate (USD/TEU)": 1200, "Bunker Price (USD/ton)": 450, "Demand Indicator": "High"},
    {"Year": 2022, "Freight Rate (USD/TEU)": 2500, "Bunker Price (USD/ton)": 520, "Demand Indicator": "Very High"},
    {"Year": 2023, "Freight Rate (USD/TEU)": 1800, "Bunker Price (USD/ton)": 480, "Demand Indicator": "Moderate"},
    {"Year": 2024, "Freight Rate (USD/TEU)": 2200, "Bunker Price (USD/ton)": 500, "Demand Indicator": "High"},
    {"Year": 2025, "Freight Rate (USD/TEU)": 2100, "Bunker Price (USD/ton)": 600, "Demand Indicator": "High"}
]

CANAL_DUES = [
    {"route": "Suez Canal", "type": "canal", "cost_usd": 300000},
    {"route": "Panama Canal", "type": "canal", "cost_usd": 250000},
    {"route": "Rotterdam", "type": "port", "cost_usd": 50000},
    {"route": "Singapore", "type": "port", "cost_usd": 45000},
    {"route": "Qingdao", "type": "port", "cost_usd": 48000}
]

PIRACY_ZONES = [
    {"Region": "Gulf of Aden", "Coordinates": "12.7N, 45.0E", "Risk Level": "High", "Recommendation": "Use naval escort"},
    {"Region": "Somalia Coast", "Coordinates": "2.0N, 50.0E", "Risk Level": "Very High", "Recommendation": "Avoid area"},
    {"Region": "West Africa", "Coordinates": "4.5N, 6.5E", "Risk Level": "High", "Recommendation": "Report to authorities"},
    {"Region": "Malacca Strait", "Coordinates": "2.5N, 101.5E", "Risk Level": "Moderate", "Recommendation": "Increase vigilance"},
    {"Region": "Indian Ocean", "Coordinates": "10.0N, 75.0E", "Risk Level": "Low", "Recommendation": "Standard precautions"}
]

FUEL_CONSUMPTION = [
    {"Speed (knots)": 13, "Fuel Consumption (tons/day)": 28, "Engine Efficiency (%)": 82},
    {"Speed (knots)": 14, "Fuel Consumption (tons/day)": 25, "Engine Efficiency (%)": 85},
    {"Speed (knots)": 15, "Fuel Consumption (tons/day)": 30, "Engine Efficiency (%)": 80},
    {"Speed (knots)": 16, "Fuel Consumption (tons/day)": 35, "Engine Efficiency (%)": 78},
    {"Speed (knots)": 17, "Fuel Consumption (tons/day)": 40, "Engine Efficiency (%)": 76}
]

PORT_FACILITIES = [
    {"Port": "Singapore", "Bunker Availability": "Yes", "Cargo Handling": "Excellent", "Berth Availability": "High"},
    {"Port": "Rotterdam", "Bunker Availability": "Yes", "Cargo Handling": "Excellent", "Berth Availability": "Moderate"},
    {"Port": "Durban", "Bunker Availability": "Yes", "Cargo Handling": "Good", "Berth Availability": "Moderate"},
    {"Port": "Richards Bay", "Bunker Availability": "Limited", "Cargo Handling": "Good", "Berth Availability": "Low"},
    {"Port": "Tubarão", "Bunker Availability": "Yes", "Cargo Handling": "Moderate", "Berth Availability": "Moderate"}
]

VOYAGE_HISTORY = [
    {"Voyage ID": "V001", "Route": "Singapore-Rotterdam", "Estimated Cost (USD)": 500000, "Actual Cost (USD)": 520000},
    {"Voyage ID": "V002", "Route": "Durban-Rotterdam", "Estimated Cost (USD)": 750000, "Actual Cost (USD)": 740000},
    {"Voyage ID": "V003", "Route": "Richards Bay-Qingdao", "Estimated Cost (USD)": 680000, "Actual Cost (USD)": 690000},
    {"Voyage ID": "V004", "Route": "Tubarão-Qingdao", "Estimated Cost (USD)": 720000, "Actual Cost (USD)": 730000},
    {"Voyage ID": "V005", "Route": "New Orleans-Alexandria", "Estimated Cost (USD)": 450000, "Actual Cost (USD)": 460000}
]

class VoyagePlanningAgent:
    """Smart Voyage Planning & Optimization Agent"""
    
    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        self._init_gemini()
    
    def _init_gemini(self):
        try:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.conversation = None
        except:
            self.model = None
            self.conversation = None
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process voyage planning queries"""
        
        # Extract route information
        route = self._extract_route(query)
        if not route:
            return {
                "response": "I need to know which route you'd like me to analyze. Please specify the departure and destination ports.",
                "data": {},
                "suggestions": ["Try asking: 'What's the optimal route from Singapore to Rotterdam?'"]
            }
        
        # Analyze route
        route_analysis = self._analyze_route(route)
        
        # Get AI insights
        ai_insight = self._get_ai_insight(query, route_analysis)
        
        return {
            "response": ai_insight,
            "data": route_analysis,
            "suggestions": [
                "Consider slow steaming for fuel cost optimization",
                "Check weather conditions along the route",
                "Evaluate alternative routes for safety"
            ]
        }
    
    def _extract_route(self, query: str) -> str:
        """Extract route from query"""
        if '-' in query:
            parts = query.split('-')
            if len(parts) >= 2:
                return f"{parts[0].strip()}-{parts[1].strip()}"
        return None
    
    def _analyze_route(self, route: str) -> Dict[str, Any]:
        """Analyze route comprehensively"""
        departure, destination = route.split('-')
        
        # Calculate distance
        distance = self._calculate_distance(departure, destination)
        
        # Get weather conditions
        weather_dep = self._get_weather(departure)
        weather_dest = self._get_weather(destination)
        
        # Calculate fuel consumption
        fuel_analysis = self._calculate_fuel_consumption(distance)
        
        # Check canal requirements
        canal_info = self._check_canal_requirements(departure, destination)
        
        # Risk assessment
        risk_assessment = self._assess_route_risks(departure, destination)
        
        return {
            "route": route,
            "distance_nm": distance,
            "departure_port": {"name": departure, "weather": weather_dep},
            "destination_port": {"name": destination, "weather": weather_dest},
            "fuel_analysis": fuel_analysis,
            "canal_requirements": canal_info,
            "risk_assessment": risk_assessment,
            "estimated_duration": self._estimate_duration(distance)
        }
    
    def _calculate_distance(self, port1: str, port2: str) -> float:
        """Calculate distance between ports"""
        try:
            port1_data = next((p for p in PORTS_DATA if p['port'] == port1), None)
            port2_data = next((p for p in PORTS_DATA if p['port'] == port2), None)
            
            if port1_data and port2_data:
                lat1, lon1 = port1_data['lat'], port1_data['lon']
                lat2, lon2 = port2_data['lat'], port2_data['lon']
                
                # Approximate distance calculation
                distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 * 60
                return round(distance, 0)
        except:
            pass
        return 0
    
    def _get_weather(self, port: str) -> Dict[str, Any]:
        """Get weather for port"""
        return next((w for w in WEATHER_DATA if w['Port/Route'] == port), None)
    
    def _calculate_fuel_consumption(self, distance: float) -> Dict[str, Any]:
        """Calculate fuel consumption for different speeds"""
        if not distance:
            return {}
        
        fuel_analysis = {}
        for fuel_data in FUEL_CONSUMPTION:
            speed = fuel_data['Speed (knots)']
            daily_consumption = fuel_data['Fuel Consumption (tons/day)']
            efficiency = fuel_data['Engine Efficiency (%)']
            
            voyage_days = distance / (speed * 24)
            total_fuel = daily_consumption * voyage_days
            
            fuel_analysis[f"{speed}_knots"] = {
                "daily_consumption_tons": daily_consumption,
                "efficiency_percent": efficiency,
                "voyage_duration_days": round(voyage_days, 1),
                "total_fuel_tons": round(total_fuel, 1)
            }
        
        return fuel_analysis
    
    def _check_canal_requirements(self, departure: str, destination: str) -> Dict[str, Any]:
        """Check if route requires canal passage"""
        if departure in ['Singapore', 'Qingdao'] and destination in ['Rotterdam', 'New Orleans']:
            return {
                "canal_required": "Suez Canal",
                "estimated_fee_usd": 300000,
                "additional_time": "2-3 days"
            }
        elif departure in ['New Orleans'] and destination in ['Qingdao', 'Singapore']:
            return {
                "canal_required": "Panama Canal",
                "estimated_fee_usd": 250000,
                "additional_time": "1-2 days"
            }
        else:
            return {
                "canal_required": "None",
                "estimated_fee_usd": 0,
                "additional_time": "0 days"
            }
    
    def _assess_route_risks(self, departure: str, destination: str) -> Dict[str, Any]:
        """Assess route risks"""
        return {
            "piracy_risk": "Low",
            "weather_risk": "Moderate",
            "recommendations": ["Monitor weather conditions", "Standard security protocols"]
        }
    
    def _estimate_duration(self, distance: float) -> Dict[str, Any]:
        """Estimate voyage duration"""
        if not distance:
            return {}
        
        duration_estimates = {}
        for fuel_data in FUEL_CONSUMPTION:
            speed = fuel_data['Speed (knots)']
            voyage_days = distance / (speed * 24)
            duration_estimates[f"{speed}_knots"] = round(voyage_days, 1)
        
        return duration_estimates
    
    def _get_ai_insight(self, query: str, route_analysis: Dict[str, Any]) -> str:
        """Get AI insight for route analysis"""
        if not self.model:
            return self._get_fallback_response(route_analysis)
        
        try:
            prompt = f"""
            You are Captain Michael Rodriguez, a senior voyage optimization specialist with 20+ years of experience in maritime route planning and fuel optimization. You are analyzing a commercial voyage for IME Hub's maritime clients.

            CRITICAL INSTRUCTIONS:
            - Provide expert-level voyage optimization analysis
            - Focus on commercial viability, fuel efficiency, and operational safety
            - Use precise maritime terminology and industry standards
            - Reference specific data points and calculations
            - Consider commercial implications and cost optimization

            VOYAGE ANALYSIS DATA:
            Route: {route_analysis['route']}
            Distance: {route_analysis['distance_nm']} nautical miles
            Fuel Analysis: {json.dumps(route_analysis['fuel_analysis'], indent=2)}
            Canal Requirements: {json.dumps(route_analysis['canal_requirements'], indent=2)}
            Risk Assessment: {json.dumps(route_analysis['risk_assessment'], indent=2)}

            RESPONSE STRUCTURE:
            1. **Route Assessment**: Professional evaluation of the route (2-3 sentences)
            2. **Fuel Optimization**: Specific fuel consumption analysis with recommendations (2-3 sentences)
            3. **Commercial Analysis**: Cost implications and operational efficiency (2-3 sentences)
            4. **Risk Management**: Safety considerations and mitigation strategies (1-2 sentences)

            TONE: Professional maritime expert, commercial focus, actionable insights
            LENGTH: 4-6 sentences maximum
            DOMAIN: Maritime voyage optimization, fuel efficiency, commercial shipping ONLY
            """
            
            if self.conversation is None:
                self.conversation = self.model.start_chat(history=[])
            
            response = self.conversation.send_message(prompt)
            return response.text
            
        except:
            return self._get_fallback_response(route_analysis)
    
    def _get_fallback_response(self, route_analysis: Dict[str, Any]) -> str:
        """Get fallback response when AI is unavailable"""
        route = route_analysis['route']
        distance = route_analysis['distance_nm']
        
        return f"Route analysis for {route}: This {distance} nautical mile voyage offers several optimization opportunities. The route requires {route_analysis['canal_requirements']['canal_required']} with estimated fees of ${route_analysis['canal_requirements']['estimated_fee_usd']:,}. Consider optimizing speed for fuel efficiency - at 14 knots, you'll consume approximately {route_analysis['fuel_analysis']['14_knots']['total_fuel_tons']} tons of fuel over {route_analysis['fuel_analysis']['14_knots']['voyage_duration_days']} days."

class CargoMatchingAgent:
    """Cargo & Tonnage Matching Assistant"""
    
    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        self._init_gemini()
    
    def _init_gemini(self):
        try:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.conversation = None
        except:
            self.model = None
            self.conversation = None
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process cargo matching queries"""
        
        # Extract cargo and vessel information
        cargo_info = self._extract_cargo_info(query)
        vessel_info = self._extract_vessel_info(query)
        
        if not cargo_info and not vessel_info:
            return {
                "response": "I need more information to help with cargo-vessel matching. Please specify cargo details, vessel requirements, or ask about available options.",
                "data": {},
                "suggestions": [
                    "Try asking: 'What vessels are available for coal cargo?'",
                    "Or: 'What cargoes can Ocean Star carry?'"
                ]
            }
        
        # Generate matches
        matches = self._generate_matches(cargo_info, vessel_info)
        
        # Calculate profitability
        profitability_analysis = self._analyze_profitability(matches)
        
        return {
            "response": self._get_ai_insight(query, matches, profitability_analysis),
            "data": {
                "matches": matches,
                "profitability_analysis": profitability_analysis,
                "cargo_info": cargo_info,
                "vessel_info": vessel_info
            },
            "suggestions": [
                "Consider vessel availability and laycan windows",
                "Evaluate technical requirements compatibility",
                "Analyze freight rate vs. operational costs"
            ]
        }
    
    def _extract_cargo_info(self, query: str) -> Dict[str, Any]:
        """Extract cargo information from query"""
        cargo_info = {}
        
        # Check for specific cargo types
        for cargo in CARGOS_DATA:
            if cargo['commodity'].lower() in query.lower():
                cargo_info['commodity'] = cargo['commodity']
                break
        
        return cargo_info
    
    def _extract_vessel_info(self, query: str) -> Dict[str, Any]:
        """Extract vessel information from query"""
        vessel_info = {}
        
        # Check for specific vessel names
        for vessel in VESSELS_DATA:
            if vessel['name'].lower() in query.lower():
                vessel_info['name'] = vessel['name']
                break
        
        return vessel_info
    
    def _generate_matches(self, cargo_info: Dict[str, Any], vessel_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate cargo-vessel matches"""
        matches = []
        
        # If specific cargo is mentioned, find compatible vessels
        if cargo_info.get('commodity'):
            for cargo in CARGOS_DATA:
                if cargo['commodity'].lower() == cargo_info['commodity'].lower():
                    compatible_vessels = self._find_compatible_vessels(cargo, VESSELS_DATA)
                    for vessel in compatible_vessels:
                        match = self._create_match(cargo, vessel)
                        if match:
                            matches.append(match)
        
        # If specific vessel is mentioned, find compatible cargoes
        elif vessel_info.get('name'):
            for vessel in VESSELS_DATA:
                if vessel['name'].lower() == vessel_info['name'].lower():
                    compatible_cargoes = self._find_compatible_cargoes(vessel, CARGOS_DATA)
                    for cargo in compatible_cargoes:
                        match = self._create_match(cargo, vessel)
                        if match:
                            matches.append(match)
        
        # If no specific info, generate all possible matches
        else:
            for cargo in CARGOS_DATA:
                compatible_vessels = self._find_compatible_vessels(cargo, VESSELS_DATA)
                for vessel in compatible_vessels:
                    match = self._create_match(cargo, vessel)
                    if match:
                        matches.append(match)
        
        # Sort by compatibility score
        matches.sort(key=lambda x: x.get('compatibility_score', 0), reverse=True)
        return matches[:5]
    
    def _find_compatible_vessels(self, cargo: Dict[str, Any], vessels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find vessels compatible with cargo"""
        compatible_vessels = []
        
        for vessel in vessels:
            compatibility_score = 0
            
            # Check DWT compatibility
            if vessel['dwt'] >= cargo['size']:
                compatibility_score += 30
                if vessel['dwt'] <= cargo['size'] * 1.2:
                    compatibility_score += 20
            
            # Check gear compatibility
            if cargo['requirements'] == 'gearless' and vessel['gear'] == 'gearless':
                compatibility_score += 25
            elif cargo['requirements'] == 'cranes' and vessel['gear'] == 'cranes':
                compatibility_score += 25
            
            if compatibility_score >= 50:
                vessel['compatibility_score'] = compatibility_score
                compatible_vessels.append(vessel)
        
        return compatible_vessels
    
    def _find_compatible_cargoes(self, vessel: Dict[str, Any], cargoes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find cargoes compatible with vessel"""
        compatible_cargoes = []
        
        for cargo in cargoes:
            compatibility_score = 0
            
            # Check DWT compatibility
            if vessel['dwt'] >= cargo['size']:
                compatibility_score += 30
                if vessel['dwt'] <= cargo['size'] * 1.2:
                    compatibility_score += 20
            
            # Check gear compatibility
            if cargo['requirements'] == 'gearless' and vessel['gear'] == 'gearless':
                compatibility_score += 25
            elif cargo['requirements'] == 'cranes' and vessel['gear'] == 'cranes':
                compatibility_score += 25
            
            if compatibility_score >= 50:
                cargo['compatibility_score'] = compatibility_score
                compatible_cargoes.append(cargo)
        
        return compatible_cargoes
    
    def _create_match(self, cargo: Dict[str, Any], vessel: Dict[str, Any]) -> Dict[str, Any]:
        """Create a match object"""
        return {
            "cargo": cargo,
            "vessel": vessel,
            "compatibility_score": vessel.get('compatibility_score', 0),
            "match_type": "Optimal" if vessel.get('compatibility_score', 0) >= 80 else "Good" if vessel.get('compatibility_score', 0) >= 60 else "Acceptable"
        }
    
    def _analyze_profitability(self, matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze profitability for matches"""
        profitability_data = {}
        
        for i, match in enumerate(matches):
            cargo = match['cargo']
            vessel = match['vessel']
            
            # Calculate estimated costs (simplified)
            estimated_costs = 200000  # Base operational costs
            freight_revenue = cargo['size'] * cargo['freight_rate']
            profit = freight_revenue - estimated_costs
            profit_margin = (profit / freight_revenue) * 100 if freight_revenue > 0 else 0
            
            profitability_data[f"match_{i+1}"] = {
                "freight_revenue_usd": freight_revenue,
                "estimated_costs_usd": estimated_costs,
                "estimated_profit_usd": profit,
                "profit_margin_percent": round(profit_margin, 2)
            }
        
        return profitability_data
    
    def _get_ai_insight(self, query: str, matches: List[Dict[str, Any]], profitability: Dict[str, Any]) -> str:
        """Get AI insight for cargo matching"""
        if not self.model:
            return self._get_fallback_response(matches, profitability)
        
        try:
            prompt = f"""
            You are Captain Elena Vasquez, a senior chartering manager with 18+ years of experience in cargo-vessel optimization and commercial shipping at IME Hub. You are analyzing chartering opportunities for maritime clients.

            CRITICAL INSTRUCTIONS:
            - Provide expert-level chartering analysis and recommendations
            - Focus on commercial viability, profitability, and operational efficiency
            - Use precise maritime chartering terminology and industry standards
            - Reference specific compatibility scores, freight rates, and profit margins
            - Consider market conditions and operational requirements

            CHARTERING ANALYSIS DATA:
            Query: {query}
            Cargo-Vessel Matches: {json.dumps(matches, indent=2)}
            Profitability Analysis: {json.dumps(profitability, indent=2)}

            RESPONSE STRUCTURE:
            1. **Match Assessment**: Professional evaluation of cargo-vessel compatibility (2-3 sentences)
            2. **Commercial Analysis**: Profitability analysis with specific numbers (2-3 sentences)
            3. **Operational Recommendations**: Chartering strategy and optimization (2-3 sentences)
            4. **Risk Considerations**: Compatibility risks and mitigation (1-2 sentences)

            TONE: Professional chartering expert, commercial focus, actionable insights
            LENGTH: 4-6 sentences maximum
            DOMAIN: Maritime chartering, cargo-vessel optimization, commercial shipping ONLY
            """
            
            if self.conversation is None:
                self.conversation = self.model.start_chat(history=[])
            
            response = self.conversation.send_message(prompt)
            return response.text
            
        except:
            return self._get_fallback_response(matches, profitability)
    
    def _get_fallback_response(self, matches: List[Dict[str, Any]], profitability: Dict[str, Any]) -> str:
        """Get fallback response"""
        if not matches:
            return "No compatible cargo-vessel matches found. Consider adjusting requirements or checking availability."
        
        best_match = matches[0]
        cargo = best_match['cargo']
        vessel = best_match['vessel']
        
        return f"Best match found: {cargo['commodity']} cargo ({cargo['size']} tons) with {vessel['name']} vessel. Compatibility score: {best_match['compatibility_score']}/100. This match shows {best_match['match_type']} compatibility and offers potential for profitable operations."

# Add other agents similarly...
class MarketInsightsAgent:
    """Market & Commercial Insights Agent"""
    
    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        self._init_gemini()
    
    def _init_gemini(self):
        try:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.conversation = None
        except:
            self.model = None
            self.conversation = None
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process market insights queries"""
        
        # Get market data
        current_market = self._get_current_market_data()
        trend_analysis = self._analyze_market_trends()
        market_insights = self._generate_market_insights(trend_analysis, current_market)
        
        return {
            "response": self._get_ai_insight(query, trend_analysis, current_market, market_insights),
            "data": {
                "market_trends": trend_analysis,
                "current_market": current_market,
                "market_insights": market_insights
            },
            "suggestions": [
                "Monitor bunker price trends for optimal bunkering timing",
                "Consider market timing for chartering decisions",
                "Analyze supply-demand patterns for route selection"
            ]
        }
    
    def _get_current_market_data(self) -> Dict[str, Any]:
        """Get current market data snapshot"""
        latest_market = MARKET_TRENDS[-1]
        avg_bunker_price = sum(b['price_usd_per_ton'] for b in BUNKER_PRICES) / len(BUNKER_PRICES)
        
        return {
            "current_freight_rate": latest_market['Freight Rate (USD/TEU)'],
            "current_bunker_price": round(avg_bunker_price, 2),
            "demand_indicator": latest_market['Demand Indicator'],
            "year": latest_market['Year']
        }
    
    def _analyze_market_trends(self) -> Dict[str, Any]:
        """Analyze market trends"""
        if len(MARKET_TRENDS) < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        current = MARKET_TRENDS[-1]
        previous = MARKET_TRENDS[-2]
        
        freight_change = ((current['Freight Rate (USD/TEU)'] - previous['Freight Rate (USD/TEU)']) / previous['Freight Rate (USD/TEU)']) * 100
        bunker_change = ((current['Bunker Price (USD/ton)'] - previous['Bunker Price (USD/ton)']) / previous['Bunker Price (USD/ton)']) * 100
        
        return {
            "freight_rate_trend": {
                "trend": "Upward" if freight_change > 0 else "Downward",
                "change_percent": round(freight_change, 2)
            },
            "bunker_price_trend": {
                "trend": "Rising" if bunker_change > 0 else "Falling",
                "change_percent": round(bunker_change, 2)
            }
        }
    
    def _generate_market_insights(self, trend_analysis: Dict[str, Any], current_market: Dict[str, Any]) -> Dict[str, Any]:
        """Generate market insights"""
        insights = {
            "key_trends": [],
            "opportunities": [],
            "risk_factors": []
        }
        
        freight_trend = trend_analysis.get('freight_rate_trend', {})
        if freight_trend.get('trend') == 'Upward':
            insights["key_trends"].append("Freight rates showing positive momentum")
            insights["opportunities"].append("Favorable conditions for rate negotiations")
        
        bunker_trend = trend_analysis.get('bunker_price_trend', {})
        if bunker_trend.get('trend') == 'Rising':
            insights["key_trends"].append("Bunker prices on upward trend")
            insights["risk_factors"].append("Increasing operational costs")
        
        return insights
    
    def _get_ai_insight(self, query: str, trend_analysis: Dict[str, Any], current_market: Dict[str, Any], market_insights: Dict[str, Any]) -> str:
        """Get AI insight for market analysis"""
        if not self.model:
            return self._get_fallback_response(trend_analysis, current_market, market_insights)
        
        try:
            prompt = f"""
            You are Dr. James Mitchell, a senior maritime market analyst and economist with 22+ years of experience in maritime finance and market intelligence at IME Hub. You are providing strategic market insights for maritime executives and chartering managers.

            CRITICAL INSTRUCTIONS:
            - Provide expert-level maritime market analysis and strategic insights
            - Focus on commercial implications, risk assessment, and strategic opportunities
            - Use precise maritime finance and market terminology
            - Reference specific data points, trends, and percentages
            - Consider market timing and strategic decision-making

            MARKET ANALYSIS DATA:
            Query: {query}
            Current Market Conditions: {json.dumps(current_market, indent=2)}
            Trend Analysis: {json.dumps(trend_analysis, indent=2)}
            Strategic Insights: {json.dumps(market_insights, indent=2)}

            RESPONSE STRUCTURE:
            1. **Market Assessment**: Professional evaluation of current market conditions (2-3 sentences)
            2. **Trend Analysis**: Specific trend data with commercial implications (2-3 sentences)
            3. **Strategic Recommendations**: Actionable business insights and timing (2-3 sentences)
            4. **Risk Assessment**: Market risks and mitigation strategies (1-2 sentences)

            TONE: Professional market analyst, strategic focus, data-driven insights
            LENGTH: 4-6 sentences maximum
            DOMAIN: Maritime markets, freight rates, bunker prices, commercial strategy ONLY
            """
            
            if self.conversation is None:
                self.conversation = self.model.start_chat(history=[])
            
            response = self.conversation.send_message(prompt)
            return response.text
            
        except:
            return self._get_fallback_response(trend_analysis, current_market, market_insights)
    
    def _get_fallback_response(self, trend_analysis: Dict[str, Any], current_market: Dict[str, Any], market_insights: Dict[str, Any]) -> str:
        """Get fallback response"""
        freight_rate = current_market['current_freight_rate']
        bunker_price = current_market['current_bunker_price']
        
        return f"Current market analysis: Freight rates stand at ${freight_rate:,}/TEU with bunker prices at ${bunker_price}/ton. The market shows {trend_analysis.get('freight_rate_trend', {}).get('trend', 'stable')} freight rate trends and {trend_analysis.get('bunker_price_trend', {}).get('trend', 'stable')} bunker price movement. Key opportunities include {', '.join(market_insights.get('opportunities', ['market monitoring']))}."

# Example usage
if __name__ == "__main__":
    api_key = "AIzaSyCV7l4PzBVi5TtbYkJHvAcmp0XMhutCWBc"
    
    # Test Voyage Planning Agent
    voyage_agent = VoyagePlanningAgent(api_key)
    response = voyage_agent.process_query("What's the optimal route from Singapore to Rotterdam?")
    print("Voyage Planning Response:", response['response'][:100])
    
    # Test Cargo Matching Agent
    cargo_agent = CargoMatchingAgent(api_key)
    response = cargo_agent.process_query("What vessels can carry coal cargo?")
    print("Cargo Matching Response:", response['response'][:100])
    
    # Test Market Insights Agent
    market_agent = MarketInsightsAgent(api_key)
    response = market_agent.process_query("What are the current market trends?")
    print("Market Insights Response:", response['response'][:100]) 
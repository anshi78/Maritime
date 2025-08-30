#!/usr/bin/env python3
"""
IME Hub Maritime AI - Frontend General Captain Agent
Standalone file for Next.js frontend integration
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, List
import google.generativeai as genai

# Hardcoded CSV data
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

class FrontendGeneralCaptain:
    """Frontend General Captain Agent - Multi-domain maritime expertise and intelligent routing"""
    
    def __init__(self, gemini_api_key: str):
        """Initialize the General Captain Agent"""
        self.gemini_api_key = gemini_api_key
        self.conversation_context = {}
        self.conversation_history = []
        
        # Initialize Gemini AI
        try:
            genai.configure(api_key=gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.conversation = None
        except Exception as e:
            print(f"Warning: Gemini AI initialization failed: {e}")
            self.model = None
            self.conversation = None
    
    def process_query(self, user_query: str, user_id: str = None) -> Dict[str, Any]:
        """Process user query and provide intelligent maritime response"""
        
        # Extract context from query
        context = self._extract_context(user_query)
        
        # Update conversation context
        self._update_context(context, user_id)
        
        # Determine response type and generate answer
        response = self._generate_response(user_query, context)
        
        # Update conversation history
        self._update_history(user_query, response, user_id)
        
        return response
    
    def _extract_context(self, query: str) -> Dict[str, Any]:
        """Extract maritime context from user query"""
        context = {
            'ports': [],
            'vessels': [],
            'cargoes': [],
            'routes': [],
            'query_type': 'general'
        }
        
        # Extract ports
        for port_data in PORTS_DATA:
            if port_data['port'].lower() in query.lower():
                context['ports'].append(port_data['port'])
        
        # Extract vessels
        for vessel in VESSELS_DATA:
            if vessel['name'].lower() in query.lower():
                context['vessels'].append(vessel['name'])
        
        # Extract cargo types
        for cargo in CARGOS_DATA:
            if cargo['commodity'].lower() in query.lower():
                context['cargoes'].append(cargo['commodity'])
        
        # Extract routes
        if '-' in query:
            parts = query.split('-')
            if len(parts) >= 2:
                context['routes'].append(f"{parts[0].strip()}-{parts[1].strip()}")
        
        # Determine query type
        if any(word in query.lower() for word in ['route', 'voyage', 'journey', 'distance']):
            context['query_type'] = 'voyage_planning'
        elif any(word in query.lower() for word in ['cargo', 'vessel', 'matching', 'compatibility']):
            context['query_type'] = 'cargo_matching'
        elif any(word in query.lower() for word in ['market', 'trend', 'freight', 'bunker']):
            context['query_type'] = 'market_insights'
        elif any(word in query.lower() for word in ['port', 'bunker', 'facility']):
            context['query_type'] = 'port_intelligence'
        elif any(word in query.lower() for word in ['cost', 'pda', 'expense', 'budget']):
            context['query_type'] = 'cost_management'
        
        return context
    
    def _update_context(self, context: Dict[str, Any], user_id: str = None):
        """Update conversation context"""
        if user_id not in self.conversation_context:
            self.conversation_context[user_id] = {}
        
        # Update ports
        if context['ports']:
            if 'ports' not in self.conversation_context[user_id]:
                self.conversation_context[user_id]['ports'] = []
            self.conversation_context[user_id]['ports'].extend(context['ports'])
            self.conversation_context[user_id]['ports'] = list(set(self.conversation_context[user_id]['ports']))
        
        # Update vessels
        if context['vessels']:
            if 'vessels' not in self.conversation_context[user_id]:
                self.conversation_context[user_id]['vessels'] = []
            self.conversation_context[user_id]['vessels'].extend(context['vessels'])
            self.conversation_context[user_id]['vessels'] = list(set(self.conversation_context[user_id]['vessels']))
        
        # Update cargoes
        if context['cargoes']:
            if 'cargoes' not in self.conversation_context[user_id]:
                self.conversation_context[user_id]['cargoes'] = []
            self.conversation_context[user_id]['cargoes'].extend(context['cargoes'])
            self.conversation_context[user_id]['cargoes'] = list(set(self.conversation_context[user_id]['cargoes']))
    
    def _generate_response(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate intelligent maritime response"""
        
        # Get basic data response
        data_response = self._get_data_response(query, context)
        
        # Get AI-enhanced response
        ai_response = self._get_ai_response(query, context, data_response)
        
        # Generate routing recommendation
        routing_info = self._get_routing_recommendation(context)
        
        return {
            "response": ai_response,
            "data": data_response,
            "routing": routing_info,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "agent": "General Captain Agent"
        }
    
    def _get_data_response(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get basic data response based on query"""
        response = {}
        
        # Distance queries
        if 'distance' in query.lower() and len(context['ports']) >= 2:
            port1, port2 = context['ports'][0], context['ports'][1]
            distance = self._calculate_distance(port1, port2)
            response['distance'] = {
                "from": port1,
                "to": port2,
                "nautical_miles": distance,
                "kilometers": round(distance * 1.852, 1)
            }
        
        # Weather queries
        if 'weather' in query.lower() and context['ports']:
            port = context['ports'][-1]
            weather = self._get_weather(port)
            if weather:
                response['weather'] = weather
        
        # Bunker price queries
        if 'bunker' in query.lower() and context['ports']:
            port = context['ports'][-1]
            price = self._get_bunker_price(port)
            if price:
                response['bunker_price'] = {
                    "port": port,
                    "price_usd_per_ton": price
                }
        
        # Vessel queries
        if 'vessel' in query.lower():
            response['vessels'] = VESSELS_DATA
        
        # Cargo queries
        if 'cargo' in query.lower():
            response['cargoes'] = CARGOS_DATA
        
        return response
    
    def _get_ai_response(self, query: str, context: Dict[str, Any], data_response: Dict[str, Any]) -> str:
        """Get AI-enhanced response using Gemini"""
        if not self.model:
            return self._get_fallback_response(query, context, data_response)
        
        try:
            # Prepare prompt for Gemini
            prompt = self._create_ai_prompt(query, context, data_response)
            
            # Get AI response
            if self.conversation is None:
                self.conversation = self.model.start_chat(history=[])
            
            ai_response = self.conversation.send_message(prompt)
            return ai_response.text
            
        except Exception as e:
            return self._get_fallback_response(query, context, data_response)
    
    def _create_ai_prompt(self, query: str, context: Dict[str, Any], data_response: Dict[str, Any]) -> str:
        """Create AI prompt for Gemini"""
        
        context_summary = self._get_context_summary(context)
        
        prompt = f"""
        You are Captain Sarah Chen, a senior maritime consultant with 25+ years of experience at IME Hub, a leading maritime technology company. You are speaking to maritime professionals who expect expert-level insights.

        CRITICAL INSTRUCTIONS:
        - You are a maritime expert, not a general AI
        - Use precise maritime terminology and industry standards
        - Provide actionable, commercial insights
        - Always consider safety, efficiency, and profitability
        - Reference specific data points from the available information
        - Stay within maritime domain expertise only

        CURRENT CONVERSATION CONTEXT: {context_summary}
        
        USER QUERY: {query}
        
        AVAILABLE MARITIME DATA: {json.dumps(data_response, indent=2)}
        
        RESPONSE REQUIREMENTS:
        1. **Professional Maritime Analysis**: Provide expert-level maritime insights using industry terminology
        2. **Data-Driven Insights**: Reference specific numbers, distances, prices, and technical specifications
        3. **Commercial Recommendations**: Offer actionable business advice for maritime operations
        4. **Safety & Efficiency Focus**: Consider operational safety, fuel efficiency, and risk management
        5. **Industry Best Practices**: Apply current maritime standards and regulations
        6. **Structured Format**: Use clear sections with maritime headings

        RESPONSE STRUCTURE:
        - **Analysis**: Professional maritime assessment (2-3 sentences)
        - **Technical Details**: Specific data points and calculations (2-3 sentences)
        - **Commercial Insights**: Business implications and recommendations (2-3 sentences)
        - **Operational Considerations**: Safety, efficiency, and risk factors (1-2 sentences)

        TONE: Professional, authoritative, maritime-expert level
        LENGTH: 4-6 sentences maximum, concise but comprehensive
        DOMAIN: Maritime operations, shipping, logistics, and port operations ONLY
        """
        
        return prompt
    
    def _get_fallback_response(self, query: str, context: Dict[str, Any], data_response: Dict[str, Any]) -> str:
        """Get fallback response when AI is unavailable"""
        
        if data_response.get('distance'):
            dist = data_response['distance']
            return f"The distance between {dist['from']} and {dist['to']} is {dist['nautical_miles']} nautical miles ({dist['kilometers']} km). This route typically takes 18-25 days depending on vessel speed and weather conditions."
        
        elif data_response.get('weather'):
            weather = data_response['weather']
            return f"Current weather conditions at {weather['Port/Route']}: Sea State is {weather['Sea State']}, Wind is {weather['Wind']}, and Visibility is {weather['Visibility']}. These conditions are suitable for normal maritime operations."
        
        elif data_response.get('bunker_price'):
            bunker = data_response['bunker_price']
            return f"Bunker price at {bunker['port']} is currently ${bunker['price_usd_per_ton']}/ton. This represents a competitive rate for the region."
        
        elif data_response.get('vessels'):
            return f"There are {len(data_response['vessels'])} vessels currently available in our system, ranging from 76,000 to 100,000 DWT. Each vessel has specific capabilities and laycan windows for chartering."
        
        elif data_response.get('cargoes'):
            return f"We have {len(data_response['cargoes'])} cargo types available, including coal, iron ore, and grain. Each cargo has specific requirements and freight rates."
        
        else:
            return "I can help you with maritime queries including route planning, vessel information, cargo matching, market analysis, port intelligence, and cost management. Please provide more specific details about what you'd like to know."
    
    def _get_routing_recommendation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get recommendation for which specialized agent to use"""
        
        routing_map = {
            'voyage_planning': {
                'agent': 'Voyage Planning & Optimization',
                'description': 'Route optimization, weather analysis, piracy risk assessment',
                'page': '/voyage-planning'
            },
            'cargo_matching': {
                'agent': 'Cargo & Tonnage Matching',
                'description': 'Cargo-vessel compatibility and profitability analysis',
                'page': '/cargo-matching'
            },
            'market_insights': {
                'agent': 'Market & Commercial Insights',
                'description': 'Market trends, benchmarking, and strategic analysis',
                'page': '/market-insights'
            },
            'port_intelligence': {
                'agent': 'Port & Cargo Intelligence',
                'description': 'Port optimization and bunker analysis',
                'page': '/port-intelligence'
            },
            'cost_management': {
                'agent': 'PDA & Cost Management',
                'description': 'Cost estimation and variance tracking',
                'page': '/cost-management'
            }
        }
        
        if context['query_type'] in routing_map:
            return routing_map[context['query_type']]
        else:
            return {
                'agent': 'General Captain',
                'description': 'Multi-domain maritime expertise',
                'page': '/general'
            }
    
    def _calculate_distance(self, port1: str, port2: str) -> float:
        """Calculate distance between two ports"""
        try:
            port1_data = next((p for p in PORTS_DATA if p['port'] == port1), None)
            port2_data = next((p for p in PORTS_DATA if p['port'] == port2), None)
            
            if port1_data and port2_data:
                # Simple distance calculation (in real system, use proper geodesic)
                lat1, lon1 = port1_data['lat'], port1_data['lon']
                lat2, lon2 = port2_data['lat'], port2_data['lon']
                
                # Approximate distance calculation
                distance = ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5 * 60  # Convert to nautical miles
                return round(distance, 0)
        except:
            pass
        
        return 0
    
    def _get_weather(self, port: str) -> Dict[str, Any]:
        """Get weather for a specific port"""
        return next((w for w in WEATHER_DATA if w['Port/Route'] == port), None)
    
    def _get_bunker_price(self, port: str) -> float:
        """Get bunker price for a specific port"""
        bunker = next((b for b in BUNKER_PRICES if b['port'] == port), None)
        return bunker['price_usd_per_ton'] if bunker else None
    
    def _get_context_summary(self, context: Dict[str, Any]) -> str:
        """Get summary of current context"""
        summary_parts = []
        
        if context.get('ports'):
            summary_parts.append(f"Ports mentioned: {', '.join(context['ports'])}")
        
        if context.get('vessels'):
            summary_parts.append(f"Vessels mentioned: {', '.join(context['vessels'])}")
        
        if context.get('cargoes'):
            summary_parts.append(f"Cargo types mentioned: {', '.join(context['cargoes'])}")
        
        if context.get('routes'):
            summary_parts.append(f"Routes discussed: {', '.join(context['routes'])}")
        
        if summary_parts:
            return " | ".join(summary_parts)
        else:
            return "No specific context established yet"
    
    def _update_history(self, query: str, response: Dict[str, Any], user_id: str = None):
        """Update conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response,
            'context': response.get('context', {})
        })
        
        # Keep only last 10 conversations
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id].pop(0)
    
    def get_conversation_history(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Get conversation history for a user"""
        return self.conversation_history.get(user_id, [])
    
    def clear_context(self, user_id: str = None):
        """Clear conversation context for a user"""
        if user_id in self.conversation_context:
            del self.conversation_context[user_id]
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]

# Example usage
if __name__ == "__main__":
    # Initialize with your Gemini API key
    api_key = "AIzaSyCV7l4PzBVi5TtbYkJHvAcmp0XMhutCWBc"
    captain = FrontendGeneralCaptain(api_key)
    
    # Test queries
    test_queries = [
        "What's the distance between Singapore and Rotterdam?",
        "What's the weather like at Singapore?",
        "What vessels are available?",
        "What are the bunker prices?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        response = captain.process_query(query)
        print(f"Response: {response['response'][:100]}...")
        print(f"Routing: {response['routing']['agent']}")
        print(f"Page: {response['routing']['page']}") 
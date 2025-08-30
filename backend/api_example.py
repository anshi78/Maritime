#!/usr/bin/env python3
"""
IME Maritime AI - API Integration Example for Next.js
Shows how to integrate the agents with your frontend
"""

from frontend_general_captain import FrontendGeneralCaptain
from frontend_specialist_agents import VoyagePlanningAgent, CargoMatchingAgent, MarketInsightsAgent

# Example Next.js API route integration
class IMEAPI:
    """API wrapper for IME Maritime AI agents"""
    
    def __init__(self, gemini_api_key: str):
        """Initialize all agents"""
        self.general_captain = FrontendGeneralCaptain(gemini_api_key)
        self.voyage_planning = VoyagePlanningAgent(gemini_api_key)
        self.cargo_matching = CargoMatchingAgent(gemini_api_key)
        self.market_insights = MarketInsightsAgent(gemini_api_key)
    
    def process_general_query(self, query: str, user_id: str = None) -> Dict[str, Any]:
        """Process query with General Captain Agent"""
        return self.general_captain.process_query(query, user_id)
    
    def process_voyage_query(self, query: str) -> Dict[str, Any]:
        """Process query with Voyage Planning Agent"""
        return self.voyage_planning.process_query(query)
    
    def process_cargo_query(self, query: str) -> Dict[str, Any]:
        """Process query with Cargo Matching Agent"""
        return self.cargo_matching.process_query(query)
    
    def process_market_query(self, query: str) -> Dict[str, Any]:
        """Process query with Market Insights Agent"""
        return self.market_insights.process_query(query)
    
    def get_agent_recommendation(self, query: str) -> Dict[str, Any]:
        """Get recommendation for which agent to use"""
        # Use General Captain to determine routing
        response = self.general_captain.process_query(query)
        return response.get('routing', {})

# Example Next.js API route (pages/api/maritime-ai.js)
"""
// Next.js API route example
import { IMEAPI } from '../../../api_example.py';

const imeAPI = new IMEAPI(process.env.GEMINI_API_KEY);

export default async function handler(req, res) {
    if (req.method !== 'POST') {
        return res.status(405).json({ message: 'Method not allowed' });
    }
    
    try {
        const { query, agent, user_id } = req.body;
        
        let response;
        
        switch (agent) {
            case 'general':
                response = imeAPI.process_general_query(query, user_id);
                break;
            case 'voyage':
                response = imeAPI.process_voyage_query(query);
                break;
            case 'cargo':
                response = imeAPI.process_cargo_query(query);
                break;
            case 'market':
                response = imeAPI.process_market_query(query);
                break;
            default:
                // Auto-detect which agent to use
                routing = imeAPI.get_agent_recommendation(query);
                response = imeAPI.process_general_query(query, user_id);
                response.routing = routing;
        }
        
        res.status(200).json(response);
        
    } catch (error) {
        res.status(500).json({ 
            error: 'Internal server error', 
            message: error.message 
        });
    }
}
"""

# Example usage
if __name__ == "__main__":
    api_key = "AIzaSyCV7l4PzBVi5TtbYkJHvAcmp0XMhutCWBc"
    api = IMEAPI(api_key)
    
    # Test general query
    print("=== Testing General Captain Agent ===")
    response = api.process_general_query("What's the distance between Singapore and Rotterdam?")
    print(f"Response: {response['response'][:100]}...")
    print(f"Routing: {response['routing']['agent']}")
    print(f"Page: {response['routing']['page']}")
    
    # Test voyage planning
    print("\n=== Testing Voyage Planning Agent ===")
    response = api.process_voyage_query("What's the optimal route from Singapore to Rotterdam?")
    print(f"Response: {response['response'][:100]}...")
    
    # Test cargo matching
    print("\n=== Testing Cargo Matching Agent ===")
    response = api.process_cargo_query("What vessels can carry coal cargo?")
    print(f"Response: {response['response'][:100]}...")
    
    # Test market insights
    print("\n=== Testing Market Insights Agent ===")
    response = api.process_market_query("What are the current market trends?")
    print(f"Response: {response['response'][:100]}...") 
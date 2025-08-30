#!/usr/bin/env python3
"""
Specialist Agents API Script for Next.js
Handles queries for specific maritime domains
"""

import sys
import json
import os

# Add the parent directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend_specialist_agents import (
    VoyagePlanningAgent, 
    CargoMatchingAgent, 
    MarketInsightsAgent
)

def main():
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Query and agent_type required"}))
        return
    
    query = sys.argv[1]
    agent_type = sys.argv[2]
    
    try:
        # Initialize with your Gemini API key
        api_key = "AIzaSyCV7l4PzBVi5TtbYkJHvAcmp0XMhutCWBc"
        
        # Select agent based on type
        if agent_type == 'voyage':
            agent = VoyagePlanningAgent(api_key)
        elif agent_type == 'cargo':
            agent = CargoMatchingAgent(api_key)
        elif agent_type == 'market':
            agent = MarketInsightsAgent(api_key)
        else:
            print(json.dumps({"error": f"Invalid agent type: {agent_type}"}))
            return
        
        # Process query
        response = agent.process_query(query)
        
        # Return JSON response
        print(json.dumps(response))
        
    except Exception as e:
        print(json.dumps({"error": str(e), "type": "python_error"}))

if __name__ == "__main__":
    main() 
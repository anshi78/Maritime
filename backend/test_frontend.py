#!/usr/bin/env python3
"""
Test script for frontend integration files
"""

def test_imports():
    """Test if all frontend files can be imported"""
    try:
        print("Testing imports...")
        
        # Test General Captain
        from frontend_general_captain import FrontendGeneralCaptain
        print("✅ FrontendGeneralCaptain imported successfully")
        
        # Test Specialist Agents
        from frontend_specialist_agents import VoyagePlanningAgent, CargoMatchingAgent, MarketInsightsAgent
        print("✅ Specialist agents imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_general_captain():
    """Test General Captain Agent"""
    try:
        from frontend_general_captain import FrontendGeneralCaptain
        
        api_key = "AIzaSyCV7l4PzBVi5TtbYkJHvAcmp0XMhutCWBc"
        captain = FrontendGeneralCaptain(api_key)
        
        # Test basic query
        response = captain.process_query("What's the distance between Singapore and Rotterdam?")
        
        print("✅ General Captain test successful")
        print(f"   Response length: {len(response.get('response', ''))}")
        print(f"   Data keys: {list(response.get('data', {}).keys())}")
        print(f"   Routing: {response.get('routing', {}).get('agent', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ General Captain test failed: {e}")
        return False

def test_specialist_agents():
    """Test Specialist Agents"""
    try:
        from frontend_specialist_agents import VoyagePlanningAgent, CargoMatchingAgent, MarketInsightsAgent
        
        api_key = "AIzaSyCV7l4PzBVi5TtbYkJHvAcmp0XMhutCWBc"
        
        # Test Voyage Planning
        voyage_agent = VoyagePlanningAgent(api_key)
        response = voyage_agent.process_query("What's the optimal route from Singapore to Rotterdam?")
        print("✅ Voyage Planning Agent test successful")
        
        # Test Cargo Matching
        cargo_agent = CargoMatchingAgent(api_key)
        response = cargo_agent.process_query("What vessels can carry coal cargo?")
        print("✅ Cargo Matching Agent test successful")
        
        # Test Market Insights
        market_agent = MarketInsightsAgent(api_key)
        response = market_agent.process_query("What are the current market trends?")
        print("✅ Market Insights Agent test successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Specialist agents test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing IME Maritime AI Frontend Integration")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("❌ Import tests failed. Exiting.")
        exit(1)
    
    print("\n" + "=" * 50)
    
    # Test General Captain
    if not test_general_captain():
        print("❌ General Captain tests failed.")
    
    print("\n" + "=" * 50)
    
    # Test Specialist Agents
    if not test_specialist_agents():
        print("❌ Specialist agent tests failed.")
    
    print("\n" + "=" * 50)
    print("🎉 Frontend integration testing completed!")
    print("\nYour files are ready for Next.js integration!") 
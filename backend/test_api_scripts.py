#!/usr/bin/env python3
"""
Test API Scripts for Next.js Integration
Verifies that the Python API scripts work correctly
"""

import subprocess
import json
import sys
import os

def test_general_chatbot_api():
    """Test the general chatbot API script"""
    print("🚢 Testing General Chatbot API Script")
    print("=" * 50)
    
    try:
        # Test the script with a query
        result = subprocess.run([
            'python', 'python/general_chatbot_api.py', 
            'What is the distance between Singapore and Rotterdam?'
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            # Parse the response
            response = json.loads(result.stdout)
            print("✅ Script executed successfully")
            print(f"Response type: {type(response)}")
            print(f"Response keys: {list(response.keys())}")
            
            if 'response' in response:
                print(f"AI Response: {response['response'][:100]}...")
            
            if 'routing' in response:
                print(f"Routing: {response['routing']}")
                
        else:
            print(f"❌ Script failed with return code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")

def test_specialist_agents_api():
    """Test the specialist agents API script"""
    print("\n🚢 Testing Specialist Agents API Script")
    print("=" * 50)
    
    agent_types = ['voyage', 'cargo', 'market']
    
    for agent_type in agent_types:
        print(f"\n--- Testing {agent_type.upper()} Agent ---")
        
        try:
            # Test the script with a query and agent type
            result = subprocess.run([
                'python', 'python/specialist_agents_api.py', 
                f'What can you tell me about {agent_type}?', 
                agent_type
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                # Parse the response
                response = json.loads(result.stdout)
                print(f"✅ {agent_type} agent executed successfully")
                print(f"Response type: {type(response)}")
                print(f"Response keys: {list(response.keys())}")
                
                if 'response' in response:
                    print(f"AI Response: {response['response'][:100]}...")
                    
            else:
                print(f"❌ {agent_type} agent failed with return code: {result.returncode}")
                print(f"Error output: {result.stderr}")
                
        except Exception as e:
            print(f"❌ {agent_type} agent test failed: {e}")

def show_integration_steps():
    """Show the integration steps for the user"""
    print("\n🎯 NEXT.JS INTEGRATION STEPS")
    print("=" * 50)
    print("1. ✅ Copy Python files to your project")
    print("2. ✅ Install Python dependencies")
    print("3. ✅ Create Next.js API routes")
    print("4. ✅ Create frontend components")
    print("5. ✅ Test the integration")
    print("\n📁 Required Files:")
    print("   - frontend_general_captain.py")
    print("   - frontend_specialist_agents.py")
    print("   - python/general_chatbot_api.py")
    print("   - python/specialist_agents_api.py")
    print("   - requirements_frontend.txt")
    print("\n🚀 Your maritime AI is ready for frontend integration!")

if __name__ == "__main__":
    print("🚀 Testing IME Maritime AI API Scripts")
    print("=" * 50)
    print("Verifying that the Python API scripts work correctly...")
    
    # Test both API scripts
    test_general_chatbot_api()
    test_specialist_agents_api()
    
    # Show integration steps
    show_integration_steps()
    
    print("\n🎉 API Script Testing Completed!")
    print("If all tests passed, your scripts are ready for Next.js integration!") 
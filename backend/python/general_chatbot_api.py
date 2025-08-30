#!/usr/bin/env python3
"""
General Chatbot API Script for Next.js
Handles all general maritime queries and routes to specialists
"""

import sys
import json
import os

# Add the parent directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend_general_captain import FrontendGeneralCaptain

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Query required"}))
        return
    
    query = sys.argv[1]
    user_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Initialize with your Gemini API key
        api_key = "AIzaSyCV7l4PzBVi5TtbYkJHvAcmp0XMhutCWBc"
        captain = FrontendGeneralCaptain(api_key)
        
        # Process query
        response = captain.process_query(query, user_id)
        
        # Return JSON response
        print(json.dumps(response))
        
    except Exception as e:
        print(json.dumps({"error": str(e), "type": "python_error"}))

if __name__ == "__main__":
    main() 
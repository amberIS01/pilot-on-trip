"""
AI Assistant Demonstration Script
This script shows how the basic chatbot works for evaluation purposes
"""

import requests
import json
import time

# API Base URL - Update this if running on different port
BASE_URL = "http://localhost:8000"

def print_separator():
    print("\n" + "="*60 + "\n")

def print_response(response_data):
    """Pretty print the chatbot response"""
    print(f"Bot: {response_data['response']}")
    print(f"Case ID: {response_data['case_id']}")
    print(f"User Type: {response_data['user_type']}")
    print(f"Query Type: {response_data['query_type']}")
    print(f"Status: {response_data['conversation_status']}")
    if response_data.get('suggestions'):
        print(f"Suggestions: {', '.join(response_data['suggestions'])}")

def scenario_1_new_user_booking():
    """Scenario 1: New user wants to book a ride"""
    print("SCENARIO 1: New User Booking")
    print_separator()
    
    # First message from new user
    print("User: Hi, I want to book a ride")
    response = requests.post(f"{BASE_URL}/chat/", 
        json={"message": "Hi, I want to book a ride"})
    data = response.json()
    print_response(data)
    case_id = data['case_id']
    
    time.sleep(2)
    print_separator()
    
    # User provides name
    print("User: My name is John")
    response = requests.post(f"{BASE_URL}/chat/", 
        json={"message": "My name is John", "case_id": case_id})
    print_response(response.json())
    
    time.sleep(2)
    print_separator()
    
    # User provides phone
    print("User: My phone is 9876543210")
    response = requests.post(f"{BASE_URL}/chat/", 
        json={"message": "My phone is 9876543210", "case_id": case_id})
    print_response(response.json())
    
    return case_id

def scenario_2_support_query():
    """Scenario 2: User has a support issue"""
    print_separator()
    print("SCENARIO 2: Support Query")
    print_separator()
    
    print("User: I have a problem with my last booking")
    response = requests.post(f"{BASE_URL}/chat/", 
        json={"message": "I have a problem with my last booking"})
    data = response.json()
    print_response(data)
    
    time.sleep(2)
    print_separator()
    
    # Follow up
    print("User: The driver was late and charged extra")
    response = requests.post(f"{BASE_URL}/chat/", 
        json={"message": "The driver was late and charged extra", "case_id": data['case_id']})
    print_response(response.json())
    
    return data['case_id']

def scenario_3_existing_user():
    """Scenario 3: Existing user returns with email"""
    print_separator()
    print("SCENARIO 3: Existing User Detection")
    print_separator()
    
    print("User: Hi, my email is john@example.com")
    response = requests.post(f"{BASE_URL}/chat/", 
        json={
            "message": "Hi, my email is john@example.com",
            "email": "john@example.com"
        })
    data = response.json()
    print_response(data)
    
    time.sleep(2)
    print_separator()
    
    # Ask about pricing
    print("User: What are your rates?")
    response = requests.post(f"{BASE_URL}/chat/", 
        json={"message": "What are your rates?", "case_id": data['case_id']})
    print_response(response.json())
    
    return data['case_id']

def scenario_4_view_history(case_id):
    """Scenario 4: View conversation history"""
    print_separator()
    print("SCENARIO 4: View Conversation History")
    print_separator()
    
    print(f"Fetching history for case: {case_id}")
    response = requests.get(f"{BASE_URL}/chat/{case_id}/history")
    history = response.json()
    
    print(f"\nCreated: {history['created_at']}")
    print(f"Updated: {history['updated_at']}")
    print(f"User Type: {history['user_type']}")
    print(f"Query Type: {history['query_type']}")
    print(f"Status: {history['status']}")
    print("\nConversation Log:")
    print(history['conversation'])

def scenario_5_close_case(case_id):
    """Scenario 5: Close a conversation"""
    print_separator()
    print("SCENARIO 5: Close Conversation")
    print_separator()
    
    print(f"[OK] Closing case: {case_id}")
    response = requests.put(f"{BASE_URL}/chat/{case_id}/close")
    print(response.json()['message'])

def main():
    """Run all demonstration scenarios"""
    print("\n" + "="*60)
    print("   AI ASSISTANT DEMONSTRATION FOR EVALUATION")
    print("="*60)
    print("\nMake sure the FastAPI server is running:")
    print("./env/Scripts/python -m uvicorn main:app --reload")
    print("="*60)
    
    # Removed input to allow automated testing
    print("\nStarting the demonstration...")
    
    try:
        # Run scenarios
        case1 = scenario_1_new_user_booking()
        case2 = scenario_2_support_query()
        case3 = scenario_3_existing_user()
        
        # View history and close cases
        scenario_4_view_history(case1)
        scenario_5_close_case(case1)
        
        print_separator()
        print("[OK] DEMONSTRATION COMPLETE!")
        print("\nKey Features Demonstrated:")
        print("1. [OK] Automatic Case ID generation")
        print("2. [OK] Query type detection (booking, support, pricing)")
        print("3. [OK] New vs Existing user identification")
        print("4. [OK] Conversation tracking and history")
        print("5. [OK] Context-aware responses")
        print("6. [OK] Suggestion prompts")
        print("7. [OK] Case status management")
        
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] ERROR: Cannot connect to the API")
        print("Please make sure the FastAPI server is running:")
        print("./env/Scripts/python -m uvicorn main:app --reload")
    except Exception as e:
        print(f"\n[ERROR] ERROR: {e}")

if __name__ == "__main__":
    main()
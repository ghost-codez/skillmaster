"""
Test script for SkillMaster API
Run this to verify the API is working correctly
"""

import requests
import json
import sys

API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server. Is it running?")
        print("   Start it with: python api_server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_skill_analysis():
    """Test the skill analysis endpoint"""
    print("\n🔍 Testing skill analysis endpoint...")
    
    test_data = {
        "skill_name": "Python Programming",
        "proficiency_level": "Beginner"
    }
    
    print(f"   Analyzing: {test_data['skill_name']} ({test_data['proficiency_level']})")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Analysis successful!")
            print(f"\n📊 Results:")
            print(f"   Skill: {data['skill_name']}")
            print(f"   Level: {data['proficiency_level']}")
            print(f"   Distinctions: {len(data['distinctions'])}")
            print(f"   Insights: {len(data['insights'])}")
            print(f"   Next Steps: {len(data['next_steps'])}")
            print(f"   Sources: {len(data['sources'])}")
            print(f"   Related Questions: {len(data['related_questions'])}")
            
            print(f"\n🔍 Sample Distinction:")
            if data['distinctions']:
                dist = data['distinctions'][0]
                print(f"   Name: {dist['name']}")
                print(f"   Description: {dist['description'][:80]}...")
            
            print(f"\n💡 Sample Insight:")
            if data['insights']:
                print(f"   {data['insights'][0][:80]}...")
            
            # Save full response
            with open('test_api_response.json', 'w') as f:
                json.dump(data, f, indent=2)
            print(f"\n💾 Full response saved to: test_api_response.json")
            
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            try:
                error = response.json()
                print(f"   Error: {error.get('detail', 'Unknown error')}")
            except:
                print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("SkillMaster API Test Suite")
    print("=" * 60)
    
    # Test 1: Health check
    health_ok = test_health_check()
    if not health_ok:
        print("\n⚠️  API server is not running or not accessible")
        print("   Please start it with: python api_server.py")
        sys.exit(1)
    
    # Test 2: Skill analysis
    analysis_ok = test_skill_analysis()
    
    print("\n" + "=" * 60)
    if health_ok and analysis_ok:
        print("✅ All tests passed!")
        print("\n🎉 Your API is working correctly!")
        print("\n📝 Next steps:")
        print("   1. Open skillmaster-demo.html in your browser")
        print("   2. Toggle 'Live API' in the top-right corner")
        print("   3. Try analyzing a skill!")
    else:
        print("❌ Some tests failed")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure .env file exists with OPENAI_API_KEY")
        print("   2. Check that the API server is running")
        print("   3. Verify your OpenAI API key is valid")
    print("=" * 60)

if __name__ == "__main__":
    main()


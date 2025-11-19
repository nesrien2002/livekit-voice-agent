import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def test_gemini_models():
    try:
        # Configure Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        # Try different models in order of preference
        models_to_try = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'gemini-pro',
            'gemini-2.0-flash-exp'
        ]

        for model_name in models_to_try:
            try:
                print(f"\nTrying model: {model_name}...")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say hello in 5 words")

                print(f"✅ SUCCESS with {model_name}!")
                print(f"Response: {response.text}")

                # Test with context
                print(f"\nTesting {model_name} with RAG context...")
                context = "Business hours: Monday-Friday, 9 AM to 6 PM EST"
                prompt = f"Context: {context}\n\nQuestion: When are you open?\n\nAnswer:"
                response2 = model.generate_content(prompt)
                print(f"Context response: {response2.text}")

                print(f"\n✅ Use this model in your voice agent: {model_name}")
                return model_name

            except Exception as e:
                print(f"❌ {model_name} failed: {str(e)[:100]}")
                continue

        print("\n❌ All models failed. You may need to:")
        print("1. Wait for quota to reset")
        print("2. Check your API key at https://aistudio.google.com/apikey")
        print("3. Verify billing is enabled if needed")
        return None

    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return None


if __name__ == "__main__":
    working_model = test_gemini_models()
    if working_model:
        print(f"\n🎯 RECOMMENDATION: Update your voice_agent.py to use: {working_model}")
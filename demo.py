"""
Demo Script - LiveKit Voice Agent with Gemini and RAG

This script demonstrates the core functionality of the voice agent,
showing how RAG retrieval and Gemini generation work together.
"""

import asyncio
from voice_agent import VoiceAgent
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)


async def demo():
    """Run demo of the voice agent"""

    print("=" * 70)
    print("🎤 LIVEKIT VOICE AGENT DEMO")
    print("=" * 70)
    print()

    # Initialize agent
    print("📦 Initializing Voice Agent...")
    agent = VoiceAgent()
    print()

    # Test questions
    test_questions = [
        {
            "question": "What are your business hours?",
            "description": "Testing RAG retrieval with exact match"
        },
        {
            "question": "How much does it cost?",
            "description": "Testing semantic search for pricing"
        },
        {
            "question": "Tell me about your company",
            "description": "Testing general information retrieval"
        },
        {
            "question": "Do you support multiple languages?",
            "description": "Testing specific feature question"
        },
        {
            "question": "What's the difference between plans?",
            "description": "Testing comparison understanding"
        }
    ]

    for i, test in enumerate(test_questions, 1):
        print("=" * 70)
        print(f"TEST {i}/{len(test_questions)}: {test['description']}")
        print("=" * 70)
        print()
        print(f"❓ Question: {test['question']}")
        print()

        # Process query
        response = await agent.process_user_input(test['question'])

        print()
        print(f"💬 Response:")
        print(f"   {response}")
        print()

        # Show if RAG was used
        history = agent.get_conversation_history()
        if history:
            last_entry = history[-1]
            if last_entry.get('used_rag'):
                print("   ✅ Used knowledge base context")
            else:
                print("   ℹ️  Used general knowledge")

        print()
        input("Press Enter to continue...")
        print()

    print("=" * 70)
    print("🎯 DEMO COMPLETE")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  Total questions processed: {len(test_questions)}")
    print(f"  Knowledge base documents: {len(agent.rag.documents)}")
    print(f"  Model used: Gemini 2.5 Flash")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
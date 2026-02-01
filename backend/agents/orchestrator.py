from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from backend.tools.kirana_tools import update_udhaar, check_inventory

# 1. Initialize Gemini Pro (Free & Fast)
llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

# 2. Tools
tools = [update_udhaar, check_inventory]

# 3. System Prompt
system_message = """
You are the Bharat Biz-Agent, an AI co-pilot for Indian Kirana stores.
1. You understand Hinglish perfectly (e.g., 'Rahul ka 500 chada do').
2. For any financial transaction (Udhaar), ALWAYS ask for confirmation: 'Confirming: Add ₹X to Y's account?'.
3. Do not execute the tool until the user says 'Yes' or 'Haan' or 'Theek hai'.
"""

# 4. Create Agent
agent_executor = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_message
)
from google.adk.agents import Agent
from google.genai import types
from csp_agent.help_agents import *

root_agent = Agent(
    name="csp_agent",
    model="gemini-2.0-flash",
    description="Routes customer queries to appropriate sub-agents.",
    instruction=(
        "You are a smart router agent responsible for directing customer queries.\n"
        "- If the user message is a greeting (e.g., 'hi', 'hello'), a thank you, or a farewell (e.g., 'bye'), forward it to 'faq_agent'.\n"
        "- If the message is a question related to general support, company policies, product FAQs, or help, forward it to 'faq_agent'.\n"
        "- If the message is unclear or general, still forward it to 'faq_agent'. Do not attempt to clarify first.\n"
        "Only route to sub-agents when their specialty is clearly needed. Do not generate answers yourself unless explicitly required."
    ),
    sub_agents=[faq_agent],
    generate_content_config=types.GenerateContentConfig(temperature=0.6),
)

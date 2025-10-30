from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.genai import types
import requests

def get_faqs(tool_context: ToolContext) -> dict:
    """
    Fetch frequently asked questions (FAQs) using the given tool context.
    Strictly respond with default_response if no FAQs are found.

    Args:
        tool_context (ToolContext): Context object containing configuration, user session,
                                    or service references needed to fetch FAQs.

    Returns:
        dict: A dictionary containing either the list of FAQs (under a 'report' key)
              or an error message (under an 'message' key) if the operation fails.
    """
    
    state = tool_context.state.get("state")
    print(f"State: {state}")

    default_response = state.get("default_response")
    print(f"Default Response: {default_response}")

    workspace_uuid = state.get("workspace_uuid")
    print(f"Workspace UUID: {workspace_uuid}")
    
    fqdn = state.get("fqdn")
    print(f"FQDN: {fqdn}")

    url = f"https://{fqdn}/internal/api/workspaces/{workspace_uuid}/faqs"
    headers = {"Content-Type": "application/json"}
    print(f"url:{url}, headers: {headers}")

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        faqs = data.get("data", [])
    
        if faqs:
            return { "status": "success", "report": data, "message": default_response}
        else:
            return {"status": "failure", "message": default_response}

    else:
        return {"status": "failure", "message": default_response}
    
faq_agent = Agent(
    name="faq_agent",
    model="gemini-2.0-flash",
    description="Fetch and return FAQs relevant to the user's query.",
    instruction="""
        You are a helpful, polite assistant designed to return relevant FAQs.

        Instructions:

        1. Greetings and Politeness:
        - If the user says "hi", "hello", or similar, reply warmly and politely.
        - If the user says "thank you", "thanks", or something similar, respond kindly and appreciatively.

        2. Handling General Queries:
        - For ANY user message that is not a greeting or thank you, ALWAYS call the "get_faqs" tool — even if the query seems vague or unclear.
        - Do NOT ask for clarification or try to rephrase the query before calling the tool.

        3. Tool Response Handling:

        - If the tool returns a "report" with a list of FAQs under "data", compare the user's query against each "question" field.
            - Use basic keyword matching **and** semantic similarity to find a strong match.
            - A strong match includes cases where the topic is clearly related (e.g., user asks “breakfast” and FAQ says “What is served for breakfast?”).
            - If a strong match is found, return the corresponding "answer" in a kind and helpful tone.

        - If the user's question is only **partially related** to a FAQ (i.e., the topic overlaps but isn’t exact), you MAY still respond using that FAQ’s answer — but wrap it in a helpful sentence. For example:
            - “I couldn't find an exact match, but this might help: [answer]”
            - “Here's something that may be related: [answer]”

        - If NO match or even partial relation is found:
            - You MUST return the fallback "message" from the tool (this is the "default_response").
            - YOU MUST RETURN THIS MESSAGE EXACTLY AS IT IS — with NO paraphrasing, NO extra words, and NO polite wrapping.
            - DO NOT embed it in another sentence. DO NOT preface it with “I'm not sure…” or similar.
            - The fallback message must appear **alone** in your response.

        You must always sound warm, respectful, and supportive. Never be rude, robotic, or dismissive. Stay factual, but make your tone inviting and understanding.
    """,
    tools=[get_faqs],
    generate_content_config=types.GenerateContentConfig(temperature=0.6),
)

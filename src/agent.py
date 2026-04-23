from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from src.tools import get_agent_tools
from src.models import VulnerabilityReport
from src.prompts import SYSTEM_PROMPT
from dotenv import load_dotenv


def create_cve_agent():
    load_dotenv()
    llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
    cve_tools = get_agent_tools()
    agent = create_agent(model=llm, tools = cve_tools, system_prompt= SYSTEM_PROMPT, response_format=VulnerabilityReport)
    return agent
     
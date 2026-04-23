from src.agent import create_cve_agent
from src.prompts import build_report_prompt


def _extract_text_content(content) -> str:
    """Normalize LangChain/OpenAI message content into readable text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
            else:
                parts.append(str(item))
        return "\n".join(part for part in parts if part)
    return str(content)


def main():
    print("=== AI Network Vulnerability Analyzer ===")
    
    # 1. Collect the network device details from the user
    user_make = input("Enter device make (e.g., Cisco): ")
    user_model = input("Enter device model (e.g., Catalyst 9300): ")
    user_os = input("Enter OS version (e.g., IOS-XE 17.3.2): ")
    
    print("\n[System] Initializing AI Agent...")
    
    # 2. Instantiate the agent using the function from your agent.py
    agent_executor = create_cve_agent()
    
    print("[System] Researching CVEs on the web... (This may take 10-20 seconds)\n")
    
    try:
        
        user_prompt = build_report_prompt(device_make= user_make, device_model= user_model, os_version= user_os) # Build the user prompt (device_make: str, device_model: str, os_version:)

        
        response = agent_executor.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ]
            }
        )

        print("\n=== FINAL VULNERABILITY REPORT ===")
        report_data = response.get("structured_response")
        if report_data is None:
            messages = response.get("messages", [])
            last_message = messages[-1] if messages else None
            last_content = (
                _extract_text_content(getattr(last_message, "content", ""))
                if last_message is not None
                else "No final model message was returned."
            )
            raise ValueError(
                "The agent returned a normal chat response instead of structured output. "
                f"Final model message: {last_content}"
            )
        print(report_data.model_dump_json(indent=4))

    except Exception as e:
        print(f"\n[Error] The agent encountered a problem: {e}")


if __name__ == "__main__":
    main()

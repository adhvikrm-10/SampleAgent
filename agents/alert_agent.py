from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.notification_tools import send_alert

alert_tool = FunctionTool(func=send_alert)

alert_agent = Agent(
    name="alert_agent",
    model="gemini-2.0-flash-exp",
    description="Agent for managing multi-channel alert notifications based on issue severity.",
    instruction="Assess urgency, choose alert channels, and send notifications.",
    tools=[alert_tool]
)

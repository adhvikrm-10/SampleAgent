import asyncio
import logging
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.diagnostic_agent import diagnostic_agent
from agents.anomaly_detection_agent import anomaly_detection_agent
from agents.recommendation_agent import recommendation_agent
from agents.alert_agent import alert_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

root_agent = Agent(
    name="root_orchestrator",
    model="gemini-2.0-flash-exp",
    description="Main orchestrator agent for IoT Device Health Monitoring system.",
    instruction="You coordinate sub-agents for diagnostics, anomaly detection, recommendations, and alerts.",
    sub_agents=[
        diagnostic_agent,
        anomaly_detection_agent,
        recommendation_agent,
        alert_agent
    ]
)

class IoTHealthMonitor:
    def __init__(self):
        self.session_service = InMemorySessionService()
        self.runner = Runner(agent=root_agent, app_name="iot_health_monitor", session_service=self.session_service)
        self.current_session_id = None

    async def initialize_session(self, user_id: str, session_id: str):
        await self.session_service.create_session(app_name="iot_health_monitor", user_id=user_id, session_id=session_id)
        self.current_session_id = session_id

    async def query(self, user_id: str, session_id: str, message: str) -> str:
        content = types.Content(role='user', parts=[types.Part(text=message)])
        response = ""
        events = self.runner.run(user_id=user_id, session_id=session_id, new_message=content)
        for event in events:
            if event.is_final_response():
                response = event.content.parts[0].text
        return response

async def main():
    monitor = IoTHealthMonitor()
    await monitor.initialize_session("engineer", "session1")
    print(await monitor.query("engineer", "session1", "Check health of device ESP32-A1"))

if __name__ == "__main__":
    asyncio.run(main())

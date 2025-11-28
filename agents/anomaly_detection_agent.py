from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from tools.data_analysis_tools import detect_anomalies, get_sensor_readings

anomaly_detection_tool = FunctionTool(func=detect_anomalies)
sensor_tool = FunctionTool(func=get_sensor_readings)

anomaly_detection_agent = Agent(
    name="anomaly_detection_agent",
    model="gemini-2.5-pro-preview",
    description="Agent that identifies unusual sensor patterns and anomalies.",
    instruction="Retrieve sensor data and detect statistically significant anomalies.",
    tools=[anomaly_detection_tool, sensor_tool]
)

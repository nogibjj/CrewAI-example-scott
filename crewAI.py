from langchain_community.llms import Ollama
import os
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

ollama_openhermes = Ollama(model="openhermes")

ollama_solar = Ollama(model="solar")

researcher = Agent(
    role="researcher", 
    goal="Research methods to grow this website https://scottlai.me/ on X (Twitter)",
    backstory="you are an AI research assistant",
    tools=[search_tool],
    verbose = True,
    llm = ollama_openhermes,
    allow_delegation = False
)

writer = Agent(
    role = "writer",
    goal = "writer compelling and engaging reasons as to why someone should join Scott Lai's X account",
    backstory = "You are an AI master mind capable of growing any X account",
    verbose = True,
    llm = ollama_solar,
    allow_delegation = False
    )

task1 = Task(description = "Inverstigate ScottLai's website on https://scottlai.me/", agent = researcher)
task2 = Task(description = "Inverstigate the competitive of ScottLai's website on https://scottlai.me/ in X", agent = researcher)
task1 = Task(description = "Write a list of tasks Scott Lai must to do to grow this channel", agent = writer)

crew = Crew(
    Agent = [researcher, writer],
    tasks = [task1, task2],
    verbose = 2,
    Process = Process.sequential
)

result = crew.kickoff()

print("############################")
print(result)
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.mcp import MCPServerStdio, MCPServerHTTP, MCPServerSSE
from typing import List

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class DataEngineerAgent:
    """DataEngineerAgent crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    @agent
    def data_engineer(self) -> Agent:
        """Senior Data Engineer agent with watsonx.data MCP server integration"""
        return Agent(
            config=self.agents_config["data_engineer"],  # type: ignore[index]
            verbose=True,
            # llm = LLM(model="ollama/llama3", base_url="http://localhost:11434")
            mcps=[
                MCPServerStdio(
                    command="uvx",
                    args=[
                        "ibm-watsonx-data-intelligence-mcp-server",
                        "--transport",
                        "stdio",
                    ],
                    env={
                        "DI_SERVICE_URL": "",
                        "DI_APIKEY": "",
                        "DI_ENV_MODE": "",
                        "DI_USERNAME": "",
                    },
                )
            ],
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def data_exploration_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_exploration_task"],  # type: ignore[index]
            human_input=True,
        )

    @task
    def data_query_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_query_task"],  # type: ignore[index]
            human_input=True,
        )

    @task
    def data_engineering_report_task(self) -> Task:
        return Task(
            config=self.tasks_config["data_engineering_report_task"],  # type: ignore[index]
            # output_file="report.md",
            human_input=True,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DataEngineerAgent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,  # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )


# Made with Bob

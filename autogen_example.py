import autogen
from autogen import UserProxyAgent, AssistantAgent, config_list_from_json
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen import ConversableAgent  # Use this for the teachable agent


config_list_llama2 = [
    {
        'base_url': "http://0.0.0.0:34708",  # Adjust as necessary
        'api_key': "NULL",
        'model': "ollama/llama2"
    }
]

config_list_mistral = [
    {
        'base_url' : "http://0.0.0.0:8000",
        'api_key' : "NULL",
        'model': "mistral"
    }
]

config_list_codellama= [
    {
        'base_url' : "http://0.0.0.0:28530",
        'api_key' : "NULL",
        'model': "ollama/codellama"
    }
]


llm_config_mistral={
    "config_list" : config_list_mistral,
}

llm_config_codellama={
    "config_list" : config_list_codellama,
}


llm_config_llama2 = {
    "config_list": config_list_llama2, 
    "timeout": 120
}


assistant = autogen_example.AssistantAgent(
    name="Assistant",
    llm_config=llm_config_mistral
)

coder = autogen_example.AssistantAgent(
    name="Coder",
    llm_config=llm_config_codellama
)

teachable_agent = ConversableAgent(
    name="TeachableAgent",
    llm_config=llm_config_llama2
)

# Instantiate a Teachability object with optional parameters
teachability = Teachability(
    reset_db=False,  # Use False to keep existing DB, True to reset
    path_to_db_dir="./tmp/interactive/teachability_db_llama2"  # Ensure unique path for each agent
)

# Add teachability to the teachable agent
teachability.add_to_agent(teachable_agent)


user_proxy = autogen_example.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web", "use_docker": False},
    llm_config=llm_config_llama2,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
    Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)


task="""
teach me how to build an AI autogen agent to dealing with the feedback data
"""

groupchat = autogen_example.GroupChat(agents=[user_proxy, coder, assistant, teachable_agent], messages=[], max_round=12)
manager = autogen_example.GroupChatManager(groupchat=groupchat, llm_config=llm_config_llama2)
user_proxy.initiate_chat(manager, message=task)
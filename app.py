from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FilePurpose, CodeInterpreterTool, ListSortOrder, MessageRole, FunctionTool, ToolSet



def main(): 
    project_endpoint="https://foundryproject-tecnun-resource.services.ai.azure.com/api/projects/foundryproject-tecnun"

    # Connect to the Agent client
    agent_client = AgentsClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential()
    )

    with agent_client:
            
        # Ask user for existing Agent Name in console
        existing_agent_name = input("Enter existing Agent Name: ")

        # Check if agent "data-agent" exists
        agents = list(agent_client.list_agents())
        agent = None
        for a in agents:
            if a.name == existing_agent_name:
                agent = a
                print(f"Found existing agent: {agent.name}")
                break
        if not agent:
            #print agent not found message and exit
            print(f"Agent '{existing_agent_name}' not found. Exiting.")

        # Create a thread for the conversation
        thread = agent_client.threads.create()

        # Loop until the user types 'quit'
        while True:
            user_prompt = input("Enter a prompt (or type 'quit' to exit): ")
            if user_prompt.lower() == "quit":
                break
            if len(user_prompt) == 0:
                print("Please enter a prompt.")
                continue

            message = agent_client.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_prompt,
            )

            run = agent_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

            if run.status == "failed":
                print(f"Run failed: {run.last_error}")

            last_msg = agent_client.messages.get_last_message_text_by_role(
                thread_id=thread.id,
                role=MessageRole.AGENT,
            )
            if last_msg:
                print(f"Last Message: {last_msg.text.value}")

        print("\nConversation Log:\n")
        messages = agent_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
        for message in messages:
            if message.text_messages:
                last_msg = message.text_messages[-1]
                print(f"{message.role}: {last_msg.text.value}\n")
if __name__ == '__main__': 
    main()
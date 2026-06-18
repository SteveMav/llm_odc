import asyncio
import os
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import MessagesState
from langchain.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import END, START, StateGraph


os.environ["OPENAI_API_BASE"] = "http://127.0.0.1:1234/v1"
os.environ["OPENAI_API_KEY"] = "lm_studio"

llm = ChatOpenAI(model="qwen3-1.7b@q6_k")


async def main():
    client = MultiServerMCPClient(
        {
            "Test MCP": {
                "transport": "stdio", # fichier local
                "command": "uv",
                "args": [
                    "run",
                    "--with",
                    "fastmcp",
                    "fastmcp",
                    "run",
                    "C:\\Users\\steve\\OneDrive\\Documents\\IA ODC\\code\\test_mcp.py"
                ]
            },
             "domotique": {
                "transport": "stdio", # fichier local
                "command": "uv",
                "args": [
                    "run",
                    "--with",
                    "fastmcp",
                    "fastmcp",
                    "run",
                    "C:\\Users\\steve\\OneDrive\\Documents\\IA ODC\\code\\serveur_mqqt_mcp.py"
                ]
            }
        }
    )



    tools = await client.get_tools()
    tools_by_name = {tool.name: tool for tool in tools}
    llm_with_tools = llm.bind_tools(tools)

    print(f"Outils chargés : {[tool.name for tool in tools]}")

    async def llm_call(state: MessagesState):
        """LLM decide entre appeler un outil ou non"""

        response = await llm_with_tools.ainvoke(
            [
                SystemMessage(
                    content="Tu es un agent qui peut appeler des outils pour résoudre des problèmes."
                )
            ] + state["messages"]
        )

        return {"messages": [response]}
    
    async def tool_node(state: dict):
        """Appelle l'outil choisi par le LLM"""
        tool_calls = state["messages"][-1].tool_calls
        results = []
        for tool_call in tool_calls:
            tool = tools_by_name[tool_call["name"]]
            observation = await tool.ainvoke(tool_call["args"])
            results.append(
                ToolMessage(content=observation, tool_call_id=tool_call["id"])
            )
        return {"messages": results}
    
    async def should_continue(state: dict):
        """Decide si on continue la boucle d'appel des tools ou non."""
        messages = state["messages"]
        last_message = messages[-1]

        # Si le LLM fait un appel de tools, réaliser l'action
        if last_message.tool_calls:
            return "tool_node"
        
        # Sinon on stock et on returne à l'utilisateur
        return END
    
    # Créer le graphe d'exécution de l'agent
    agent_builder = StateGraph(MessagesState)
    agent_builder.add_node("llm", llm_call)
    agent_builder.add_node("tool_node", tool_node)

    # Connecter les noeuds
    agent_builder.add_edge(START, "llm")
    agent_builder.add_conditional_edges("llm", should_continue, ["tool_node", END])
    agent_builder.add_edge("tool_node", "llm")

    # compiler
    agent = agent_builder.compile()

    # Invoke
    messages = [HumanMessage(content="Additionne 5 et 10 ensuite multiplie par 4")]
    messages = await agent.ainvoke({"messages": messages})
    for m in messages["messages"]:
        m.pretty_print()

if __name__ == "__main__":
    asyncio.run(main())
# from langchain_core.tools import tool
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("echo_tool")

# Add a tool to query the LangGraph documentation
@mcp.tool()
def echo_tool(query: str) -> str:
    """
    Simple echo tool.

    This tool takes a string as input and returns a string where each character
    is separated by a space.

    Args:
        query (str): The string to process.

    Returns:
        str: A string with spaces inserted between each character.
    """
    if not isinstance(query, str):
        raise TypeError("Input 'query' must be a string.")

    # Improved: More efficient string joining
    formatted_context = " ".join(query)

    return formatted_context


if __name__ == "__main__":
    mcp.run()

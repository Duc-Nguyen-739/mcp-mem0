import os
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mem0-cloud")

MEM0_API_KEY = os.environ.get("MEM0_API_KEY", "")
MEM0_BASE_URL = "https://api.mem0.ai/v1"
headers = {
    "Authorization": f"Token {MEM0_API_KEY}",
    "Content-Type": "application/json"
}
USER_ID = os.environ.get("MEM0_USER_ID", "lobehub-default")

@mcp.tool()
async def add_memory(content: str) -> str:
    """Add a memory to Mem0 Cloud."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{MEM0_BASE_URL}/memories/",
            headers=headers,
            json={
                "messages": [{"role": "user", "content": content}],
                "user_id": USER_ID
            }
        )
        return resp.text

@mcp.tool()
async def search_memories(query: str) -> str:
    """Search memories in Mem0 Cloud."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{MEM0_BASE_URL}/memories/search/",
            headers=headers,
            json={"query": query, "user_id": USER_ID}
        )
        return resp.text

@mcp.tool()
async def get_all_memories() -> str:
    """Get all memories from Mem0 Cloud."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{MEM0_BASE_URL}/memories/",
            headers=headers,
            params={"user_id": USER_ID}
        )
        return resp.text

if __name__ == "__main__":
    mcp.run(transport="sse")

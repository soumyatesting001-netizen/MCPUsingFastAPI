from fastmcp import FastMCP
import httpx


mcp = FastMCP(name="Malaysia Telecom MCP",
    instructions="""
You provide read-only access to telecom tower and complaint data in Malaysia.
You MUST only use the provided tools.
Do NOT fabricate data.""")


API_BASEURL = "https://soumyaj-mcmcfastapi.hf.space/"

@mcp.tool()
async def get_towers(
    state: str | None = None,
    technology: str | None = None,
    limit: int = 50
):
    """
    Purpose:
    Retrieve a list of telecom towers operating in Malaysia.

    When to use:
    - When the user asks about telecom towers, coverage, infrastructure,
      or availability of network technology.
    - Use filters instead of guessing or summarizing manually.

    Parameters:
    - state: Optional Malaysian state name (e.g., Selangor, Johor, Sabah).
    - technology: Optional network technology (e.g., 4G, 5G).
    - limit: Maximum number of tower records to return (≤ 500).

    Behavior:
    - Returns only data provided by the backend system.
    - Does not infer missing attributes or generate synthetic towers.
    - If no towers match the filters, return an empty list.

    Output:
    - JSON array of tower records.
    - Each record includes id, name, state, technology, latitude, longitude.

    Safety:
    - Read-only access.
    - Does not modify or create infrastructure records.
    """

    with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{API_BASEURL}/towers",
            params={
                "state": state,
                "technology": technology,
                "limit": limit
            }
        )
        resp.raise_for_status()
        return resp.json()
    
@mcp.tool()
async def get_tower_by_id(tower_id: int):
    """
    Purpose:
    Retrieve detailed information for a specific telecom tower.

    When to use:
    - When the user references a specific tower by identifier.
    - When deeper inspection of a known tower is required.

    Parameters:
    - tower_id: Unique identifier of the telecom tower.

    Behavior:
    - Returns authoritative data from the backend.
    - If the tower does not exist, returns an error from the API.

    Output:
    - JSON object containing full tower details.

    Safety:
    - Read-only operation.
    - No infrastructure changes are possible.
    """

    with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(f"{API_BASEURL}/towers/{tower_id}")
        resp.raise_for_status()
        return resp.json()

@mcp.tool()
async def get_complaints(
    state: str | None = None,
    tower_id: int | None = None,
    limit: int = 50
):
    """
    Purpose:
    Retrieve customer complaints related to telecom services in Malaysia.

    When to use:
    - When the user asks about service issues, outages, or dissatisfaction.
    - Useful for diagnostics and operational analysis.

    Parameters:
    - state: Optional Malaysian state to filter complaints.
    - tower_id: Optional tower identifier for localized complaints.
    - limit: Maximum number of complaint records to return (≤ 500).

    Behavior:
    - Returns historical complaint records only.
    - Does not perform trend prediction or sentiment inference.

    Output:
    - JSON array of complaint records.
    - Each record includes id, date, category, severity, state, tower_id.

    Safety:
    - Read-only.
    - No personal customer-identifying information is exposed.
    """

    with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(
            f"{API_BASEURL}/complaints",
            params={
                "state": state,
                "tower_id": tower_id,
                "limit": limit
            }
        )
        resp.raise_for_status()
        return resp.json()

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)


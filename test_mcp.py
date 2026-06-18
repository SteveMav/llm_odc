from fastmcp import FastMCP

mcp = FastMCP("Simple MCP Server")

@mcp.tool(name="addition", description="Fait l'addition en prenant deux valeurs et retourne leur somme.")
async def add(a: int, b: int) -> int:
    return a + b

@mcp.tool(name="soustraction", description="Fait la soustraction en prenant deux valeurs et retourne leur difference.")
async def substract(a: int, b: int) -> int:
    return a - b

@mcp.tool(name="multiplication", description="Fait la multiplication en prenant deux valeurs et retourne leur produit.")
async def multiply(a: int, b: int) -> int:
    return a * b

@mcp.tool(name="division", description="Fait la division en prenant deux valeurs et retourne leur quotient.")
async def divide(a: int, b: int) -> float:
    if b == 0:
        return "Erreur: Division par zéro."
    return a / b

if __name__ == "__main__":
    mcp.run()
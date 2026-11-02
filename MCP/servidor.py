"""Servidor MCP de ejemplo: consulta un pequeño registro de ventas.

Expone tres tools que Claude (o cualquier cliente MCP) puede llamar.
"""

from mcp.server import MCPServer

mcp = MCPServer("ventas-demo")

# Datos de ejemplo. Más adelante esto puede ser un CSV, SQLite o Databricks.
VENTAS = [
    {"producto": "Cafe", "ciudad": "Bucaramanga", "unidades": 120, "precio": 9000},
    {"producto": "Cafe", "ciudad": "Medellin", "unidades": 80, "precio": 9500},
    {"producto": "Panela", "ciudad": "Bucaramanga", "unidades": 200, "precio": 3500},
    {"producto": "Arepa", "ciudad": "Bogota", "unidades": 150, "precio": 2500},
    {"producto": "Panela", "ciudad": "Bogota", "unidades": 90, "precio": 3800},
]


@mcp.tool()
def listar_productos() -> list[str]:
    """Devuelve la lista de productos distintos que hay en el registro de ventas."""
    return sorted({v["producto"] for v in VENTAS})


@mcp.tool()
def unidades_vendidas(producto: str) -> int:
    """Devuelve el total de unidades vendidas de un producto en todas las ciudades."""
    return sum(v["unidades"] for v in VENTAS if v["producto"].lower() == producto.lower())


@mcp.tool()
def ingresos_por_ciudad(ciudad: str) -> float:
    """Devuelve los ingresos (unidades x precio) de una ciudad, en pesos colombianos."""
    return float(sum(v["unidades"] * v["precio"] for v in VENTAS if v["ciudad"].lower() == ciudad.lower()))


if __name__ == "__main__":
    mcp.run()  # sin argumentos usa stdio: habla por entrada y salida estándar

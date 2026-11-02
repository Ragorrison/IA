"""Cliente de prueba: hace lo mismo que haría Claude, pero desde un script.

Lanza servidor.py como subproceso, pide la lista de tools y llama algunas.
"""

import asyncio
import sys
from pathlib import Path

from mcp import Client, StdioServerParameters

SERVIDOR = Path(__file__).parent / "servidor.py"


async def main() -> None:
    parametros = StdioServerParameters(command=sys.executable, args=[str(SERVIDOR)])

    async with Client(parametros) as cliente:  # 1. initialize (el saludo)
        print("Servidor:", cliente.server_info.name)

        lista = await cliente.list_tools()  # 2. tools/list (descubrimiento)
        print("\nTools disponibles:")
        for tool in lista.tools:
            print(f"  - {tool.name}: {tool.description}")
            print(f"    parametros: {tool.input_schema.get('properties', {})}")

        print("\nLlamadas (tools/call):")  # 3. tools/call (ejecución)
        for nombre, argumentos in [
            ("listar_productos", {}),
            ("unidades_vendidas", {"producto": "Cafe"}),
            ("ingresos_por_ciudad", {"ciudad": "Bogota"}),
        ]:
            resultado = await cliente.call_tool(nombre, argumentos)
            print(f"  {nombre}({argumentos}) -> {resultado.structured_content}")


if __name__ == "__main__":
    asyncio.run(main())

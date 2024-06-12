from mymoney.utils.controllers.GDriveController import GDriveController
from mymoney.utils.clients.GDriveClient import client
import asyncio
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    client = asyncio.run(client.getClient())
    controller = GDriveController(client=client)

    # Exemplo de uso
    folder = asyncio.run(controller.searchFolder("Planilhas"))
    # controller.newFolder("newFoldere", folder[0]["id"])

    print(folder[0]["name"], "-", folder[0]["id"])

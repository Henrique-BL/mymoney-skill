from mymoney.utils.controllers.GDriveController import GDriveController
from mymoney.utils.clients.GDriveClient import client

from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    controller = GDriveController(client=client)

    # Exemplo de uso
    folder = controller.searchFolder("Planilhas")
    controller.newFolder("newFoldere", folder[0]["id"])
    breakpoint()

    print(folder[0]["name"], "-", folder[0]["id"])

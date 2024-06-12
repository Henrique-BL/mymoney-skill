from mymoney.utils.controllers.GDriveController import GDriveController
from mymoney.utils.clients.GDriveClient import client

from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    controller = GDriveController(client=client)

    # Exemplo de uso
    folder_list = controller.list_folders()

    for folder in folder_list:
        print(folder["name"], "-", folder["id"])

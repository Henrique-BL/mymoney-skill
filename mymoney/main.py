from mymoney.utils.controllers.GSheetController import GSheetController
from mymoney.utils.clients.GspreadClient import client
from dotenv import load_dotenv

load_dotenv()
if __name__ == "__main__":
    client = client.getClient()
    controller = GSheetController("test_sheet", client=client)
    controller.initialize()
    controller.insertCell(40, "Outcome", "Money")
    controller.insertCell(40, "Outcome", "Money")
    controller.deleteLastCell("Money")

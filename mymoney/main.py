from mymoney.utils.SheetController import SheetController
from mymoney.utils.GspreadClient import client


if __name__ == "__main__":
    controller = SheetController("test_sheet", client)
    # controller.initialize()
    controller.insertCell(data=200, column="Debit Card", type="Outome")
    cell = controller.searchCell(row=3, col=1)

    controller.deleteLastCell("Money")

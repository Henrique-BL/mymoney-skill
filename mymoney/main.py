from mymoney.utils.SheetController import SheetController
from mymoney.utils.GspreadClient import client


if __name__ == "__main__":
    controller = SheetController("test_sheet", client)
    # controller.initialize()
    controller.insertData(data=887.5, column="Money", type="income")

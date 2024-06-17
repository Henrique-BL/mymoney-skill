import asyncio

from mymoney.schemas.Data import DataIn, DataUpdate
from mymoney.services.DataService import DataService


async def main():
    # Inicializando o serviço
    service = DataService()
    await service.initialize()
    # Criando um novo dado
    data_in = DataIn(type="example_type", value=123.45, row=1, col=3)
    created_data = await service.create_data(data_in)
    print(f"Created Data: {created_data}")

    # # Lendo o dado pelo ID
    data_id = await service.search(1, 1)
    # retrieved_data = await service.get_data_by_id(data_id)
    # print(f"Retrieved Data by ID: {retrieved_data}")

    # # Lendo todos os dados
    # all_data = await service.get_all_data()
    # print(f"All Data: {all_data}")

    # Atualizando o dado
    data_update = DataUpdate(type="income")
    updated_data = await service.update_data(data_id, data_update)
    print(f"Updated Data: {updated_data}")

    # Deletando o dado
    delete_status = await service.delete_data(data_id)
    print(f"Deleted Data Status: {delete_status}")


# # Executando a função main
if __name__ == "__main__":
    asyncio.run(main())

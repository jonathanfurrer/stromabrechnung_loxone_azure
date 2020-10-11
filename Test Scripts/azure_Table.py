from os import pipe
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

credential = "eFH0EUaE6HU8GaqS9S04vf2MLdQ94vMdbMg6kaMetKG1gXU8g+QUtfAKxbtvyjj6Vrq4X3E0hBVNe5gIzjFZHQ=="

table_service = TableService(
    account_name="jofustrom456789", account_key=credential)

task = Entity()
task.PartitionKey = 'tasksSeattle'
task.RowKey = '003'
task.description = 'Wash the car'
task.priority = 100
table_service.insert_entity('D41Strombezug', task)

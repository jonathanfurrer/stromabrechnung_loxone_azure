from os import pipe
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

credential = "eFH0EUaE6HU8GaqS9S04vf2MLdQ94vMdbMg6kaMetKG1gXU8g+QUtfAKxbtvyjj6Vrq4X3E0hBVNe5gIzjFZHQ=="

table_service = TableService(
    account_name="jofustrom456789", account_key=credential)



tasks = table_service.query_entities(
    'D41Strombezug', filter="PartitionKey eq '272-4_day' and cleared eq false")
for task in tasks:
    print(task.value)
    print(task.PartitionKey)
    print(task.paid)
    print(task.cleared)



"""

tasks = table_service.query_entities(
    'D41Strombezug', filter="paid eq 'null'")
for task in tasks:
    print(task.value)
    print(task.paid)
"""
from modules.get_chain_and_rpc import user_input
from modules.get_tokens_data import get_tokens_data
from modules.swapper import swap_manager
import asyncio

def menu():
    #Выбираем сеть
    user_input
    while True:
        #Выбираем действия с кошельком
        print('Choose option like 1, 2, 3 etc: ')
        print('1. Check balance')
        print('2. Make swap')
        print('3. Exit')
            
        choises = input('Option: ')
        if choises == '1':
            get_tokens_data()
        if choises == '2':
            asyncio.run(swap_manager.main())
        if choises == '3':
            break

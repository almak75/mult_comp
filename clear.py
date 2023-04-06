import pandas
import pickle
RATING_FILE = 'comp.txt'    #здесь будем хранить данные с рейтингом
with open(RATING_FILE, 'rb') as file:
     rating = pickle.load(file)
print('\n\n\nДо удаления')

print(rating)
for i in ['Тестовый Тест', 'Выберите..']:
    if i in rating.index:
        rating = rating.drop(index = i, axis = 1)
print('\n\n\nПосле удаления')
print(rating)
with open(RATING_FILE, 'wb') as handle:
     pickle.dump(rating, handle, protocol=pickle.HIGHEST_PROTOCOL)
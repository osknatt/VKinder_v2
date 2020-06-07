# Дипломная работа


## VKinder
Все слышали про известное приложение для знакомств - Tinder. Приложение предоставляет простой интерфейс для выбора понравившегося человека. Сейчас в Google Play более 100 миллионов установок.

Используя данные из VK нужно сделать сервис намного лучше чем Tinder. Искать людей, подходящих под условия, на основании информации о пользователе из VK:
- диапазон возраста,
- пол,
- группы,
- расположение,
- интересы, 
- любой другой необязательный параметр.

У каждого критерия поиска должны быть свои веса. То есть совпадение по возрасту должны быть важнее общих групп. Интересы по музыке важнее книг. Наличие общих друзей важнее возраста.

Разбор похожих интересов(книги, музыка, интересы) нужно будет провести с помощью анализа текста.

У тех людей, которые подошли по требованиям пользователю, получать топ-3 популярных фотографии с аватара. Популярность  определяется по количеству лайков.

## Входные данные
Имя пользователя или его id в ВК, для которого мы ищем пару.
- если информации недостаточно нужно дополнительно спросить её у пользователя.


## Выходные данные
JSON-файл с 10 объектами, где у каждого объекта перечислены топ-3 фотографии и ссылка на аккаунт.

## Требование к сервису:
1. Код программы удовлетворяет`PEP8`.
2. Получать токен от пользователя с нужными правами.
3. Программа декомпозирована на функции/классы/модули/пакеты.
4. Результат программы записывать в БД.
5. Люди не должны повторяться при повторном поиске.(ЧТО ЭТО ОЗНАЧАЕТ? ЧТО ПОВТОРНЫЙ ПОИСК СОЗДАЕМ ФАЙЛ С НОВЫМИ ЛЮДЬМИ? - спросить у руководителя
6. Реализовать тесты на базовую функциональность.
7. Не запрещается использовать внешние библиотеки для vk.


## Дополнительные требования (не обязательны для получения диплома):
1. В vk максимальная выдача при поиске 1000 человек. Подумать как это ограничение можно обойти.
2. Добавить возможность ставить/убирать лайк, выбранной фотографии.
3. Добавлять человека в избранный список, используя БД.
4. Добавлять человека в черный список чтобы он больше не попадался при поиске, используя БД.
5. К списку фотографий из аватарок добавлять список фотографий, где отмечен пользователь.

*****Реализация*****
Создаем класс пользователя
Задаем у класса методы:
- init
	Проверяем, открыта ли информация с помощью try?

- получить друзей - записываем в множество
- получить группы - множество
- получить инфо о возрасте
- получить инфо о поле
- получить инфо о городе
- получить инфо об интересах


Критерии весов: записываем в виде словарика
common_friends 10 (10/50 = 0,2)
age 8 
common_groups 7 
sex = 12
city = 7
interests (books, music, movies) = 6


Основная функция кода:
Создаем пустой словарь для 10 итоговых объектов {ключ: user_id, значение: список [имя фамилия, 3 фото, ссылка на аккаунт])}
Начинаем поиск всех людей по диапазону возраста и полу, записываем их в пустой словарь.
Далее в цикле по этим друзьям ищем совпадение по критериям:
	1. Общие друзья - пересекаем множество друзей пользователя с мн-вом друзей человека. Каждое совпадение дает +10 баллов 
	2. Город - совпадение дает +7 баллов
	3. Общие группы - пересекаем множества - каждое совпадение групп дает + 7 баллов
	4. Общие интересы с помощью анализа текста ищем совпадения с нашим пользователям по словам с числом знаков более 3
	5. Совпадение по возрасту - на каждую единицу различия вычитаем - 1
	Результат каждого вычисления добавляем в наш словарь.
	Сортируем по убыванию и топ-10 записываем в файл json, а также записываем необходимые данные
print('Рекомендации были созданы и записаны в файл!')

if name = main,
принимаем на вход имя пользователя или его id
запускаем осн.функцию кода



	 
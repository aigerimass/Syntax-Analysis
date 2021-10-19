### Отчет по проекту

#### Задача
`L`
 - Конкретный синтаксис
 - Парсер
 - Интервальный анализ

#### Синтаксис языка
 - Язык был составлен на основе синтаксиса языка Си
 - Программой на языке L является возможно пустая последовательность определений функций и одна функция-точка-входа ```Main```. 
- Все функции начинаются с большой буквы, в круглых скобках записываются названия аргументов через `;`, в фигурных скобках тело функции.  Телом функции является некоторый оператор.
```cpp
Function(arg1; arg2; arg3) {
    skip;
}
```
- Литералы языка: числа в десятичной и двоичной записях, строковые литералы
```cpp
number = 1234;
string = "sdfs";
number_2 = 10101110;
```
- Операторы:
1) Пустой оператор skip.
```cpp
skip
```
2) Условный оператор. Содержит условие (выражение). Ветви -- операторы, ветвь else опциональна.
```cpp
if (condition) {
    skip;
} else {
    skip;
}
```
3) Оператор цикла с предусловием. Условием является выражение, телом -- оператор.
```cpp
while (condition) {
    skip;
}
```
4) Оператор связывания (присвоения значения) переменной. Связывает переменную со значением выражения.
```cpp
a = 1
-------
a = "a"
-------
b = a
```
5) Последовательность операторов (как ; в си-подобных).
```cpp
skip;
if (condition) {skip;};
while (condition) {skip;};
```
6) Вызов функции.
```cpp
Function(1; 2; 3)
```
7) Возврат значения из функции
```cpp
return a
```

 - Базовыми выражениями являются литералы, переменные или вызовы функций.

Допустимые бинарные операции с их арностью и ассоциативностью приведены в таблице:

  | Приоритет | Оператор             | Арность  | Ассоциативность   |
  | :-------- | :------------------- | :------- | :---------------- |
  | Высший    | ^                    | Бинарный | Правоассоциативна |
  |           | -                    | Унарный  |                   |
  |           | *, /                 | Бинарный | Левоассоциативна  |
  |           | +, -                 | Бинарный | Левоассоциативна  |
  |           | ==, /=, <=, <, >=, > | Бинарный | Неассоциативна    |
  |           | !                    | Унарный  |                   |
  |           | &&                   | Бинарный | Правоассоциативна |
  | Низший    | \|\|                 | Бинарный | Правоассоциативна |

```cpp
a = b + (12^(3*4)) + Function(2,3,4);
```

#### Синтаксический анализ

- Парсер написан с помощью ``yacc`` на языке `Python`
- Результат парсинга -- дерево с корнем типа `Program`. От него ветви уходят в определения функций.
- Узел, соответствующий определению функции, хранит список аргументов. Из него идут ветви в операторы, составляющие тело функции.
- Из операторов идут ветви либо в другие операторы, которые составляют тело текущего оператора, либо в выражение
- Из выражений идут ветви в промежуточные нетерминалы для выражений, оператор вызова функции, литералы или переменные.
- Каждый узел умеет отображать все поддерево, корнем которого является
- Чтобы посмотреть, что распарсилось во всей программе, нужно вызвать метод ```show()``` у результата парсинга (Объект типа `Program`)
- Построенное дерево передается дальше для интервального анализа.

#### Интервальный анализ

- 

#### Разделение работы

Айгерим Асылханова:
- План синтаксического разбора, разработка классов для узлов синтаксического дерева
- Построение дерева
- Отображение дерева

Рамазан Джекшембаев:
- Лексер
- Интервальный анализ синтаксического дерева






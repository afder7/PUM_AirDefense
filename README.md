# Моделирование работы комплекса ПВО

## Краткая информация
В рамках данного задания требуется реализовать приложение, моделирующее работу системы ПВО (противовоздушной обороны), защищающую некий наземный объект. Система ПВО будет содержать несколько компонентов: РЛС (радиолокационная станция), выявляющая воздушные цели, и орудие, выпускающее по ним снаряды. Целями ПВО будут ракеты, пытающиеся атаковать защищаемый объект.
![Air Defence](air_defence.png)

## Описание сущностей
### Комплекс ПВО
Как уже было сказано вначале, комплекс ПВО в данной задаче будет состоять из двух компонентов: РЛС и орудия. Будем считать, что оба компонента физически размещаются в одном корпусе, чтобы избежать лишних вычислений, связанных с удаленностью РЛС от орудия.

РЛС позволит нам выявлять угрозы с воздуха. Единственной характеристикой данной системы является дальность ее работы, т.е. максимальное расстояние, на котором она "видит" объекты. Будем считать, что она работает без задержек, т.е. сообщает нам обо всех видимых объектах, как только мы ее об этом попросим, при этом мы можем немедленно обратиться к ней снова и получить результат. Результат система должна выдавать в виде списка кортежей (тип `tuple`), элементами которого являются уникальный идентификатор объекта, угол между вертикальной осью и объектом (измеряется от -pi / 2 до pi / 2), а также расстояние до объекта в метрах. Такая система координат называется полярной. Создайте для РЛС класс `Radar` со свойством `max_distance` и методом `scan`. Метод `scan` должен пробежаться по всем объектам-целям, перевести декартовы координаты в полярные, отбросить все объекты, находящиеся дальше, чем `max_distance` и вернуть список оставшихся троек. Этот ответ метод должен напечатать в консоль в виде: `SCANINIG: (1, 30, 1400), (2, -45, 1500)`. Здесь угла следует перевести в градусы.

Орудие способно выпускать снаряды, представляющие из себя металлические шары, с некоторой скоростью. Например, 1 раз в секунду. Очень важно блокировать орудие после выстрела на этот интервал времени. Придумайте, как это можно сделать при помощи `root.after()`. Снаряды должны лететь по баллистической траектории: на них действуют гравитация и сила сопротивления воздуха. Такой снаряд может сбить цель только при точном попадании. Орудие должно поворачиваться по нажатию на стрелки клавиатуры (влево и вправо). Угловая скорость поворота должна быть не более 30 градусов за одну секунду. Придумайте, каким образом это сделать. Выстрел должен производиться по клавише пробела. Начальную скорость снаряда сделайте глобальной константой. Постарайтесь подобрать для нее правдоподобное значение. Класс снаряда назовите `Bullet`.

### Ракеты
Ракеты должны спавниться за пределами окна и лететь в направлении защищаемого объекта, как это показано на рисунке. Все они должны обязательно пролетать через верхнюю "стенку" кадра (они не должны атаковать объект сбоку). Считайте, что все ракеты движутся равномерно и прямолинейно. Их скорости должны различаться, но находиться в разумных и адекватных пределах. Храните их в глобальном списке, заведите для них класс `Rocket`.

Оба класса `Rocket` и `Bullet` унаследуйте от общего предка `MovingObject`. Всю логику движения реализуйте в базовом классе, классы для ракет и снарядов нужны, чтобы задать в них характеризующие эти объекты характеристики движения.

## Взаимодействие объектов
Цель игры -- сбить все ракеты. При выявлении попадания снаряда в ракету (придется выявить, что кружок "наложился" на прямоугольник) оба объекта исчезают.

## Это "4"
На "4" достаточно реализовать вышеописанную игру. В случае, если что-либо будет реализовано некорректно, оценка будет снижена до "3". Помните, что задача -- моделирование. Как мы проходили, адекватность модели -- критерий ее приненимости для анализа оригинала. Сделайте модель адекватной.

## А это "5"?
На "5" требуется добавить самую малость: тумблер, переводящий комплекс ПВО в автоматический режим работы. В данном режиме РЛС перестает быть бесполезным сканером воздушного пространства, а будет для орудия единственным источником информации о ситуации в небе. Теперь комплекс должен пытаться самостоятельно сбить угрожающие грибочку ракеты, но, как только пользователь нажмет любую из клавиш управления орудием, комплекс должен моментально перейти в режим ручного управления, идентичный варианту выполнения на "4". Еще раз: орудие не имеет права "подсматривать" в объекты `Rocket`, единственным источником информации для него должна служить система РЛС! Траектории ракет придется восстанавливать, используя несколько наблюдений за объектами (для этого пригодятся их идентификаторы).

## Дедлайны
Для групп, у которых уроки по вторникам: 07.02.2023 включительно<br>
Для групп, у которых уроки по средам: 08.02.2023 включительно

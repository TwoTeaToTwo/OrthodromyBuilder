# Построение ортодрома
## Установка
### Frontend
1. Нужно [скачать и установить](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)  npm последней версии.
2. Установить yarn
```shell
npm install --global yarn
```
3. В папке frontend выполнить следующую команду
```shell
yarn
```

### Backend
1. Нужно скачать и установить последнюю версию python3
2. Через pip скачать следующие пакеты
```shell
pip install flask
pip install pyproj
```

## Запуск
1. В папке frontend выполнить следующую команду
```shell
yarn build
```
2. В папке backend запустить скрипт main.py
```shell
python main.py
```

## Функционал
### Frontend
Можно вводить координаты двух точек на правой панели, указывать количество полигонов(узлов) для построения ортодрома и систему координат. На данный момент доступны следующие EPSG: 4326, 4284, 3857.

### Backend
Реализован весь функционал, создан адаптер для более удобного использования ортодрома.

![Пример работы sk42](https://sun9-24.userapi.com/impg/GmqLl2gawnWqkIQj0cLrFRXv2Ws1t01teWmuXg/r94eDQ-iHow.jpg?size=1907x942&quality=96&sign=2220c8dd4a87dcf051c5554f4a377acd&type=album)

![Пример работы Mercator](https://sun9-43.userapi.com/impg/SYD1sUQcH-mY426cU4whiq698KRbGAq-zev7mg/rPxNgcrczeo.jpg?size=1920x941&quality=96&sign=97c305f0529881a2dd1fb2089cf6e1bb&type=album)

![Пример работы 1 WGS84](https://sun9-21.userapi.com/impg/OYSY6PUKMEncxn7UaF28LpXoLfqO-q9g4-rw4A/tMOU5oE3rCA.jpg?size=1919x956&quality=96&sign=812f2e1de2a82dab8b99e0f00a1afcb4&type=album)

![Пример работы 2 WGS84](https://sun9-49.userapi.com/impg/A1kGj-MvSDEoqJcFm2nfD3zjcJnoJ3dGhu9MrQ/EXOBz1y5yYE.jpg?size=1915x948&quality=96&sign=c545754b4c593c140e6b0c3a7d349ddf&type=album)
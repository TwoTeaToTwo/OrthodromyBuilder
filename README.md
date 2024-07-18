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
### Если возникли трудности после 2го пункта, то попробовать
3. Установить следущий список пакетов
```shell
yarn add vite
yarn add svelte
```
4. В папке frontend проекта
```shell
yarn add normalize.css
yarn add leaflet
yarn add @types/leaflet
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

p.s может добавлю makefile для быстрого запуска проекта

## Функционал (main)
### Frontend
Можно вводить координаты двух точек на правой панели, указывать количество полигонов(узлов) для построения ортодрома. На данный момент в main находится стабильная версия реализации только для WGS84.
### Backend
Реализован весь функционал, создан адаптер для более удобного использования ортодрома.

![Пример работы](https://sun9-23.userapi.com/impg/f5TjzkxciiSxJxMUqum7MzGwMAc0a007UAxd0w/gZukGhehUeU.jpg?size=1920x954&quality=96&sign=a268e7cb72a77566ea291616d13e4939&type=album)

### Функционал (develop)
### Frontend
Для Меркатор иногда правильно отображает ортодром на экране, но чаще всего неверно. При вводе координат в этой СК может падать сайт.
СК-72 в разработке.
### Backend
Изменений нет.

![Пример работы](https://sun9-11.userapi.com/impg/4V-euGhrlruFzSxKfoM01hgoz3O_kHWJzfbu2w/nCZZ95vLEY0.jpg?size=1901x906&quality=96&sign=ba4a02ecf449f66de3117dc8ce2f1072&type=album)
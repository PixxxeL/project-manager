# Console Project Manager

Консольное приложение. Создает локальный проект для разработки
и репозиторий проекта.

## Загрузить

[Бинарники](https://github.com/PixxxeL/new-project/releases)

## Типы проектов

### Статический проект

Полностью статический проект. Только HTML, CSS, Javascript.
Для упрощения работы с кодом используется
[Jade](http://jade-lang.com/) вместо HTML,
[SASS](http://sass-lang.com/) вместо CSS
и [CoffeeScript](http://coffeescript.org/) вместо Javascript.

Для работы проекта нужны:

* [Python](https://www.python.org/downloads/) или [PHP](http://php.net/downloads.php) для локального сервера
* [Node](https://nodejs.org/en/download/) с [NPM](https://docs.npmjs.com/getting-started/what-is-npm)
* [Gulp](http://gulpjs.com/)
* [Bower](https://bower.io/)

### Статический проект с обратной связью на PHP

Статический проект, но с минимальными серверными возможностями,
реализованными на PHP, в частности, с отправкой писем.

### Чистый Django 1.11

Чистый Django 1.11 проект с клиентской частью обычной или react
на выбор.

## В планах

* Добавление файла конфигурации, чтобы не заполнять папку проекта и пользователя
* Аргументы командной строки для создания, редактирования, публикации: start (+из репо) deploy extend publish
* Добавление других типов проектов: Grappelli, Mezzanine, Joomla, Wordpress(?)
* Проверка зависимостей (возможно их установка)
* Шел-скрипты для nix

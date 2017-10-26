@echo off

::chcp 1251

set app_path=D:\storage\new-project\
set py_pro=D:\python\pro
set py_pro_st=/D/python/pro
set php_pro=D:\www\htdocs
set php_pro_st=/D/www/htdocs
set repo_user=pixxxel

for /f "delims=" %%i in (%app_path%.pwd) do if not defined repo_pwd set repo_pwd=%%i 
set repo_acc=%repo_user%:%repo_pwd%
set api_url=https://api.bitbucket.org/2.0/repositories/%repo_user%/
set git_url=git@bitbucket.org:%repo_user%/
set client=https://raw.githubusercontent.com/PixxxeL/regular-gulpfile/master/new-client.bat
set cuurent_dir=%cd%
:: https://github.com/jeremejevs/cmdcolor
set colorize=%app_path%cmdcolor.exe
set bb_data=%app_path%bitbucket.json

IF "%2" == "" (
    echo \033[91m You must define project name. For example: | %colorize%
    echo \033[91m new-project.bat py proj-example | %colorize%
    goto EOF
)
set pro_name=%2

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
if /I "%1" == "py" (
    goto PYTHON
) else if /I "%1" == "php" (
    goto PHP
) else (
    echo \033[91m You must define type of project as `python` or `php`. For example: | %colorize%
    echo \033[91m new-project.bat py proj-name | %colorize%
    goto EOF
)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:PYTHON
    set pro_path=%py_pro%\%pro_name%
    set pro_nix_path=%py_pro_st%

    echo \033[92m Create directories docs, media... | %colorize%
    mkdir %pro_path%\docs
    mkdir %pro_path%\media

    echo \033[92m Create virtual environment at env... | %colorize%
    virtualenv %pro_path%\env

    echo \033[92m Create batch files... | %colorize%
    echo env\Scripts\activate > %pro_path%\envi.bat
    echo cd repo\client ^&^& gulp > %pro_path%\cli.bat
    echo python repo\server\manage.py %%1 %%2 %%3 %%4 %%5 %%6 %%7 %%8 %%9 > %pro_path%\mana.bat
    echo python repo\server\manage.py runserver 8080  > %pro_path%\runs.bat

    goto COMMON

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:PHP
    set pro_path=%php_pro%\%pro_name%
    set pro_nix_path=%php_pro_st%

    echo \033[92m Create directories docs, www... | %colorize%
    mkdir %pro_path%\docs
    mkdir %pro_path%\www

    goto COMMON

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:COMMON
    echo \033[92m Create project file... | %colorize%
    set f=%pro_path%\%pro_name%.sublime-project
    echo { > %f%
    echo     "folders": >> %f%
    echo     [ >> %f%
    echo         { >> %f%
    echo             ^"path^": ^"%pro_nix_path%/%pro_name%^" >> %f%
    echo         } >> %f%
    echo     ] >> %f%
    echo } >> %f%

    echo \033[92m Download new-client script file... | %colorize%
    curl -O %client% && mv new-client.bat %pro_path%\new-client.bat

    echo \033[92m Create repository... | %colorize%
    curl -X POST -u %repo_acc% -H "Content-Type: application/json" -d @%bb_data% %api_url%%pro_name%
    mkdir %pro_path%\repo && cd %pro_path%\repo && git init
    git remote add origin %git_url%%pro_name%.git
    echo /client/bower_components> %pro_path%\repo\.gitignore
    echo /client/node_modules>> %pro_path%\repo\.gitignore
    echo /client/html>> %pro_path%\repo\.gitignore
    echo *.pyc>> %pro_path%\repo\.gitignore
    echo *.sql>> %pro_path%\repo\.gitignore
    echo *.log>> %pro_path%\repo\.gitignore
    echo *.sqlite3>> %pro_path%\repo\.gitignore
    echo *.db>> %pro_path%\repo\.gitignore
    echo local_settings.py>> %pro_path%\repo\.gitignore
    echo # %pro_name% > %pro_path%\repo\readme.md
    git add .gitignore readme.md
    git commit -m "Init commit"
    git push origin master
    mkdir %pro_path%\repo\client
    mv %pro_path%\new-client.bat %pro_path%\repo\client\new-client.bat
    
    goto EOF

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:EOF
    cd %cuurent_dir%
    echo.
    echo \033[0m Job finished! | %colorize%

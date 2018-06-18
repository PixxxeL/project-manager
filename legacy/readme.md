# Create New Project

This batch file intended for create project skeleton on my Windows station.
You may use it also. To do:
* Type password of your bitbucket repository in `.pwd` file (create it before).
* Set variables `app_path` - where `new-project.bat` live,
`py_pro` - where Python's projects live,
`py_pro_st` same as py_pro but for Sublime,
`php_pro` and `php_pro_st` - for PHP projects,
`repo_user` - user login from Bitbucket.
* I'm using [Sublime Text](https://sublimetext.com/2) for coding. Install it.
* You must install [cURL](https://curl.haxx.se/download.html) for Windows
and [Git for Windows](https://git-scm.com/download/win) that run from this script.
* Also need [Virtual Environment](https://virtualenv.pypa.io/en/stable/) for Python.
* You may set path to `new-project.bat` in system `PATH` variable for using script anywhere.

Script download `new-client.bat` in `repo/client` directory of created project. Run it for set client environment.

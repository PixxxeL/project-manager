@echo off

chcp 1251

set root=%cd%

env\Scripts\activate && cd repo\server && fab build_and_deploy && cd %root%

@echo off
call "%~dp0.venv\Scripts\python.exe" -m ipykernel install --user --name=imdb_project --display-name="IMDb Project"
echo Kernel registered successfully!

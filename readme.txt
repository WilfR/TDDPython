Use the TDDPython environment.
See https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html for info on environments.

Here is how I created the virtual environment :

conda create -n TDDPython
conda activate TDDPython
pip install "django<1.12" "selenium<4"
prompt (TDDPython) $p$g

Installed Firefox via "choco install firefox"
Downloaded and installed geckodriver.exe



Running the Django dev server
    python manage.py runserver

Running the functional tests
    python functional_tests.py

Running the unit tests
    python manage.py test



1. Activate virtual environment:

Scripts/Activate.ps1

2. Run pyinstaller:

pyinstaller .\gui.spec

3. If program doesn't start (missing modules), add all modules to the hidden imports (inside spec file):

hiddenimports=['markdown2', 'another_module', 'etc'],
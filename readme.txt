1. create exe


pyinstaller --onefile --windowed --name Fund-Trail-Analyser --add-data "templates;templates" --add-data "static;static" --add-data "lib;lib" --icon=rspc.ico launcher.py


pyinstaller --onefile --windowed --name Fund-Trail-Analyser --add-data "templates;templates" --add-data "static;static" --collect-all pyvis --icon=rspc.ico launcher.py

pyinstaller --onefile --windowed --name Fund-Trail-Analyser --add-data "templates;templates" --add-data "static;static" --collect-all pyvis --icon=foresightdigital.ico launcher.py

pyinstaller --onedir --windowed --name Fund-Trail-Analyser --add-data "templates;templates" --add-data "static;static" --add-data "jdk.zip;." --hidden-import=jpype --collect-all pyvis --add-data "D:\application\\transaction analyser merged\venv\Lib\site-packages\tabula\tabula-1.0.5-jar-with-dependencies.jar;tabula" --icon=foresightdigital.ico launcher.py


pyinstaller --onedir --windowed --name Fund-Trail-Analyser --add-data "templates;templates" --add-data "static;static" --collect-all jpype --add-data "jdk.zip;." --add-data "D:\application\\transaction analyser merged\venv\Lib\site-packages\tabula\tabula-1.0.5-jar-with-dependencies.jar;tabula" --collect-all pyvis --icon=foresightdigital.ico launcher.py

pyinstaller --onedir --windowed --name Fund-Trail-Analyser --add-data "templates;templates" --add-data "static;static" --collect-all jpype --collect-all numpy --add-data "jdk.zip;." --add-data "D:\application\\transaction analyser merged\venv\Lib\site-packages\tabula\tabula-1.0.5-jar-with-dependencies.jar;tabula" --collect-all pyvis --add-binary "msvcp140.dll;." --add-binary "vcruntime140.dll;." --add-binary "vcruntime140_1.dll;." --icon=foresightdigital.ico launcher.py



--collect-all pyvis

2. delete normal user

flask shell
from app import db, User
# Delete all normal users (non-superusers)
User.query.filter_by(is_superuser=False).delete()
db.session.commit()


3 delete all users

# Import the necessary modules from app.py
from app import db, User

# Delete all users
User.query.delete()
db.session.commit()

# Optionally, verify the deletion
remaining_users = User.query.all()
print(f"Number of users remaining: {len(remaining_users)}")


4. initialize superuser

python initialize_db.py

5. create virtual env

python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
venv\Scripts\activate

6.remove dist folder

Remove-Item -Recurse -Force dist

7. initialize databse of superuser

python initialize_db.py


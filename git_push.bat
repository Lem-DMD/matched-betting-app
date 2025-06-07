:: Step 1 – Navigate to your project folder
cd /d D:\matched_betting_app

:: Step 2 – Initialize Git (creates .git folder)
git init

:: Step 3 – Stage all files for commit
git add .

:: Step 4 – Save your changes with a commit message
git commit -m "Initial matched betting app"

:: Step 5 – Set default branch to main
git branch -M main

:: Step 6 – Add your GitHub repo as a remote origin
git remote add origin https://github.com/Lem-DMD/matched-betting-app.git

:: Step 7 – Push your code to GitHub (you’ll be asked to log in)
git push -u origin main

echo "Pushing to GitHub..."
git add .
git commit -m "Added CSTR data code"
git branch -M main
git remote add origin https://github.com/Goldenprince8420/cstr-aspen-optim.git
git push -u origin main
echo "Done!!"

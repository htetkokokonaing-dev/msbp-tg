# Termux quick commands for GitHub upload

GitHub CLI may be difficult in Android/Termux environments. The most reliable route is often to upload this ZIP to a desktop/laptop, extract it, and use GitHub Desktop or the GitHub web UI.

If you use Termux, run from the extracted repository root:

```bash
pkg update -y
pkg install -y git zip unzip

git init
git add .
git commit -m "Prepare MSBP-Tg public-safe preprint package"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/MSBP-Tg.git
git push -u origin main

git tag -a preprint-candidate -m "MSBP-Tg preprint candidate"
git push origin preprint-candidate
```

If `git push` asks for a password, use a GitHub personal access token instead of your account password.

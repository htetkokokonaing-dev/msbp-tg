# GitHub upload commands

Recommended public repository name:

```text
MSBP-Tg
```

Replace `YOUR_GITHUB_USERNAME` with your GitHub username. Run commands from the extracted repository root.

## Option A: GitHub CLI workflow

```bash
git init
git add .
git commit -m "Prepare MSBP-Tg public-safe preprint package"

gh auth login
gh repo create YOUR_GITHUB_USERNAME/MSBP-Tg --public --source=. --remote=origin --push

git tag -a preprint-candidate -m "MSBP-Tg preprint candidate"
git push origin preprint-candidate

gh release create preprint-candidate \
  --title "MSBP-Tg preprint candidate" \
  --notes-file RELEASE_NOTES.md \
  manuscript/MSBP_Tg_Journal_Manuscript.pdf \
  manuscript/MSBP_Tg_Journal_Manuscript.docx
```

## Option B: Git commands after manually creating the GitHub repository

Create an empty public GitHub repository named `MSBP-Tg`, then run from the extracted repository root:

```bash
git init
git add .
git commit -m "Prepare MSBP-Tg public-safe preprint package"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/MSBP-Tg.git
git push -u origin main

git tag -a preprint-candidate -m "MSBP-Tg preprint candidate"
git push origin preprint-candidate
```

Then create the release in the GitHub web UI:

- Tag: `preprint-candidate`
- Title: `MSBP-Tg preprint candidate`
- Description: paste `RELEASE_NOTES.md`
- Optional assets: attach the manuscript PDF and DOCX

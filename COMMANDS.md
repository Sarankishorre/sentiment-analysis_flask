# Quick Command Reference

## 🚀 PUSH TO GITHUB (One Command)

```powershell
cd D:\ml\flask
.\PUSH_TO_GITHUB.ps1
```

---

## 📋 Manual Steps (If Script Doesn't Work)

```powershell
# 1. Navigate to project
cd D:\ml\flask

# 2. Initialize git (if needed)
git init

# 3. Configure git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 4. Stage all files
git add .

# 5. Create commit
git commit -m "Initial commit: Sentiment Analysis API with ML model and web interface"

# 6. Add remote repository
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/sentiment-analysis-api.git

# 7. Set main branch
git branch -M main

# 8. Push to GitHub
git push -u origin main

# When prompted for password, use your Personal Access Token
```

---

## 🔍 Verify Git Setup

```powershell
# Check git version
git --version

# Check user configuration
git config --global user.name
git config --global user.email

# Check current status
git status

# Check remote configuration
git remote -v

# View commit history
git log --oneline
```

---

## 🛠️ Common Git Commands After Initial Push

```powershell
# See what changed
git status

# Stage specific file
git add filename.py

# Stage all changes
git add .

# Create commit
git commit -m "Your message here"

# Push changes
git push

# Pull latest changes
git pull

# Create new branch
git branch feature-name
git checkout feature-name
# Or: git switch feature-name

# View all branches
git branch -a

# View commit history
git log
git log --oneline
git log -5

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Discard changes to file
git checkout -- filename.py

# View differences
git diff
git diff HEAD~1
```

---

## 🔐 GitHub Authentication

### Setup Personal Access Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scope: `repo`
4. Copy token and save securely
5. Use token as password when git prompts

### SSH Alternative
```powershell
# Generate SSH key (one time)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add public key to GitHub:
# Settings → SSH and GPG keys → New SSH key

# Use SSH URL instead of HTTPS:
git remote set-url origin git@github.com:YOUR_USERNAME/sentiment-analysis-api.git
```

---

## 📁 Project Structure

```
D:\ml\flask\
├── app.py                    # Flask API
├── README.md                 # Main documentation
├── HOW_IT_WORKS.md          # Technical details
├── GIT_PUSH_GUIDE.md        # Git instructions
├── README_PUSH.md           # Push instructions
├── requirements.txt         # Dependencies
├── test_api.ps1            # API tests
├── PUSH_TO_GITHUB.ps1      # Push script (PowerShell)
├── PUSH_TO_GITHUB.bat      # Push script (Batch)
├── COMMANDS.md             # This file
├── .gitignore              # Files to ignore
├── models/
│   ├── model.joblib        # ML model
│   └── vectorizer.joblib   # Text vectorizer
├── sentiment-analysis/     # Cloned repo
│   ├── sentiment_analysis.ipynb
│   ├── train.csv
│   ├── export_model.py
│   └── README.md
└── __pycache__/            # (ignored)
```

---

## 🎯 Typical Workflow

```powershell
# 1. Make changes to app.py or other files
# (Edit code...)

# 2. Check status
git status

# 3. Stage changes
git add .

# 4. Commit
git commit -m "Add new feature: batch processing"

# 5. Push
git push

# 6. Check on GitHub
# Visit https://github.com/YOUR_USERNAME/sentiment-analysis-api
```

---

## 🚨 Troubleshooting Quick Fixes

```powershell
# "fatal: not a git repository"
git init

# "Authentication failed"
# Use Personal Access Token instead of password
# Or setup SSH keys

# "Repository already exists"
git remote set-url origin https://github.com/YOUR_USERNAME/new-repo-name.git

# "Git: command not found"
# Install Git from https://git-scm.com/

# "fatal: origin does not appear to be a git repository"
git remote add origin https://github.com/YOUR_USERNAME/sentiment-analysis-api.git

# Undo recent changes
git reset --hard HEAD~1  # Caution: discards changes

# See what will be committed
git diff --cached

# Unstage files
git reset HEAD filename.py
```

---

## 💡 Pro Tips

1. **Commit Often**: Small, frequent commits are better than large ones
2. **Write Clear Messages**: Use present tense ("Add feature" not "Added")
3. **Check Status**: Always run `git status` before committing
4. **Use Branches**: Create branches for features: `git checkout -b feature/my-feature`
5. **Keep .gitignore Updated**: Add files that shouldn't be tracked
6. **Never Commit Secrets**: Don't push API keys, passwords, or tokens

---

## 📚 Useful Links

- **Create Personal Access Token**: https://github.com/settings/tokens
- **Git Documentation**: https://git-scm.com/doc
- **GitHub Docs**: https://docs.github.com/
- **Commit Message Guide**: https://chris.beams.io/posts/git-commit/
- **GitHub Markdown**: https://docs.github.com/en/github/writing-on-github

---

## ✨ After First Push

```powershell
# Make a change
# (Edit app.py...)

# Add the change
git add app.py

# Commit
git commit -m "Improve error handling in predict endpoint"

# Push (no -u needed now)
git push

# Verify on GitHub
# https://github.com/YOUR_USERNAME/sentiment-analysis-api
```

---

**Save this file for quick reference! 🎯**

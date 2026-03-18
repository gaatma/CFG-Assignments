#  Gifty Acquah — CFG Data Science & ML Assignments

## About Me

Hi! I'm **Gifty Acquah**, a PhD Candidate in Information Systems Engineering 
at **Concordia University**, researching cybersecurity and AI for critical 
infrastructure protection. I am also a Data Science & ML student with 
**Code First Girls (CFG)**.

---

##  Previous Projects & Experience

| Project | Description | Tools Used |
|---|---|---|
| Smart Grid Intrusion Detection | ML-based anomaly detection for energy networks | Python, Scikit-learn |
| IOC Extraction Tool | Automated threat intelligence parsing | Python |
| Secure File Upload API | Access-controlled backend system | Java Spring Boot |
| Bone Fracture Detection | Automated medical image analysis | MATLAB |

---

## What I'll Use This Repository For

This repository — **CFG-Assignments** — will store all my work for the 
CFG Foundation Module, including:

- Git & GitHub assignment (Assignment 1)
- Data Science notebooks
- Machine Learning projects
- Notes and resources

---

## Git Commands I Used in This Assignment

### Checking status
```bash
git status
```

### Creating a branch
```bash
git checkout -b feature/add-project-files
```

### Adding files to a branch
```bash
git add .
```

### Adding commits with meaningful messages
```bash
git commit -m "Add initial project files and README"
```

### Opening a pull request
> Done via GitHub UI — see screenshot below

### Merging to main branch
```bash
git checkout main
git merge feature/add-project-files
```

---

## 📸 Screenshots

*(Add your screenshots here as you go — see instructions below)*

---

##  About .gitignore

A `.gitignore` file tells Git which files and folders to **ignore** and 
**not track**. This is useful for:

- Keeping sensitive files (like API keys or passwords) out of GitHub
- Excluding large files that don't need version control
- Ignoring system files like `.DS_Store` on Mac

---

##  About requirements.txt

A `requirements.txt` file lists all the **Python packages and dependencies** 
needed to run the project. This allows anyone who clones the repository to 
install everything they need by running:
```bash
pip install -r requirements.txt
```

---

##  Community & Mentorship

Alongside my studies, I am the founder of:
-  **Creative Brains** — mentoring 100+ students in coding and cybersecurity
-  **Black Girls in Tech** — supporting women in technology across Africa 
and internationally

> *"If I made it, you can make it too."*

---
*Last updated: March 2026*
```

---

## Step 3 — Create Your Branch and Files

After saving the README, go to your repository and follow these steps:

**Create a new branch:**
1. Click the branch dropdown that says **"main"**
2. Type **feature/add-project-files**
3. Click **"Create branch"**

**Create .gitignore file:**
1. Make sure you are on your new branch
2. Click **"Add file"** → **"Create new file"**
3. Name it: `.gitignore`
4. Paste this content:
```
# Python
__pycache__/
*.py[cod]
*.env
.env

# Jupyter Notebooks
.ipynb_checkpoints

# System files
.DS_Store
Thumbs.db

# Virtual environments
venv/
env/
```
5. In the commit message box type: `Add .gitignore to exclude unnecessary files`
6. Select **"Commit directly to feature/add-project-files branch"**
7. Click **"Commit changes"**

**Create requirements.txt file:**
1. Click **"Add file"** → **"Create new file"**
2. Name it: `requirements.txt`
3. Paste this content:
```
# Python packages required for CFG Data Science & ML assignments
# Install all dependencies with: pip install -r requirements.txt

numpy
pandas
matplotlib
scikit-learn
jupyter
```
4. Commit message: `Add requirements.txt with core data science dependencies`
5. Commit to the **feature/add-project-files** branch

---

## Step 4 — Open a Pull Request

1. After committing, GitHub will show a yellow banner saying **"Compare & pull request"** — click it
2. Title: `Add project files: .gitignore and requirements.txt`
3. In the description write:
```
## What this PR adds
- .gitignore to exclude unnecessary and sensitive files from version control
- requirements.txt listing core Python dependencies for the course

## Why
Good practice for any Python/Data Science project to include these files 
from the start.

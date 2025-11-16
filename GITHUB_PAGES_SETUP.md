# GitHub Pages Deployment Guide

## Quick Start (5 minutes)

We've created a fully functional web interface that's ready for GitHub Pages deployment. Here's how to get it live:

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web Interface
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `esc-web` (or any name you prefer)
3. Description: "Elevator Service Companion - Via Series Diagnostics"
4. Make it **Public** (required for free GitHub Pages)
5. Click "Create repository"

### Option B: Using Git Command Line
```bash
cd /path/to/esc/web
git init
git add .
git commit -m "Initial ESC web interface release"
git remote add origin https://github.com/YOUR-USERNAME/esc-web.git
git branch -M main
git push -u origin main
```

---

## Step 2: Enable GitHub Pages

After creating the repository:

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Scroll down to **Pages** (left sidebar under "Code and automation")
4. Under "Build and deployment":
   - Source: Select **Deploy from a branch**
   - Branch: Select **main**
   - Folder: Select **/ (root)**
5. Click **Save**

GitHub will automatically build and deploy your site.

---

## Step 3: Access Your Live Website

After 1-2 minutes, your site will be available at:

```
https://pimpster82.github.io/esc-web/
```

For example:
- `https://git@github.com:pimpster82/esc-web`
- `https://elevator-pro.github.io/esc-web/`

---

## What Gets Deployed

The web folder contains:
- ✅ `index.html` - Interactive interface
- ✅ `knowledge.json` - 270 data entries
- ✅ `README.md` - Documentation

**No backend server needed** - everything runs in the browser!

---

## Testing Before Deployment

### Local Testing
```bash
cd /mnt/c/daniel_ai_playground/ESC/web

# Start a simple Python server
python3 -m http.server 8000

# Open in browser:
# http://localhost:8000
```

Then test:
1. Type "F01 02" → Should show error code details
2. Type "P0001" → Should show parameter info
3. Type "XTSS" → Should show component definition
4. Try example queries in the blue box

---

## Updating Content

### To add more data:
1. Update the JSON files in `data/via/v74/`
2. Regenerate `web/knowledge.json` using the Python script
3. Commit and push to GitHub

```bash
# Regenerate knowledge.json
python3 scripts/create_knowledge_base.py

# Push updates
git add web/knowledge.json
git commit -m "Update knowledge base with new data"
git push
```

### To change the interface:
1. Edit `web/index.html`
2. Commit and push
3. GitHub Pages automatically rebuilds

---

## Custom Domain (Optional)

Want a custom domain like `elevator-service.com`?

1. In Settings > Pages > Custom domain
2. Enter your domain: `elevator-service.com`
3. Add DNS records (GitHub will show you how)
4. Wait for verification (5-10 minutes)

---

## Troubleshooting

### "404 Not Found"
- Wait 2-3 minutes for GitHub to build
- Check Settings > Pages shows correct branch (main) and folder (/)
- Try hard refresh (Ctrl+Shift+R)

### "knowledge.json" not loading
- Make sure `knowledge.json` is in the `/web` folder
- File name is case-sensitive
- Run local test first to verify

### Changes not showing
- Clear browser cache (Ctrl+Shift+Delete)
- Wait 1-2 minutes for GitHub to rebuild
- Check that you pushed the changes: `git push`

---

## File Structure

After deployment, your GitHub Pages will serve:

```
esc-web/
├── index.html          ← Main interface
├── knowledge.json      ← 270 data entries
├── README.md           ← Documentation
└── .gitignore          ← (optional) exclude unnecessary files
```

---

## Advanced: Custom Configuration

### Create a `.gitignore` (optional)
```
venv/
*.pyc
__pycache__/
.DS_Store
extracted_raw/
manuals/
*.pdf
```

This keeps your repo clean on GitHub.

### Create a `.nojekyll` file (optional)
GitHub Pages uses Jekyll by default. If you want to disable it:
```bash
touch web/.nojekyll
git add web/.nojekyll
git commit -m "Disable Jekyll processing"
git push
```

---

## Success Checklist

✅ Repository created on GitHub
✅ GitHub Pages enabled in Settings
✅ Website is live at `https://username.github.io/esc-web/`
✅ Search works for error codes (F01 02)
✅ Search works for parameters (P0001)
✅ Search works for components (XTSS)
✅ All 270 data entries accessible

---

## What You Can Do Now

Your technicians can:
- 🔍 Search for error codes instantly
- 📚 Look up parameters by code
- 🔧 Find component definitions
- 📋 Get diagnostic guidance
- 💾 Works completely offline (data already loaded)

---

## Next Steps (Phase 3)

Ready for even more power? You can:
1. Add Claude API integration (intelligent Q&A)
2. Add case history tracking
3. Add German language support
4. Add mobile app version
5. Add voice input support

But for now, you have a **fully functional diagnostic tool** that technicians can use immediately!

---

## Questions?

- **Knowledge base question?** Check `web/knowledge.json`
- **Interface issue?** Edit `web/index.html`
- **Deployment issue?** Check GitHub Settings > Pages
- **New data?** Update `data/via/v74/*.json` and regenerate

---

**Status:** ✅ Ready to Deploy
**Estimated Time:** 5 minutes
**Cost:** FREE (GitHub Pages is free)
**Server:** No backend needed (static files only)

Deploy now and share the URL with your team! 🚀

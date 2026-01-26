# ⚡ El Dorado - 3-Step Deployment (EASIEST WAY)

**Get your site live in under 10 minutes using Vercel**

---

## 🚀 THE 3 STEPS

### **STEP 1: Push to GitHub** (5 minutes)

In terminal, inside `el-dorado-site` folder:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "El Dorado ready to launch"

# Create repo on GitHub.com first, then:
git remote add origin https://github.com/YOUR_USERNAME/el-dorado-ecommerce.git
git branch -M main
git push -u origin main
```

**Don't have GitHub?**
1. Go to github.com
2. Sign up (free)
3. Click "New Repository"
4. Name it: `el-dorado-ecommerce`
5. Copy the URL and use in command above

---

### **STEP 2: Connect to Vercel** (3 minutes)

1. Go to **vercel.com**
2. Click "Sign up" (use your GitHub account)
3. Click "Import Project"
4. Select your `el-dorado-ecommerce` repo
5. Click **"Deploy"**

That's it! Vercel automatically:
- Detects it's a Vite project
- Builds it
- Deploys it
- Gives you HTTPS
- Gives you a URL

---

### **STEP 3: Get Your Live URL** (instant)

After deployment (takes ~2 minutes), you'll get:

**Your Live Site:**
```
https://el-dorado-ecommerce.vercel.app
```

Or you can add a custom domain later (like `eldorado.com`)

---

## 🎯 THAT'S IT!

**Every time you update:**
1. Edit files
2. `git add .`
3. `git commit -m "update"`
4. `git push`
5. ✨ Automatically rebuilds and deploys!

No manual builds. No FTP. No uploading files.

---

## 📝 Before You Deploy

Make sure these are done:

**Required:**
- [ ] Product photos in `public/` folder
  - `product-pendant.jpg`
  - `product-chain.jpg`
  - `product-bracelet-1.jpg`
  - `product-bracelet-2.jpg`
  - `product-bracelet-3.jpg`
  - `product-bracelet-4.jpg`

**Optional (can add later):**
- [ ] Product descriptions in `src/main.js`
- [ ] Final prices confirmed
- [ ] Stripe payment links

---

## 🔄 Update Workflow (After First Deploy)

```bash
# 1. Make changes to your files

# 2. Save and commit
git add .
git commit -m "updated products"

# 3. Push
git push

# 4. Wait 2 minutes
# ✨ Site automatically updates!
```

---

## 🌐 Add Custom Domain (Optional)

If you want `eldorado.com` instead of `vercel.app`:

1. Buy domain (Namecheap, GoDaddy, etc.)
2. In Vercel dashboard → Settings → Domains
3. Add your domain
4. Update DNS (Vercel gives you exact instructions)
5. Done! (takes 5-30 minutes to propagate)

---

## ⚡ Why Vercel is Easiest

| Feature | Vercel | Hostinger |
|---------|--------|-----------|
| **Deploy** | 1 click | Upload files manually |
| **Updates** | Git push → auto deploy | Build + upload each time |
| **HTTPS** | Automatic | Manual setup |
| **Speed** | Global CDN | Single server |
| **Cost** | Free | $3-10/month |
| **Setup Time** | 5 minutes | 30+ minutes |

---

## 🆘 Quick Troubleshooting

**"Git not found"**
→ Install Git: git-scm.com/downloads

**"Build failed on Vercel"**
→ Check `package.json` has all dependencies
→ Run `npm install` locally to test

**"Images not showing"**
→ Make sure images are in `public/` folder
→ Push images to GitHub: `git add public/* && git commit -m "add images" && git push`

**"Want to test before deploying"**
→ Run `npm run dev` locally first

---

## ✅ Deployment Checklist

- [ ] Have GitHub account
- [ ] Product photos ready
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] Repository connected to Vercel
- [ ] Deployment successful
- [ ] Website loads at vercel.app URL
- [ ] All products showing
- [ ] Cart works
- [ ] Chatbot appears

---

## 🎊 You're Live!

**Total Time:** Under 10 minutes  
**Total Cost:** $0 (Vercel free tier)  
**Updates:** Automatic on every git push  
**HTTPS:** Included  
**Performance:** Global CDN  

**Your site:** `https://el-dorado-ecommerce.vercel.app`

Share it, start selling, make money! 💎🚀

---

*Simplest deployment ever. No build steps. No file uploads. Just push code and go live.*

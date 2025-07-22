# Streamlit Cloud Deployment Guide

## **Deploy TalentScout Hiring Assistant to Streamlit Cloud**

Your GitHub repository: **https://github.com/VineetSnegi/TalentScout-Hiring-Assistant**

---

## **Step-by-Step Deployment**

### **Step 1: Prepare Your Repository**

Make sure your GitHub repository has:
- ✅ `app.py` (main application file)
- ✅ `requirements.txt` (dependencies)
- ✅ `.env.example` (environment template)
- ✅ All source code in `src/` folder
- ✅ This README.md

### **Step 2: Deploy to Streamlit Cloud**

1. **Visit Streamlit Cloud**
   - Go to: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app"
   - Select "From existing repo"

3. **Configure Repository**
   - **Repository**: `VineetSnegi/TalentScout-Hiring-Assistant`
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
   - **App URL**: Choose a custom name like `talentscout-hiring-assistant`

4. **Add Secrets (IMPORTANT!)**
   - Click "Advanced settings"
   - In the "Secrets" section, add:
   ```toml
   GOOGLE_API_KEY = "your_actual_google_ai_api_key_here"
   ```

5. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for deployment

### **Step 3: Your Live App**

Once deployed, your app will be available at:
```
https://talentscout-hiring-assistant-[random-id].streamlit.app/
```

---

## **Configuration Requirements**

### **Environment Variables**
Your app needs these environment variables in Streamlit Cloud:

```toml
# In Streamlit Cloud Secrets
GOOGLE_API_KEY = "your_google_ai_api_key"
```

### **Google AI API Key Setup**
1. Go to: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key
4. Add it to Streamlit Cloud secrets

---

## **Deployment Commands**

### **If you need to update your repository:**

```bash
# Navigate to your project
cd "c:\Users\MyComputer\Desktop\AI Assignment"

# Initialize git (if not already done)
git init
git remote add origin https://github.com/VineetSnegi/TalentScout-Hiring-Assistant.git

# Add all files
git add .

# Commit changes
git commit -m "Complete TalentScout Hiring Assistant - Ready for deployment"

# Push to GitHub
git push -u origin main
```

### **For updates after initial deployment:**

```bash
# Make your changes, then:
git add .
git commit -m "Update: describe your changes"
git push origin main
```

*Streamlit Cloud will automatically redeploy when you push changes!*

---

## **Expected Deployment Results**

### **What you'll get:**
- **Live Application**: Fully functional hiring assistant
- **Custom URL**: Professional-looking app URL
- **Automatic Updates**: App updates when you push to GitHub
- **Free Hosting**: No cost for deployment
- **SSL Certificate**: Secure HTTPS connection

### **Performance:**
- **Fast Loading**: Optimized for quick startup
- **Auto-scaling**: Handles multiple users
- **Persistent Data**: Candidate data saved between sessions
- **Mobile Friendly**: Responsive design works on all devices

---

## **After Deployment**

### **Test Your Live App:**
1. Visit your Streamlit Cloud URL
2. Click "START MY INTERVIEW"
3. Complete a full interview flow
4. Check data is saved properly

### **Share Your Success:**
- **Email the URL** to demonstrate your project
- **Social Media**: Share your AI hiring assistant
- **Resume**: Add the live demo link
- **Assignment**: Submit the live URL

---

## **Troubleshooting**

### **Common Issues:**

**App won't start?**
- Check your `GOOGLE_API_KEY` in secrets
- Verify all files are in your GitHub repo
- Check the logs in Streamlit Cloud

**Import errors?**
- Ensure `requirements.txt` is complete
- Verify all source files are uploaded

**API not working?**
- Double-check your Google AI API key
- Ensure the key has proper permissions

---

## **Your Deployment Checklist**

- [ ] GitHub repository is updated with latest code
- [ ] Google AI API key is ready
- [ ] Streamlit Cloud account created
- [ ] App configured with correct repository path
- [ ] Secrets added (GOOGLE_API_KEY)
- [ ] App deployed successfully
- [ ] Live testing completed
- [ ] URL shared for demonstration

---

**Ready to deploy? Your TalentScout Hiring Assistant is about to go live!**

**Repository**: https://github.com/VineetSnegi/TalentScout-Hiring-Assistant
**Deployment Platform**: Streamlit Cloud
**Expected URL**: `https://talentscout-hiring-assistant-[id].streamlit.app/`

# Project Deployment Checklist

## 1. Setup & Initialization
- [ ] Initialize Git Repository (`git init`)
- [ ] Create GitHub Repository (`gh repo create`)
- [ ] Configure `.gitignore`

## 2. Local Emulation
- [ ] Configure `local.settings.json` / `.env`
- [ ] Start Local Emulators (Azurite, LocalStack, etc.)
- [ ] Verify Application Runs Locally

## 3. Cloud Deployment
- [ ] Login to Cloud CLI (`az login` / `aws configure`)
- [ ] Run Deployment Script
- [ ] Verify Resources in Cloud Console

## 4. Final Verification
- [ ] Test Live Endpoints
- [ ] Cleanup Resources (if applicable)

# GitHub login + Netlify auto-deploy setup

1. In Firebase Console, enable **Authentication > Sign-in method > GitHub**.
2. In GitHub, create an **OAuth App** with callback URL:
   `https://<your-firebase-auth-domain>/__/auth/handler`
3. Copy the OAuth app Client ID/Secret into the Firebase GitHub provider config.
4. Update `/assets/config/firebase.config.js` by setting `window.KN3AUX_FIREBASE_CONFIG` to your Firebase web config object.
5. In your GitHub repository secrets, add:
   - `NETLIFY_AUTH_TOKEN`
   - `NETLIFY_SITE_ID`
6. Connect the repository to Netlify (or create a site in Netlify), then pushes to the repository will trigger `.github/workflows/netlify-deploy.yml` and publish updates automatically.

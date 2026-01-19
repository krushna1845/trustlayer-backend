Deploying TrustLayer backend (quick guide)

Option A — Render (recommended quick deploy)
- Create a new Web Service on Render and connect your GitHub repo.
- Choose "Docker" as the environment (Render will use the `Dockerfile` in the repo root).
- Set the service port to `5000` (Render will respect EXPOSE).
- Add the following Environment Variables in Render dashboard (Settings -> Environment):
  - `DATABASE_URL` (if using production DB)
  - `ANTHROPIC_API_KEY`
  - `OPENAI_API_KEY`
  - `SECRET_KEY`
  - `FRONTEND_URL` = https://trustlayarai-three.vercel.app

Option B — Temporary tunnel (ngrok) for quick testing
- Install ngrok and run:
  - `ngrok http 5000`
- Copy the generated public URL (https://....ngrok.io)
- In your Vercel project, set Environment Variable `VITE_BASE_URL` to that URL and redeploy.

Vercel: set `VITE_BASE_URL`
- Go to your Vercel project -> Settings -> Environment Variables
- Add `VITE_BASE_URL` = `https://your-backend-url` (Render URL or ngrok URL)
- Redeploy the frontend

Local Docker test
- Build and run locally:
  - `docker build -t trustlayer-backend:local .`
  - `docker run -p 5000:5000 --env-file .env trustlayer-backend:local`

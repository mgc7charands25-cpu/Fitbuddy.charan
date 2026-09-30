# FitBuddy AI

FitBuddy is a lightweight fitness planner that generates personalized weekly workout plans using Google Gemini when an API key is configured. It also includes a deterministic fallback generator so the app works without any external service.

## Features

- Goal-driven plan generation
- Weekly workout schedule
- Recovery and nutrition notes
- Form-based user profile input
- Gemini-powered generation with graceful fallback

## Run locally

1. Create a virtual environment:
   python -m venv .venv
2. Activate it:
   - Windows: .venv\Scripts\activate
   - macOS/Linux: source .venv/bin/activate
3. Install dependencies:
   pip install -r requirements.txt
4. Copy environment settings:
   copy .env.example .env
5. Add your Gemini API key to .env if you want live AI generation.
6. Start the app:
   python app.py

The app will be available at http://localhost:5000

## Testing

pytest

import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover
    genai = None

load_dotenv()

app = Flask(__name__)


def build_fallback_plan(profile):
    goal = profile.get('goal', 'General fitness')
    experience = profile.get('experience', 'Beginner')
    days = int(profile.get('days', 4))
    train_type = profile.get('training_type', 'Balanced')

    days_map = {
        3: ['Mon', 'Wed', 'Fri'],
        4: ['Mon', 'Tue', 'Thu', 'Sat'],
        5: ['Mon', 'Tue', 'Thu', 'Fri', 'Sat'],
        6: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    }
    selected_days = days_map.get(days, ['Mon', 'Wed', 'Fri', 'Sat'])

    plan_lines = [
        f"AI Fitness Plan for {goal}",
        f"Experience level: {experience}",
        f"Training type: {train_type}",
        "",
        "Weekly structure:",
    ]

    for day in selected_days:
        plan_lines.append(f"- {day}: {train_type} strength + mobility block")

    plan_lines.extend([
        "",
        "Recovery guidance:",
        "- Sleep 7–9 hours nightly",
        "- Drink water consistently throughout the day",
        "- Keep one active recovery day per week",
        "",
        "Nutrition note:",
        "- Prioritize protein, complex carbs, and vegetables",
        "- Eat a balanced meal 1–2 hours before training",
        "- Hydrate after sessions and include post-workout recovery nutrition",
    ])
    return "\n".join(plan_lines)


def generate_plan_with_gemini(profile):
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or genai is None:
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    Create a personalized weekly fitness plan.
    User profile:
    - Goal: {profile.get('goal', 'General fitness')}
    - Experience: {profile.get('experience', 'Beginner')}
    - Days per week: {profile.get('days', 4)}
    - Training type: {profile.get('training_type', 'Balanced')}
    - Focus area: {profile.get('focus', 'Overall conditioning')}
    - Availability: {profile.get('availability', '45–60 min per session')}
    - Age: {profile.get('age', 30)}
    - Sex: {profile.get('sex', 'Prefer not to say')}

    Return a clear and motivating weekly plan with day-by-day schedule, recovery notes, and nutrition guidance.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return None


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None

    if request.method == 'POST':
        profile = {
            'goal': request.form.get('goal', 'General fitness'),
            'experience': request.form.get('experience', 'Beginner'),
            'days': request.form.get('days', 4),
            'training_type': request.form.get('training_type', 'Balanced'),
            'focus': request.form.get('focus', 'Overall conditioning'),
            'availability': request.form.get('availability', '45–60 min per session'),
            'age': request.form.get('age', 30),
            'sex': request.form.get('sex', 'Prefer not to say'),
        }

        ai_plan = generate_plan_with_gemini(profile)
        if ai_plan:
            result = ai_plan
        else:
            result = build_fallback_plan(profile)
            error = 'Gemini was not available, so a local fallback plan was generated instead.'

    return render_template('index.html', result=result, error=error)


if __name__ == '__main__':
    app.run(debug=True)

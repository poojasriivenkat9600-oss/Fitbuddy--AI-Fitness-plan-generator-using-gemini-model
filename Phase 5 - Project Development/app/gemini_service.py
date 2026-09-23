 `app/gemini_service.py`:

```python
"""Gemini AI service — generates workout plans, nutrition tips, and plan updates."""

import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.google_api_key)

_pro_model = genai.GenerativeModel(settings.model_pro)
_flash_model = genai.GenerativeModel(settings.model_flash)


def generate_workout_plan(
    name: str, age: int, weight: str, goal: str, intensity: str
) -> str:
    """Use Gemini 1.5 Pro to generate a structured 7-day workout plan."""

    prompt = f"""
You are a certified personal trainer. Create a detailed, structured 7-day workout
plan for the following person. Use a clear day-by-day format with exercise names,
sets, reps, and rest periods.

User Profile:
- Name: {name}
- Age: {age}
- Weight: {weight}
- Goal: {goal}
- Intensity Level: {intensity}

Return the plan in clean markdown with a heading for each day (Day 1 through Day 7).
Keep it practical and actionable. Include a brief warm-up and cool-down for each day.
"""
    response = _pro_model.generate_content(prompt)
    return response.text.strip()


def generate_nutrition_tips(goal: str, weight: str, intensity: str) -> str:
    """Use Gemini 1.5 Flash to generate practical nutrition / dietary tips."""

    prompt = f"""
You are a sports nutritionist. Provide practical, easy-to-follow nutrition and
dietary tips tailored to this person's profile.

Profile:
- Goal: {goal}
- Weight: {weight}
- Intensity Level: {intensity}

Return 8-10 practical tips in clean markdown bullet points. Include:
- Daily calorie guidance (rough range)
- Macronutrient breakdown suggestions
- Pre-workout and post-workout meal ideas
- Hydration advice
- 2-3 sample meal ideas
Keep it concise and actionable. No medical disclaimers needed.
"""
    response = _flash_model.generate_content(prompt)
    return response.text.strip()


def update_workout_plan(current_plan: str, feedback: str) -> str:
    """Use Gemini 1.5 Pro to revise an existing plan based on user feedback."""

    prompt = f"""
You are a certified personal trainer. A user wants to update their current workout
plan based on the feedback below. Modify the plan accordingly while keeping the
7-day structure intact.

Current Workout Plan:
{current_plan}

User Feedback / Request:
{feedback}

Return the FULL updated 7-day plan in clean markdown with the same day-by-day
format. Incorporate the user's request naturally into the plan.
"""
    response = _pro_model.generate_content(prompt)
    return response.text.strip()
```

This file handles all three Gemini AI calls: `generate_workout_plan` uses Gemini 1.5 Pro to create the 7-day workout, `generate_nutrition_tips` uses Gemini 1.5 Flash for diet advice, and `update_workout_plan` uses Pro again for the feedback loop to revise an existing plan. Let me know which file you'd like next.
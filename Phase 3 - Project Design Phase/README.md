# Phase 3: Project Design Phase

## Technical Architecture Overview
The architecture is designed as a secure, fast, and fully local web application powered by **FastAPI** and **Google Gemini AI**.

1. **User Interface (Frontend):** Responsive HTML5, CSS3, and Jinja2 templates for gathering inputs and presenting the 7-day plans.
2. **Backend Server (FastAPI):** Controls routing logic, handles form submissions, communicates with Gemini APIs, and queries the database.
3. **AI Core Service:** Connects to Gemini 1.5 Pro (Workout generation & feedback cycles) and Gemini 1.5 Flash (Nutrition updates).
4. **Data Management:** SQLite database layered with SQLAlchemy ORM to track user profiles and historical workout records.

## Database Schema Model
* **Users Table:** Columns include `id`, `user_id`, `username`, `age`, `weight`, `goal`, and `intensity`.
* **Workout Plans Table:** Columns include `id`, `user_id`, `original_plan`, `updated_plan`, and `nutrition_tip`.

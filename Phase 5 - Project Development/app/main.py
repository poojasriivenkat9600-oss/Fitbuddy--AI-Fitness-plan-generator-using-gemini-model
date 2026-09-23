`app/main.py`:

```python
"""FastAPI application — FitBuddy AI Fitness Plan Generator."""

import markdown
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import init_db, get_db, User
from app.schemas import UserCreate, FeedbackRequest
from app.gemini_service import (
    generate_workout_plan,
    generate_nutrition_tips,
    update_workout_plan,
)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="FitBuddy — AI Fitness Plan Generator")

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Jinja2 filter: render markdown to safe HTML
templates.env.filters["markdown"] = lambda text: markdown.markdown(
    text, extensions=["tables", "fenced_code"]
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


# ── Pages ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.desc()).all()
    return templates.TemplateResponse(
        request, "all_users.html", {"users": users}
    )


# ── API: Generate plan ─────────────────────────────────────────────────────

@app.post("/generate")
def generate_plan(user: UserCreate, db: Session = Depends(get_db)):
    try:
        workout = generate_workout_plan(
            user.name, user.age, user.weight, user.goal, user.intensity
        )
        nutrition = generate_nutrition_tips(user.goal, user.weight, user.intensity)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API error: {exc}. Check your GOOGLE_API_KEY in .env.",
        )

    db_user = User(
        name=user.name,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity,
        workout_plan=workout,
        nutrition_tips=nutrition,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return RedirectResponse(url=f"/result/{db_user.id}", status_code=303)


@app.get("/result/{user_id}", response_class=HTMLResponse)
def result(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        request, "result.html", {"user": user}
    )


# ── API: Feedback loop ─────────────────────────────────────────────────────

@app.post("/feedback")
def feedback(req: FeedbackRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.workout_plan:
        raise HTTPException(status_code=400, detail="No existing plan to update.")

    try:
        updated = update_workout_plan(user.workout_plan, req.feedback)
    except Exception as exc:
        raise HTTPException(
            status_code=502, detail=f"Gemini API error: {exc}"
        )

    user.workout_plan = updated
    db.commit()

    return RedirectResponse(url=f"/result/{user.id}", status_code=303)


# ── API: Delete user (admin) ───────────────────────────────────────────────

@app.post("/delete-user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return RedirectResponse(url="/view-all-users", status_code=303)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

That is the complete, exact contents of `app/main.py`. It contains all five routes: the landing page form, the plan generation endpoint that calls Gemini, the result page, the feedback loop for updating plans, and the admin delete-user action. Let me know if you'd like the other files' full code as well.
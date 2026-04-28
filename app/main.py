from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from app.agent import analyze_code
from app.database import init_db, create_default_admin, verify_user, create_user

load_dotenv()

app = FastAPI(title="Mentor Clean Code API")


@app.on_event("startup")
def startup_event():
    init_db()
    create_default_admin()


class CodeRequest(BaseModel):
    code: str
    language: str = "python"
    mode: str = "Clean Code"


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(request: LoginRequest):
    if not request.username.strip() or not request.password.strip():
        raise HTTPException(
            status_code=400,
            detail="Nom d'utilisateur et mot de passe obligatoires."
        )

    is_valid = verify_user(request.username, request.password)

    if not is_valid:
        raise HTTPException(
            status_code=401,
            detail="Nom d'utilisateur ou mot de passe incorrect."
        )

    return {
        "message": "Connexion réussie",
        "username": request.username
    }


@app.post("/register")
def register(request: RegisterRequest):
    username = request.username.strip()
    password = request.password.strip()

    if not username or not password:
        raise HTTPException(
            status_code=400,
            detail="Nom d'utilisateur et mot de passe obligatoires."
        )

    if len(password) < 4:
        raise HTTPException(
            status_code=400,
            detail="Le mot de passe doit contenir au moins 4 caractères."
        )

    created = create_user(username, password)

    if not created:
        raise HTTPException(
            status_code=400,
            detail="Ce nom d'utilisateur existe déjà."
        )

    return {
        "message": "Utilisateur créé avec succès",
        "username": username
    }


@app.post("/analyze")
def analyze(request: CodeRequest):
    try:
        result = analyze_code(
            code=request.code,
            language=request.language,
            mode=request.mode
        )

        return {
            "language": request.language,
            "mode": request.mode,
            "analysis": result
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur serveur : {str(error)}"
        )
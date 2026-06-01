from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth_routes import router as auth_router
from routes.municipality_routes import router as municipality_router
from routes.suspension_routes import router as suspension_router
from routes.weather_routes import router as weather_router
from middlewares.rate_limit_middleware import rate_limit_middleware

app = FastAPI(
    title="SafeClass API",
    description="API que determina si se deben suspender actividades escolares basándose en el clima.",
    version="1.0.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar middlewares
app.middleware("http")(rate_limit_middleware)

# Registrar routers

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(municipality_router, prefix="/municipios", tags=["Municipios"])
app.include_router(suspension_router, prefix="/suspensions", tags=["Suspensions"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"]) 


@app.get("/", tags=["Root"])
def root():
    return {"message": "SafeClass API is running!"}

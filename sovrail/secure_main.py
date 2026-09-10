from .main import app
from .assurance import router as assurance_router

# Additive security/assurance layer. Existing SOVRAIL routes remain unchanged.
app.include_router(assurance_router)

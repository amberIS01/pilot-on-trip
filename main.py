from fastapi import FastAPI
from routers import user, location, vehicle, partner, service, dashboard

app = FastAPI()
app.include_router(user.router)
app.include_router(location.router)
app.include_router(vehicle.router)
app.include_router(partner.router)
app.include_router(service.router)
app.include_router(dashboard.router)
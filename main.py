from fastapi import FastAPI
from routers import user, location, vehicle, partner, service, dashboard, partner_query, customer_support, rider, booking, payment, user_profile, chatbot

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Welcome"}

app.include_router(user.router)
app.include_router(location.router)
app.include_router(vehicle.router)
app.include_router(partner.router)
app.include_router(service.router)
app.include_router(dashboard.router)
app.include_router(partner_query.router)
app.include_router(customer_support.router)
app.include_router(rider.router)
app.include_router(booking.router)
app.include_router(payment.router)
app.include_router(user_profile.router)
app.include_router(chatbot.router)
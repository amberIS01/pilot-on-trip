from databases.database import engine, Base
from models import user_model, partner_model, vehicle_model, customer_support_model, location_model, service_model, dashboard_model, partner_query_model, rider_model, booking_model, payment_model

Base.metadata.create_all(bind=engine)
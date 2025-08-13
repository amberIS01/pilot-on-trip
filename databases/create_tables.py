
from databases.database import engine, Base
from models import user_model, partner_model, vehicle_model, customer_support_model, location_model, service_model, partner_query_model, rider_model, booking_model, payment_model
from models import customer_dashboard_model, admin_dashboard_model, rider_dashboard_model, feedback_model, feedback_center_model

Base.metadata.create_all(bind=engine)
"""
Initialize pricing data in the database
Run this script once to seed the pricing table with default values
"""
from app import app
from models import db, PricingPlan
import json

def init_pricing():
    with app.app_context():
        # Check if pricing data already exists
        existing = PricingPlan.query.first()
        if existing:
            print("Pricing data already exists. Skipping initialization.")
            return
        
        # Define pricing plans
        plans = [
            {
                'plan_name': 'Starter',
                'base_price': 62.0,
                'current_price': 62.0,
                'discount_percent': 0,
                'features': json.dumps([
                    'Basic AI WhatsApp automation',
                    'Auto-replies',
                    'Basic lead capture',
                    'Email support',
                    '1 Connected Number'
                ]),
                'is_featured': False,
                'checkout_url': 'https://chariow.com/checkout/placeholder-starter'
            },
            {
                'plan_name': 'Pro',
                'base_price': 125.0,
                'current_price': 125.0,
                'discount_percent': 0,
                'features': json.dumps([
                    'Everything in Starter',
                    'Lead qualification',
                    'Appointment scheduling',
                    'Multi-agent support',
                    'Priority support'
                ]),
                'is_featured': True,
                'checkout_url': 'https://chariow.com/checkout/placeholder-pro'
            },
            {
                'plan_name': 'Business',
                'base_price': 499.0,
                'current_price': 499.0,
                'discount_percent': 0,
                'features': json.dumps([
                    'Everything in Pro',
                    'Full funnel setup',
                    'Custom tone training',
                    'Unlimited contacts',
                    'Dedicated account rep'
                ]),
                'is_featured': False,
                'checkout_url': 'https://chariow.com/checkout/placeholder-business'
            }
        ]
        
        # Add plans to database
        for plan_data in plans:
            plan = PricingPlan(**plan_data)
            db.session.add(plan)
        
        db.session.commit()
        print("✓ Pricing data initialized successfully!")
        print(f"  - Created {len(plans)} pricing plans")
        
        # Display created plans
        for plan in PricingPlan.query.all():
            print(f"  - {plan.plan_name}: ${plan.current_price}/month")

if __name__ == '__main__':
    init_pricing()

#!/usr/bin/env python3
"""
Add sample resources to the database for testing
"""

from app import app
from models import db, Resource, ResourceTransaction
from datetime import datetime, date, timedelta
import random

def add_sample_resources():
    """Add sample resources to the database"""
    
    sample_resources = [
        # Medicines
        {
            'name': 'Paracetamol 500mg',
            'category': 'Medicine',
            'description': 'Common pain reliever and fever reducer',
            'current_stock': 150,
            'minimum_stock': 50,
            'maximum_stock': 500,
            'unit': 'tablets',
            'location': 'Pharmacy',
            'supplier': 'MedCorp Pharmaceuticals',
            'cost_per_unit': 0.50,
            'expiry_date': date.today() + timedelta(days=365)
        },
        {
            'name': 'Amoxicillin 250mg',
            'category': 'Medicine',
            'description': 'Antibiotic for bacterial infections',
            'current_stock': 25,
            'minimum_stock': 100,
            'maximum_stock': 300,
            'unit': 'capsules',
            'location': 'Pharmacy',
            'supplier': 'BioPharm Inc',
            'cost_per_unit': 1.20,
            'expiry_date': date.today() + timedelta(days=180)
        },
        {
            'name': 'Ibuprofen 400mg',
            'category': 'Medicine',
            'description': 'Anti-inflammatory medication',
            'current_stock': 75,
            'minimum_stock': 40,
            'maximum_stock': 200,
            'unit': 'tablets',
            'location': 'Pharmacy',
            'supplier': 'HealthSupply Co',
            'cost_per_unit': 0.75,
            'expiry_date': date.today() + timedelta(days=400)
        },
        {
            'name': 'Insulin 10ml',
            'category': 'Medicine',
            'description': 'Diabetes medication',
            'current_stock': 8,
            'minimum_stock': 20,
            'maximum_stock': 50,
            'unit': 'vials',
            'location': 'Refrigerated Storage',
            'supplier': 'DiabeticCare Ltd',
            'cost_per_unit': 45.00,
            'expiry_date': date.today() + timedelta(days=90)
        },
        {
            'name': 'Saline Solution 500ml',
            'category': 'Medicine',
            'description': 'IV fluid for hydration',
            'current_stock': 45,
            'minimum_stock': 30,
            'maximum_stock': 100,
            'unit': 'bags',
            'location': 'Emergency Room',
            'supplier': 'Fluid Dynamics',
            'cost_per_unit': 3.50,
            'expiry_date': date.today() + timedelta(days=720)
        },
        
        # Equipment
        {
            'name': 'Blood Pressure Monitor',
            'category': 'Equipment',
            'description': 'Digital blood pressure monitoring device',
            'current_stock': 12,
            'minimum_stock': 5,
            'maximum_stock': 20,
            'unit': 'units',
            'location': 'Ward A',
            'supplier': 'MedTech Solutions',
            'cost_per_unit': 89.99
        },
        {
            'name': 'Thermometer Digital',
            'category': 'Equipment',
            'description': 'Digital thermometer for temperature measurement',
            'current_stock': 3,
            'minimum_stock': 10,
            'maximum_stock': 25,
            'unit': 'units',
            'location': 'Emergency Room',
            'supplier': 'TempTech',
            'cost_per_unit': 15.50
        },
        {
            'name': 'Wheelchair Standard',
            'category': 'Equipment',
            'description': 'Standard wheelchair for patient transport',
            'current_stock': 8,
            'minimum_stock': 4,
            'maximum_stock': 15,
            'unit': 'units',
            'location': 'Main Entrance',
            'supplier': 'MobilityAids Corp',
            'cost_per_unit': 250.00
        },
        {
            'name': 'Oxygen Cylinder',
            'category': 'Equipment',
            'description': 'Portable oxygen cylinder for respiratory support',
            'current_stock': 6,
            'minimum_stock': 8,
            'maximum_stock': 20,
            'unit': 'cylinders',
            'location': 'Emergency Room',
            'supplier': 'O2 Supplies',
            'cost_per_unit': 180.00
        },
        {
            'name': 'Syringe 5ml',
            'category': 'Equipment',
            'description': 'Disposable syringes for injections',
            'current_stock': 200,
            'minimum_stock': 150,
            'maximum_stock': 500,
            'unit': 'pieces',
            'location': 'Treatment Room',
            'supplier': 'InjectAids Inc',
            'cost_per_unit': 0.25
        },
        
        # Supplies
        {
            'name': 'Face Masks Surgical',
            'category': 'Supplies',
            'description': 'Disposable surgical face masks',
            'current_stock': 450,
            'minimum_stock': 200,
            'maximum_stock': 1000,
            'unit': 'boxes',
            'location': 'Supply Room',
            'supplier': 'ProtectiveGear Ltd',
            'cost_per_unit': 12.50
        },
        {
            'name': 'Gloves Latex',
            'category': 'Supplies',
            'description': 'Disposable latex examination gloves',
            'current_stock': 15,
            'minimum_stock': 50,
            'maximum_stock': 100,
            'unit': 'boxes',
            'location': 'All Departments',
            'supplier': 'GlovePro',
            'cost_per_unit': 8.75
        },
        {
            'name': 'Alcohol Swabs',
            'category': 'Supplies',
            'description': 'Alcohol prep pads for disinfection',
            'current_stock': 800,
            'minimum_stock': 500,
            'maximum_stock': 2000,
            'unit': 'pieces',
            'location': 'Treatment Room',
            'supplier': 'CleanMed Supplies',
            'cost_per_unit': 0.05
        },
        {
            'name': 'Bandage Roll',
            'category': 'Supplies',
            'description': 'Elastic bandage rolls for wound dressing',
            'current_stock': 120,
            'minimum_stock': 40,
            'maximum_stock': 200,
            'unit': 'rolls',
            'location': 'Emergency Room',
            'supplier': 'WoundCare Inc',
            'cost_per_unit': 3.25
        },
        {
            'name': 'Cotton Balls',
            'category': 'Supplies',
            'description': 'Sterile cotton balls for medical use',
            'current_stock': 35,
            'minimum_stock': 60,
            'maximum_stock': 150,
            'unit': 'bags',
            'location': 'Pharmacy',
            'supplier': 'SterileSupplies Co',
            'cost_per_unit': 2.50
        }
    ]
    
    with app.app_context():
        # Check if resources already exist
        existing_resources = Resource.query.count()
        if existing_resources > 0:
            print(f"Database already has {existing_resources} resources.")
            return
        
        # Add sample resources
        for resource_data in sample_resources:
            resource = Resource(**resource_data)
            
            # Update status based on stock levels
            if resource.current_stock == 0:
                resource.status = 'Out of Stock'
            elif resource.current_stock <= resource.minimum_stock:
                resource.status = 'Low Stock'
            else:
                resource.status = 'Available'
            
            db.session.add(resource)
        
        db.session.commit()
        
        # Create some sample transactions
        resources = Resource.query.all()
        for resource in resources[:10]:  # Create transactions for first 10 resources
            # Create a few historical transactions
            for i in range(3):
                transaction_types = ['Stock In', 'Used', 'Stock Out']
                transaction_type = random.choice(transaction_types)
                
                if transaction_type == 'Stock In':
                    quantity = random.randint(10, 50)
                    remaining = resource.current_stock + quantity
                else:
                    quantity = random.randint(1, min(20, resource.current_stock))
                    remaining = max(0, resource.current_stock - quantity)
                
                transaction = ResourceTransaction(
                    resource_id=resource.resource_id,
                    transaction_type=transaction_type,
                    quantity=quantity,
                    remaining_stock=remaining,
                    reason=f'Sample transaction {i+1}',
                    performed_by='System',
                    transaction_date=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.session.add(transaction)
        
        db.session.commit()
        
        print(f"Successfully added {len(sample_resources)} sample resources to database!")
        
        # Show resource summary
        medicines = Resource.query.filter_by(category='Medicine').count()
        equipment = Resource.query.filter_by(category='Equipment').count()
        supplies = Resource.query.filter_by(category='Supplies').count()
        low_stock = Resource.query.filter(Resource.current_stock <= Resource.minimum_stock).count()
        out_of_stock = Resource.query.filter_by(current_stock=0).count()
        
        print(f"\nResource Summary:")
        print(f"- Medicines: {medicines}")
        print(f"- Equipment: {equipment}")
        print(f"- Supplies: {supplies}")
        print(f"- Low Stock: {low_stock}")
        print(f"- Out of Stock: {out_of_stock}")

if __name__ == '__main__':
    add_sample_resources()

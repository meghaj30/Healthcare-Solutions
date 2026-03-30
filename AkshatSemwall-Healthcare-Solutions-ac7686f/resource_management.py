from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Resource, ResourceTransaction
from datetime import datetime, date, timedelta
import sqlalchemy as sa

resource_bp = Blueprint('resource', __name__)

@resource_bp.route('/resource_dashboard')
def resource_dashboard():
    """Main resource availability dashboard"""
    # Get all resources
    resources = Resource.query.order_by(Resource.category, Resource.name).all()
    
    # Calculate statistics
    total_resources = len(resources)
    low_stock_resources = [r for r in resources if r.current_stock <= r.minimum_stock]
    out_of_stock_resources = [r for r in resources if r.current_stock == 0]
    expired_resources = [r for r in resources if r.expiry_date and r.expiry_date <= date.today()]
    
    # Categorize resources
    medicines = [r for r in resources if r.category == 'Medicine']
    equipment = [r for r in resources if r.category == 'Equipment']
    supplies = [r for r in resources if r.category == 'Supplies']
    
    # Recent transactions
    recent_transactions = ResourceTransaction.query.order_by(ResourceTransaction.transaction_date.desc()).limit(10).all()
    
    # Critical items (need immediate attention)
    critical_items = []
    for resource in resources:
        if resource.current_stock == 0:
            critical_items.append({'resource': resource, 'priority': 'Critical', 'message': 'Out of Stock'})
        elif resource.current_stock <= resource.minimum_stock * 0.5:
            critical_items.append({'resource': resource, 'priority': 'High', 'message': 'Very Low Stock'})
        elif resource.current_stock <= resource.minimum_stock:
            critical_items.append({'resource': resource, 'priority': 'Medium', 'message': 'Low Stock'})
        elif resource.expiry_date and resource.expiry_date <= date.today() + timedelta(days=30):
            critical_items.append({'resource': resource, 'priority': 'High', 'message': 'Expiring Soon'})
    
    # Sort by priority
    priority_order = {'Critical': 1, 'High': 2, 'Medium': 3}
    critical_items.sort(key=lambda x: priority_order.get(x['priority'], 4))
    
    return render_template('resource_dashboard.html',
                         resources=resources,
                         medicines=medicines,
                         equipment=equipment,
                         supplies=supplies,
                         total_resources=total_resources,
                         low_stock_count=len(low_stock_resources),
                         out_of_stock_count=len(out_of_stock_resources),
                         expired_count=len(expired_resources),
                         critical_items=critical_items,
                         recent_transactions=recent_transactions,
                         today=date.today(),
                         timedelta=timedelta)

@resource_bp.route('/add_resource', methods=['GET', 'POST'])
def add_resource():
    """Add new resource to inventory"""
    if request.method == 'POST':
        try:
            resource = Resource(
                name=request.form.get('name'),
                category=request.form.get('category'),
                description=request.form.get('description'),
                current_stock=int(request.form.get('current_stock')),
                minimum_stock=int(request.form.get('minimum_stock')),
                maximum_stock=int(request.form.get('maximum_stock')),
                unit=request.form.get('unit'),
                location=request.form.get('location'),
                supplier=request.form.get('supplier'),
                cost_per_unit=float(request.form.get('cost_per_unit', 0)),
                expiry_date=datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d').date() if request.form.get('expiry_date') else None
            )
            
            # Update status based on stock levels
            if resource.current_stock == 0:
                resource.status = 'Out of Stock'
            elif resource.current_stock <= resource.minimum_stock:
                resource.status = 'Low Stock'
            else:
                resource.status = 'Available'
            
            db.session.add(resource)
            db.session.commit()
            
            # Create initial transaction record
            transaction = ResourceTransaction(
                resource_id=resource.resource_id,
                transaction_type='Stock In',
                quantity=resource.current_stock,
                remaining_stock=resource.current_stock,
                reason='Initial inventory setup',
                performed_by='System'
            )
            db.session.add(transaction)
            db.session.commit()
            
            flash('Resource added successfully!', 'success')
            return redirect(url_for('resource.resource_dashboard'))
            
        except Exception as e:
            flash(f'Error adding resource: {str(e)}', 'error')
            return redirect(url_for('resource.add_resource'))
    
    return render_template('add_resource.html')

@resource_bp.route('/update_stock/<int:resource_id>', methods=['POST'])
def update_stock(resource_id):
    """Update resource stock levels"""
    try:
        resource = Resource.query.get_or_404(resource_id)
        transaction_type = request.form.get('transaction_type')
        quantity = int(request.form.get('quantity'))
        reason = request.form.get('reason')
        performed_by = request.form.get('performed_by', 'Unknown')
        
        # Update stock based on transaction type
        if transaction_type == 'Stock In':
            resource.current_stock += quantity
        elif transaction_type == 'Stock Out':
            resource.current_stock -= quantity
        elif transaction_type == 'Used':
            resource.current_stock -= quantity
        
        # Ensure stock doesn't go negative
        if resource.current_stock < 0:
            resource.current_stock = 0
        
        # Update status
        if resource.current_stock == 0:
            resource.status = 'Out of Stock'
        elif resource.current_stock <= resource.minimum_stock:
            resource.status = 'Low Stock'
        else:
            resource.status = 'Available'
        
        resource.last_restocked = datetime.utcnow()
        resource.updated_at = datetime.utcnow()
        
        # Create transaction record
        transaction = ResourceTransaction(
            resource_id=resource.resource_id,
            transaction_type=transaction_type,
            quantity=quantity,
            remaining_stock=resource.current_stock,
            reason=reason,
            performed_by=performed_by
        )
        db.session.add(transaction)
        db.session.commit()
        
        flash(f'Stock updated successfully!', 'success')
        return redirect(url_for('resource.resource_dashboard'))
        
    except Exception as e:
        flash(f'Error updating stock: {str(e)}', 'error')
        return redirect(url_for('resource.resource_dashboard'))

@resource_bp.route('/resource_details/<int:resource_id>')
def resource_details(resource_id):
    """View detailed resource information"""
    resource = Resource.query.get_or_404(resource_id)
    transactions = ResourceTransaction.query.filter_by(resource_id=resource_id)\
                                        .order_by(ResourceTransaction.transaction_date.desc()).all()
    
    # Calculate stock trend
    stock_levels = [t.remaining_stock for t in transactions[:10]]  # Last 10 transactions
    stock_levels.reverse()  # Show chronological order
    
    return render_template('resource_details.html',
                         resource=resource,
                         transactions=transactions,
                         stock_levels=stock_levels,
                         today=date.today(),
                         timedelta=timedelta)

@resource_bp.route('/get_stock_alerts')
def get_stock_alerts():
    """AJAX endpoint to get current stock alerts"""
    critical_resources = []
    
    for resource in Resource.query.all():
        alert = None
        
        if resource.current_stock == 0:
            alert = {
                'type': 'danger',
                'message': f'{resource.name} is OUT OF STOCK!',
                'resource_id': resource.resource_id,
                'priority': 'Critical'
            }
        elif resource.current_stock <= resource.minimum_stock * 0.5:
            alert = {
                'type': 'warning',
                'message': f'{resource.name} has VERY LOW stock ({resource.current_stock} {resource.unit})',
                'resource_id': resource.resource_id,
                'priority': 'High'
            }
        elif resource.current_stock <= resource.minimum_stock:
            alert = {
                'type': 'info',
                'message': f'{resource.name} has LOW stock ({resource.current_stock} {resource.unit})',
                'resource_id': resource.resource_id,
                'priority': 'Medium'
            }
        elif resource.expiry_date and resource.expiry_date <= date.today() + timedelta(days=30):
            days_to_expiry = (resource.expiry_date - date.today()).days
            alert = {
                'type': 'warning',
                'message': f'{resource.name} expires in {days_to_expiry} days',
                'resource_id': resource.resource_id,
                'priority': 'High'
            }
        
        if alert:
            critical_resources.append(alert)
    
    return jsonify({
        'status': 'success',
        'alerts': critical_resources,
        'total_alerts': len(critical_resources)
    })

@resource_bp.route('/delete_resource/<int:resource_id>', methods=['POST'])
def delete_resource(resource_id):
    """Delete a resource from inventory"""
    try:
        resource = Resource.query.get_or_404(resource_id)
        
        # Delete related transactions first
        ResourceTransaction.query.filter_by(resource_id=resource_id).delete()
        
        # Delete the resource
        db.session.delete(resource)
        db.session.commit()
        
        flash('Resource deleted successfully!', 'success')
        return redirect(url_for('resource.resource_dashboard'))
        
    except Exception as e:
        flash(f'Error deleting resource: {str(e)}', 'error')
        return redirect(url_for('resource.resource_dashboard'))

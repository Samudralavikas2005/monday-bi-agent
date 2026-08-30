import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Generate Deal Funnel Data
deals = []
sectors = ['Energy', 'Technology', 'Healthcare', 'Finance', 'Retail']
stages = ['Lead', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
statuses = ['Active', 'On Hold', 'Completed', 'Cancelled']

for i in range(1, 26):
    deal_name = f"Deal {1000 + i}"
    sector = random.choice(sectors)
    stage = random.choice(stages)
    status = 'Completed' if stage in ['Closed Won', 'Closed Lost'] else random.choice(['Active', 'On Hold'])
    revenue = f"${random.randint(10, 500) * 1000},00"
    created_date = datetime.now() - timedelta(days=random.randint(30, 365))
    close_date = created_date + timedelta(days=random.randint(15, 120)) if stage == 'Closed Won' else None
    
    deals.append({
        'Deal Name': deal_name,
        'Sector': sector,
        'Stage': stage,
        'Status': status,
        'Revenue': revenue,
        'Created At': created_date.strftime('%Y-%m-%d'),
        'Close Date': close_date.strftime('%Y-%m-%d') if close_date else ''
    })

df_deals = pd.DataFrame(deals)
df_deals.to_csv('Deal_Funnel_Data.csv', index=False)

# Generate Work Order Data
work_orders = []
priorities = ['High', 'Medium', 'Low']
types = ['Installation', 'Maintenance', 'Consulting', 'Support']

for i in range(1, 41):
    wo_name = f"WO-{5000 + i}"
    deal_ref = random.choice(deals)['Deal Name']
    wo_type = random.choice(types)
    priority = random.choice(priorities)
    status = random.choice(['Pending', 'In Progress', 'Completed', 'Blocked'])
    hours = f"{random.randint(5, 40)} hrs"
    cost = f"${random.randint(1, 15) * 100}"
    due_date = (datetime.now() + timedelta(days=random.randint(-15, 60))).strftime('%Y-%m-%d')

    work_orders.append({
        'Work Order Name': wo_name,
        'Associated Deal': deal_ref,
        'Type': wo_type,
        'Priority': priority,
        'Status': status,
        'Estimated Hours': hours,
        'Cost': cost,
        'Due Date': due_date
    })

df_wo = pd.DataFrame(work_orders)
df_wo.to_csv('Work_Order_Tracker_Data.csv', index=False)

print("Sample data generated successfully!")

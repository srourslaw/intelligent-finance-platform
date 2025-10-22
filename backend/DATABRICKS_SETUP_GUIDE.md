# Databricks Setup Guide

## Quick Start (Testing in Demo Mode - No Setup Required!)

The Databricks integration is **already working in DEMO MODE** with realistic sample data!

1. Start your backend: `python3 -m uvicorn app.main:app --reload`
2. Open the dashboard: http://localhost:5173
3. Click the "AI Insights" tab
4. You'll see predictions, anomalies, and cash flow forecasts!

**All features work immediately** without any configuration. The demo data is designed to show you exactly how the AI insights will look with your real data.

---

## Connecting to Real Databricks (Optional - For Production)

When you're ready to use real Databricks with live ML models, follow these steps:

### Step 1: Get Your Databricks Workspace URL

1. Log in to your Databricks workspace (https://community.cloud.databricks.com or your edu account)
2. Copy the workspace URL from your browser
   - Example: `https://adb-1234567890123456.7.azuredatabricks.net`

### Step 2: Generate an Access Token

1. In Databricks, click your profile icon (top right)
2. Select "Settings"
3. Click "Developer" → "Access Tokens"
4. Click "Generate New Token"
5. Give it a name (e.g., "Intelligent Finance Platform")
6. Set expiration (recommend 90 days for testing)
7. Click "Generate"
8. **Copy the token immediately** (you won't see it again!)

### Step 3: Create a Cluster

1. In Databricks, click "Compute" in the sidebar
2. Click "Create Cluster"
3. Configure:
   - Name: "finance-analytics"
   - Cluster Mode: Single Node
   - Runtime: Latest LTS (e.g., 13.3 LTS)
4. Click "Create Cluster" and wait for it to start
5. Copy the Cluster ID from the URL or cluster details

### Step 4: Configure Environment Variables

Create a `.env` file in your backend directory:

```bash
# Databricks Configuration
DATABRICKS_WORKSPACE_URL=https://adb-1234567890123456.7.azuredatabricks.net
DATABRICKS_TOKEN=dapi_your_token_here
DATABRICKS_CLUSTER_ID=0123-456789-abcdefgh
```

### Step 5: Restart Backend

```bash
cd backend
python3 -m uvicorn app.main:app --reload
```

You should see:
```
✓ Databricks client initialized: https://adb-1234567890123456...
```

Instead of:
```
⚠️ Databricks running in DEMO MODE (no credentials found)
```

### Step 6: Test the Connection

Visit: http://localhost:8000/api/analytics/status

You should see:
```json
{
  "status": "connected",
  "connected": true,
  "workspace": "https://adb-...",
  "cluster_id": "0123-456789-abcdefgh"
}
```

---

## Next Steps: Training ML Models

Once connected, you can train custom ML models using your project data:

### 1. Upload Training Data to Databricks

Create a notebook in Databricks and run:

```python
# Read your project data
import pandas as pd

# Example: Load budget data
budget_df = pd.read_excel("/path/to/MASTER_PROJECT_BUDGET.xlsx")

# Prepare features for prediction
features = budget_df[['Budget Amount', 'Actual Spent', 'Variance', '% Spent']]

# Train a simple regression model
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save model
import joblib
joblib.dump(model, '/dbfs/models/budget_predictor.pkl')
```

### 2. Create Prediction Functions

```python
def predict_budget_overrun(project_data):
    """Predict if budget will be exceeded"""
    model = joblib.load('/dbfs/models/budget_predictor.pkl')
    predictions = model.predict(project_data)
    return predictions
```

### 3. Expose via SQL Endpoints

1. In Databricks, go to "SQL" → "SQL Warehouses"
2. Create a SQL Warehouse (Serverless recommended)
3. Create queries that call your ML functions
4. Get the connection details

### 4. Update Backend to Use Real Models

Modify `backend/app/services/databricks_client.py`:

```python
def get_budget_predictions(self, project_id: str) -> Dict[str, Any]:
    """Get ML predictions from Databricks SQL"""
    if self.demo_mode:
        return self._demo_predictions()

    # Call real Databricks SQL endpoint
    endpoint = f"sql/statements/execute"
    query = f"SELECT * FROM predict_budget('{project_id}')"

    return self._make_request(endpoint, method="POST", data={"statement": query})
```

---

## Demo Mode vs Production Mode

### Demo Mode (Current - No Setup)
- ✅ Works immediately
- ✅ Realistic sample data
- ✅ All features functional
- ✅ Perfect for development/testing
- ⚠️ Data is static/fake

### Production Mode (With Databricks)
- ✅ Real ML predictions
- ✅ Trained on your data
- ✅ Continuous learning
- ✅ API rate limits higher
- ⚠️ Requires setup
- ⚠️ May incur costs (free tier available)

---

## Troubleshooting

### Issue: "DEMO MODE" banner still showing

**Solution**: Check your `.env` file exists and contains the right variables

```bash
# Verify environment variables are loaded
cd backend
python3 -c "import os; print(os.getenv('DATABRICKS_WORKSPACE_URL'))"
```

### Issue: "Connection refused" error

**Solution**:
1. Check cluster is running in Databricks
2. Verify token hasn't expired
3. Check firewall/network settings

### Issue: "Unauthorized" error

**Solution**:
1. Regenerate access token
2. Update `.env` file
3. Restart backend

---

## Free Tier Limitations

### Databricks Community Edition (Free Forever)
- 15GB RAM cluster
- Single user
- Perfect for development
- No SQL endpoints
- Must use notebooks/APIs directly

### Educational Account (Free with .edu email)
- Full features
- Higher limits
- SQL endpoints available
- Expires after course/program ends

### AWS/Azure Free Tier
- First 14 days free trial
- Then pay-per-use
- Best for production

---

## Cost Estimation (If Using Paid Tier)

For a small construction finance platform:

- **Compute**: ~$0.15/hour for small cluster
- **Usage**: ~10 hours/month for predictions = $1.50/month
- **Storage**: ~$0.03/GB = $0.30/month for project data
- **Total**: ~$2/month

**Your educational account should cover this for free!**

---

## Support

- Databricks Docs: https://docs.databricks.com
- Community Forum: https://community.databricks.com
- Educational Resources: https://databricks.com/learn

---

## Summary

**You don't need to set up anything to start using the AI Insights feature!** It works in demo mode with realistic data right now.

When you're ready for production, follow the steps above to connect your Databricks account and train real ML models on your project data.

The integration is designed to be **zero-config** for development and **easy-config** for production.

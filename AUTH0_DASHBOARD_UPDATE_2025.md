# 🔄 Auth0 Dashboard Update - 2025 Version

## Important Change: "Flows" → "Triggers"

Auth0 updated their dashboard in 2025. The functionality is the same, but the navigation changed:

## What Changed?

### ❌ OLD Dashboard (Before 2025)
```
Actions (sidebar)
├── Flows
│   └── Login
└── Library
```

### ✅ NEW Dashboard (2025)
```
Actions (sidebar)
├── Triggers
│   └── Login / Post Login
├── Library
└── Forms
```

## Visual Comparison

### Old Way (Flows)
```
1. Click: Actions → Flows
2. Select: "Login" flow
3. Add Action: "+ Add Action" → "Build Custom"
4. Deploy & drag into flow
5. Click "Apply"
```

### New Way (Triggers) ✅ USE THIS
```
1. Click: Actions → Triggers
2. Select: "Login / Post Login" trigger
3. Add Action: Click "+" or "Build Custom" button
4. Deploy & drag into flow
5. Click "Apply"
```

## Step-by-Step for NEW Dashboard (Triggers)

### Step 1: Create the Action
1. Go to **Actions** → **Triggers** (in left sidebar)
2. Find **"Login / Post Login"** in the list
3. On the right side, click the **"+"** button OR **"Build Custom"** link
4. Fill in:
   - **Name**: `Add User Metadata`
   - **Trigger**: Will auto-select "Login / Post Login"
5. Click **"Create"**

### Step 2: Add the Code
Replace the default code with:

```javascript
exports.onExecutePostLogin = async (event, api) => {
  const namespace = 'https://drivingtracker.com';

  // Get user metadata
  const role = event.user.app_metadata?.role || 'driver';
  const supervisor_id = event.user.app_metadata?.supervisor_id || null;
  const supervised_users = event.user.app_metadata?.supervised_users || [];

  // Add to token
  api.idToken.setCustomClaim(`${namespace}/role`, role);
  api.idToken.setCustomClaim(`${namespace}/supervisor_id`, supervisor_id);
  api.idToken.setCustomClaim(`${namespace}/supervised_users`, supervised_users);

  api.accessToken.setCustomClaim(`${namespace}/role`, role);
  api.accessToken.setCustomClaim(`${namespace}/supervisor_id`, supervisor_id);
  api.accessToken.setCustomClaim(`${namespace}/supervised_users`, supervised_users);
};
```

### Step 3: Deploy
1. Click **"Deploy"** button (top right corner)
2. Wait for green success message

### Step 4: Add to Login Flow
1. Go back to **Actions** → **Triggers**
2. Click on **"Login / Post Login"** trigger
3. You'll see a flow diagram with:
   - **Start** node on left
   - **Complete** node on right
   - Drag area in the middle
4. On the RIGHT panel, look for **"Custom"** tab
5. Find your **"Add User Metadata"** action
6. **Drag it** from right panel into the middle of the flow
   - Drop it between "Start" and "Complete"
7. Click **"Apply"** button (top right)

### Step 5: Verify
1. You should see your action in the flow diagram
2. The action box should be between Start → Your Action → Complete
3. Green checkmark = deployed and active ✅

## How to Know Which Dashboard You Have

### You have the NEW dashboard (Triggers) if:
- ✅ You see "Triggers" under Actions in sidebar
- ✅ You see "Forms" option in Actions menu
- ✅ When you click Actions, you see "Triggers", "Library", and "Forms"

### You have the OLD dashboard (Flows) if:
- ⚪ You see "Flows" under Actions in sidebar
- ⚪ No "Forms" option
- ⚪ When you click Actions, you see "Flows" and "Library" only

## Both Versions Work!

**Don't worry** - both dashboard versions work perfectly for this project. The only difference is the navigation path.

| Task | Old Dashboard (Flows) | New Dashboard (Triggers) |
|------|----------------------|--------------------------|
| Create Action | Actions → Flows → Login → + Add Action | Actions → Triggers → Login/Post Login → + |
| Edit Action | Actions → Library → Find action | Actions → Library → Find action |
| Add to Flow | Drag from right panel | Drag from Custom tab |
| Deploy | Click "Deploy" | Click "Deploy" |

## Troubleshooting

### ❌ "I don't see Flows OR Triggers"
**Solution:**
- Clear browser cache
- Try different browser
- Make sure you're logged into the correct Auth0 tenant

### ❌ "I can't find my action after deploying"
**Solution:**
1. Go to Actions → Library
2. Your action should be listed there
3. To add to flow:
   - **Old dashboard**: Actions → Flows → Login → Drag from right
   - **New dashboard**: Actions → Triggers → Login/Post Login → Drag from Custom tab

### ❌ "Action is deployed but not working"
**Solution:**
1. Make sure action is **in the flow diagram** (not just deployed)
2. Check it's between "Start" and "Complete" nodes
3. Click "Apply" to save the flow
4. Log out and log back in to test

## Quick Reference Card

### NEW Dashboard (2025) - Step by Step
```
□ 1. Actions → Triggers
□ 2. Find "Login / Post Login"
□ 3. Click "+" or "Build Custom"
□ 4. Name: "Add User Metadata"
□ 5. Paste code
□ 6. Click "Deploy"
□ 7. Go to Actions → Triggers → Login/Post Login
□ 8. Custom tab (right side)
□ 9. Drag action to flow
□ 10. Click "Apply"
```

### OLD Dashboard (Pre-2025) - Step by Step
```
□ 1. Actions → Flows
□ 2. Click "Login" flow
□ 3. "+ Add Action" → "Build Custom"
□ 4. Name: "Add User Metadata"
□ 5. Paste code
□ 6. Click "Deploy"
□ 7. Go to Actions → Flows → Login
□ 8. Drag action from right panel to flow
□ 9. Click "Apply"
```

## Need More Help?

- **Full Guide**: See [AUTH0_SETUP_GUIDE.md](AUTH0_SETUP_GUIDE.md) - now updated for both versions!
- **Checklist**: [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - works with both dashboards
- **Problems**: [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - common issues

---

**TL;DR:** If you see "Triggers" instead of "Flows", you have the new 2025 dashboard. Everything works the same, just follow the "Triggers" path! ✅

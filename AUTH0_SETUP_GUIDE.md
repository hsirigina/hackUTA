# 🔐 Auth0 Setup Guide - Step by Step

This guide will walk you through setting up Auth0 for your driving tracker application.

## Step 1: Create Auth0 Account

1. Go to [https://auth0.com/signup](https://auth0.com/signup)
2. Click **"Sign Up"**
3. Choose one of these options:
   - Sign up with Google/GitHub (recommended - fastest)
   - Sign up with email and password
4. You'll be asked to create a **tenant domain** (e.g., `your-name-hackuta`)
   - This will become: `your-name-hackuta.us.auth0.com`
   - Choose something memorable - you'll need this later!
5. Select **Region**: United States
6. Click **Create Account**

## Step 2: Create Your Application

1. After login, you'll see the Auth0 Dashboard
2. In the left sidebar, click **Applications** → **Applications**
3. Click **"+ Create Application"** button (top right)
4. Fill in the form:
   - **Name**: `Driving Tracker` (or any name you like)
   - **Application Type**: Select **"Regular Web Applications"**
5. Click **"Create"**

## Step 3: Configure Application Settings

You'll be taken to your application settings page. Follow these steps:

### 3.1: Get Your Credentials

1. Click on the **"Settings"** tab
2. **IMPORTANT**: Copy these three values (you'll need them soon):
   - **Domain** (e.g., `your-name-hackuta.us.auth0.com`)
   - **Client ID** (long string like `abc123xyz...`)
   - **Client Secret** (click "👁️ Show" to reveal it)

### 3.2: Configure URLs

Scroll down to **Application URIs** section and enter:

**Allowed Callback URLs:**
```
http://localhost:8501/callback
```

**Allowed Logout URLs:**
```
http://localhost:8501
```

**Allowed Web Origins:**
```
http://localhost:8501
```

**Allowed Origins (CORS):**
```
http://localhost:8501
```

### 3.3: Save Settings

1. Scroll to the bottom
2. Click **"Save Changes"** button

## Step 4: Create User Roles

Now we'll create the supervisor and driver roles:

### 4.1: Enable Role-Based Access Control (RBAC)

1. In the left sidebar, click **User Management** → **Roles**
2. Click **"+ Create Role"** button

### 4.2: Create Supervisor Role

1. **Name**: `supervisor`
2. **Description**: `Can monitor and manage multiple drivers`
3. Click **"Create"**

### 4.3: Create Driver Role

1. Click **"+ Create Role"** again
2. **Name**: `driver`
3. **Description**: `Individual driver account`
4. Click **"Create"**

## Step 5: Set Up User Metadata (For Relationships)

We need to add custom metadata to users to track supervisor/driver relationships:

### 5.1: Create an Action

**IMPORTANT:** Auth0 has updated their dashboard. You'll see either **"Flows"** or **"Triggers"** - both work the same way!

#### Option A: If you see "Flows" (older dashboard)
1. In the left sidebar, click **Actions** → **Flows**
2. Click on **"Login"** flow
3. Click **"+ Add Action"** → **"Build Custom"**

#### Option B: If you see "Triggers" (newer dashboard - 2025)
1. In the left sidebar, click **Actions** → **Triggers**
2. Find **"Login / Post Login"** trigger
3. Click the **"+"** button or **"Build Custom"** on the right side

#### Both options: Fill in the Action details
4. Fill in:
   - **Name**: `Add User Metadata`
   - **Trigger**: `Login / Post Login`
5. Click **"Create"**

### 5.2: Add the Code

Replace the default code with this:

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

### 5.3: Deploy and Add to Flow

1. Click **"Deploy"** button (top right)

#### Option A: If using "Flows" (older dashboard)
2. Go back to **Actions** → **Flows** → **Login**
3. Drag the **"Add User Metadata"** action from the right panel into the flow (between "Start" and "Complete")
4. Click **"Apply"** (top right)

#### Option B: If using "Triggers" (newer dashboard - 2025)
2. Go back to **Actions** → **Triggers**
3. Find **"Login / Post Login"** trigger
4. Click on it to open the flow builder
5. Look for **"Custom"** tab on the right side
6. Find your **"Add User Metadata"** action
7. Drag it into the flow (between "Start" and "Complete")
8. Click **"Apply"** (top right)

## Step 6: Create Test Users

Let's create test users to try the system:

### 6.1: Create a Supervisor User

1. Go to **User Management** → **Users**
2. Click **"+ Create User"**
3. Fill in:
   - **Email**: `supervisor@test.com`
   - **Password**: `Test1234!` (or any strong password)
   - **Connection**: `Username-Password-Authentication`
4. Click **"Create"**

### 6.2: Set Supervisor Metadata

1. Click on the newly created user
2. Scroll down to **"Metadata"** section
3. In **app_metadata** field, add this JSON:
```json
{
  "role": "supervisor",
  "supervised_users": []
}
```
4. Click **"Save"**

### 6.3: Create a Driver User

1. Click **"+ Create User"** again
2. Fill in:
   - **Email**: `driver@test.com`
   - **Password**: `Test1234!`
   - **Connection**: `Username-Password-Authentication`
3. Click **"Create"**

### 6.4: Set Driver Metadata and Link to Supervisor

1. Click on the driver user
2. Copy their **user_id** (starts with `auth0|...`)
3. In **app_metadata** field, add:
```json
{
  "role": "driver",
  "supervisor_id": "PASTE_SUPERVISOR_USER_ID_HERE"
}
```
4. Click **"Save"**

### 6.5: Update Supervisor's Supervised Users

1. Go back to the supervisor user
2. Copy the driver's **user_id**
3. Update supervisor's **app_metadata**:
```json
{
  "role": "supervisor",
  "supervised_users": ["PASTE_DRIVER_USER_ID_HERE"]
}
```
4. Click **"Save"**

## Step 7: Configure Your Application

Now let's connect Auth0 to your app:

### 7.1: Create .env File

1. In your project folder, copy the example:
```bash
cp .env.example .env
```

2. Open `.env` file and update with your Auth0 credentials:
```env
# Auth0 Configuration (from Step 3.1)
AUTH0_DOMAIN=your-name-hackuta.us.auth0.com
AUTH0_CLIENT_ID=your_client_id_here
AUTH0_CLIENT_SECRET=your_client_secret_here
AUTH0_CALLBACK_URL=http://localhost:8501/callback

# Application Settings
SECRET_KEY=generate_a_random_secret_here
APP_URL=http://localhost:8501

# Database
DATABASE_URL=sqlite:///driving_tracker.db

# Arduino API Configuration
ARDUINO_API_KEY=generate_another_random_secret
API_PORT=5000
```

### 7.2: Generate Secret Keys

Generate random secrets for `SECRET_KEY` and `ARDUINO_API_KEY`:

```bash
# On Mac/Linux:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use this online: https://randomkeygen.com/
```

## Step 8: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 9: Run Your Application

### Terminal 1 - Start Streamlit:
```bash
streamlit run app.py
```

### Terminal 2 - Start API (optional, for Arduino):
```bash
python api_endpoint.py
```

## Step 10: Test the Login

1. Open browser to: `http://localhost:8501`
2. Click **"Login with Auth0"**
3. You'll be redirected to Auth0 login page
4. Login with:
   - **Supervisor**: `supervisor@test.com` / `Test1234!`
   - **Driver**: `driver@test.com` / `Test1234!`

### What You Should See:

**As Supervisor:**
- Dashboard showing all supervised drivers
- Ability to monitor multiple drivers
- View aggregated statistics

**As Driver:**
- Personal dashboard
- Own driving statistics
- Start/stop session buttons

## 🎉 You're Done!

Your Auth0 authentication is now fully configured with multi-tier supervisor/driver relationships!

## 📸 Visual Guide Screenshots

If you need help finding anything in the Auth0 dashboard, here are the key locations:

1. **Applications**: Left sidebar → Applications → Applications
2. **Roles**: Left sidebar → User Management → Roles
3. **Users**: Left sidebar → User Management → Users
4. **Actions**: Left sidebar → Actions → Flows
5. **Settings**: Click on your application name

## 🆘 Troubleshooting

### "Callback URL mismatch" error
- Make sure `http://localhost:8501/callback` is in **Allowed Callback URLs** in Auth0
- Make sure your `.env` has `AUTH0_CALLBACK_URL=http://localhost:8501/callback`

### "Unauthorized" error
- Check that `AUTH0_CLIENT_ID` and `AUTH0_CLIENT_SECRET` are correct in `.env`
- Make sure there are no extra spaces in the `.env` file

### User role not showing
- Make sure you deployed the Action in Step 5.3
- Check that the Action is in the Login flow
- Verify user has `app_metadata` with `role` field

### Can't see supervised drivers
- Verify supervisor's `supervised_users` array has driver user IDs
- Verify driver's `supervisor_id` matches supervisor's user ID
- Both IDs should start with `auth0|`

## 📚 Additional Resources

- [Auth0 Documentation](https://auth0.com/docs)
- [Auth0 Actions](https://auth0.com/docs/customize/actions)
- [Auth0 User Metadata](https://auth0.com/docs/manage-users/user-accounts/metadata)

## 🏆 For HackUTA Judges

This implementation demonstrates:
- ✅ Full OAuth2 authentication flow
- ✅ Role-based access control (RBAC)
- ✅ Custom user metadata for relationships
- ✅ Secure session management
- ✅ Multi-tier account architecture
- ✅ Production-ready security practices

# 📱 Setup SMS with Twilio

This guide will help you configure automatic SMS notifications for the learning platform.

## Step 1: Install Twilio

Run this command in your terminal:

```bash
pip install twilio
```

## Step 2: Create Twilio Account

1. Go to [https://www.twilio.com](https://www.twilio.com)
2. Click "Sign up" and create a free account
3. Complete the verification process with your phone number

## Step 3: Get Your Credentials

1. After signing in, go to your [Twilio Dashboard](https://console.twilio.com)
2. Find your **Account SID** (starts with "ACxxxxxxxx")
3. Find your **Auth Token** (a long string of characters)
4. Get a **Twilio Phone Number** (you'll see it in the dashboard)

## Step 4: Configure in alerts.py

Edit the file `⚠️alerts.py` and replace:

```python
TWILIO_ACCOUNT_SID = "your_account_sid"    # ← Replace with your Account SID
TWILIO_AUTH_TOKEN = "your_auth_token"      # ← Replace with your Auth Token
TWILIO_PHONE = "+1234567890"               # ← Replace with your Twilio number
RECIPIENT_PHONE = "+57XX"                  # ← Replace with student's phone
```

### Example:
```python
TWILIO_ACCOUNT_SID = "ACa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p"
TWILIO_AUTH_TOKEN = "your1234567890token1234567890"
TWILIO_PHONE = "+12015551234"              # Example: United States Twilio number
RECIPIENT_PHONE = "+573001234567"          # Example: Colombian phone number
```

## Common Phone Number Formats

| Country | Format | Example |
|---------|--------|---------|
| **Colombia** | +57 | +573001234567 |
| **USA** | +1 | +12015551234 |
| **Spain** | +34 | +34912345678 |
| **Mexico** | +52 | +5215551234567 |
| **Argentina** | +54 | +541123456789 |

## Features Included

✅ Automatic SMS when exam is completed  
✅ Automatic SMS when activity is submitted  
✅ SMS with exam level and average score  
✅ SMS with activity file name  
✅ No button needed - SMS sends automatically!

## Troubleshooting

**Error: "Twilio not installed"**
- Run: `pip install twilio`

**Error: "Configure your Twilio credentials"**
- Make sure you replaced `your_account_sid` and `your_auth_token` with real values

**SMS not sending?**
- Check that your Account SID and Auth Token are correct
- Check that phone numbers have the correct format with country code
- Verify your Twilio account has credits (free tier includes 100 SMS notifications)

## Testing Your Setup

To test if SMS is working:

1. Go to the Alerts page (⚠️alerts.py)
2. Click any of the example buttons
3. You should receive an SMS on the configured phone number

---

**Questions?** Check [Twilio Documentation](https://www.twilio.com/docs)

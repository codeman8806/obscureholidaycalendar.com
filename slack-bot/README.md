# Obscure Holiday Slack Bot

## Setup (Railway or any Node 18+ host)

1) Install dependencies:
   - `npm install`

2) Set env vars:
   - `SLACK_SIGNING_SECRET=<signing_secret>`
   - `SLACK_APP_NAME=ObscureHolidayCalendar` (optional)
   - `SLACK_CLIENT_ID=<client_id>` (for public installs)
   - `SLACK_CLIENT_SECRET=<client_secret>` (for public installs)
   - `SLACK_REDIRECT_URI=https://<your-host>/slack/oauth/callback`
   - `SITE_URL=https://www.obscureholidaycalendar.com`
   - `APP_URL=https://www.obscureholidaycalendar.com/app/` (optional)
   - `SLACK_SUPPORT_URL=https://www.obscureholidaycalendar.com/slack-bot/` (optional)
   - `SLACK_VOTE_URL=<optional>`
   - `SLACK_REVIEW_URL=<optional>`
   - `SLACK_ADMIN_TOKEN=<random_string_for_admin_endpoint>`
   - `PORT=8080` (Railway injects this)
   - Stripe (optional, for premium):
     - `STRIPE_SECRET_KEY=<sk_live_or_test>`
     - `STRIPE_PRICE_ID_INTRO=<price_0_99>`
     - `STRIPE_PRICE_ID_STANDARD=<price_3_99>`
     - `STRIPE_WEBHOOK_SECRET=<whsec_...>`
     - `STRIPE_SUCCESS_URL`
     - `STRIPE_CANCEL_URL`
     - `STRIPE_PORTAL_RETURN_URL`

3) Slack app config:
   - OAuth & Permissions:
     - Redirect URL: `https://<your-host>/slack/oauth/callback`
     - Scopes: `commands`, `chat:write`
   - Slash commands: point to `https://<your-host>/slack/commands`
   - Install URL: `https://<your-host>/slack/install`
   - Stripe webhook endpoint: `https://<your-host>/stripe/webhook`
   - Enable Stripe events: `checkout.session.completed`, `invoice.paid`, `customer.subscription.updated`, `customer.subscription.deleted`

Note: install the app via the OAuth flow (Install URL) in your own workspace too, so tokens are created exactly the same way as public installs.

Admin endpoint:
- `GET /admin/installs?token=<SLACK_ADMIN_TOKEN>` returns install count and list.

## Slash commands
- `/today`
- `/tomorrow`
- `/upcoming [days]`
- `/week [days]`
- `/date MM-DD`
- `/search <query>`
- `/random`
- `/facts [name or MM-DD]`
- `/setup key=value ...`
- `/premium`
- `/upgrade`
- `/manage`
- `/help`
- `/invite`
- `/vote`
- `/rate`
- `/support`
- `/app`

## /setup examples
- `/setup timezone=America/New_York hour=9 promotions=true`
- `/setup holiday_choice=1 skip_weekends=true`

Defaults:
- timezone: `UTC`
- hour: `9`
- holiday_choice: `0` (first holiday)
- skip_weekends: `false`

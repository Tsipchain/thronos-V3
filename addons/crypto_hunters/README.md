# Crypto Hunters – Full Package (v3)

Welcome to version 3 of the Crypto Hunters project.  This archive contains
everything you need to explore, test and present the Crypto Hunters concept —
from lore and character backstories through to a working backend API and a
cross‑platform mobile demo.  All documentation is provided in English and
Greek where appropriate.  Please read this file for a quick overview.

## Contents

- `docs/` — World building and reference material
  - `story_bible.md` — English high‑level overview of the Crypto Hunters world
  - `storyline_gr.md` — Αναλυτικό σενάριο στα ελληνικά (Πράξεις, κεφάλαια, αποστολές)
  - `characters.md` — English character descriptions
  - `missions.md` / `missions.json` — Human‑readable mission list and machine JSON seed
  - `items.md` / `items.json` — Shop item list and corresponding JSON seed
  - `api.md` — API reference for the demo server
  - `whitepaper.md` — Whitepaper (English)
  - `pitch_deck.md` — Outline of the pitch deck

- `backend/` — Node/Express based demo server
  - `drx.js` — API endpoints for missions, items, wallet and withdraw queue
  - `bot_stub.js` — Example XRPL payout bot for test networks
  - `config.example.json` — Example configuration file (copy to `config.json`)
  - `data/` — Mission and item seeds used by the API
  - `panel/` — A minimal HTML admin panel for approving withdraw requests

- `mobile-demo/` — Expo/React Native demo application
  - `App.js` — Home, Missions, Wallet, Items, Inventory and Story screens
  - `package.json` / `README.md` — Basic dependencies and usage instructions

## Quickstart

### Backend

Install dependencies and start the server at `localhost:3000`:

```bash
cd backend
npm install express
node drx.js
```

Optionally copy `config.example.json` to `config.json` and supply your own admin
key and XRPL testnet credentials.  Open `http://localhost:3000/panel` to use the
admin interface (you must provide your admin key in the input field).

### Mobile demo

The demo app is built with Expo.  Install dependencies and run the expo server
from the `mobile-demo` folder:

```bash
cd mobile-demo
npm install
npx expo start
```

If you are running the backend on a different host or port, edit the `API`
constant at the top of `App.js` accordingly.  The app includes screens for
missions, wallet management, item purchases, inventory and a storyline viewer.

## Notes

- The DRX balances tracked by the server are off‑chain game credits.  When the
  player requests a withdraw, the amount is queued for review.  Once an
  administrator approves and triggers the XRPL bot, the real DRX will be paid
  out on chain.
- For security reasons, do not use the provided `AUTH_WALLET_SEED` or admin key
  in production.  Always supply your own secrets via `config.json` or
  environment variables.
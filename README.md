# Rubi's 22nd Birthday Celebration 🎂🎉

A beautiful interactive birthday celebration with fireworks, animated cakes, and surprise photo popups!

## Run Locally

```bash
node server.js
```

Then open your browser to: **http://localhost:3000**

## Features

- 🎆 Interactive fireworks - click anywhere!
- 🎂 Animated birthday cakes with candles
- 🖼️ Surprise photo popups every 15 fireworks (randomly selected from 5 photos!)
- 🎵 Background music
- ⌨️ Keyboard shortcuts:
  - SPACE: Random firework
  - M: Toggle music

## Deploy to Vercel

This is a static site (no build step). Import the GitHub repo in Vercel, or run:

```bash
vercel deploy --prod
```

`server.js` is only for running locally.

## Files

- `index.html` - Main page
- `script.js` - All animations and logic
- `style.css` - Styling
- `itinerary.html` - 28 Nov itinerary page
- `server.js` - Simple Node.js server
- `1000028077.jpg` - Birthday photo
- `happy-birthday-rock-348157.mp3` - Background music

---
name: fenix-login
user-invocable: true
description: 'Logs the user into Fenix (fenix.tecnico.ulisboa.pt) using OpenClaw browser automation. Use this skill to start an authenticated browser session for subsequent Fenix actions.'
argument-hint: 'No argument needed — just invoke to log in to Fenix.'
---

# Fenix Login Skill (OpenClaw)

This skill launches a dedicated browser session for Fenix using OpenClaw, allowing the user to log in interactively. No cookies or tokens are copied manually — authentication is preserved in the browser profile.

## Procedure

1. **Start/Open Browser Profile**
	- Run: `openclaw browser --browser-profile fenix start`
	- This launches or attaches to a dedicated Chrome session for Fenix.

2. **Open Fenix Login Page**
	- Run: `openclaw browser --browser-profile fenix open https://fenix.tecnico.ulisboa.pt/login.do`
	- The login page will appear in the browser.

3. **Ask User to Log In**
	- Prompt the user: "Please log in to Fenix in the browser window that opened. Let me know when you see your Fenix homepage."

4. **Verify Login**
	- Optionally, run: `openclaw browser --browser-profile fenix snapshot --json`
	- Parse the HTML to check for the presence of the Fenix homepage (not the login form).
	- If not logged in, prompt the user to try again.

5. **Session Ready**
	- Once logged in, the browser profile remains authenticated for all subsequent Fenix actions (course listing, navigation, etc.).

## Notes
- The browser session is isolated to the `fenix` profile and persists until closed.
- No cookies or credentials are exposed to the agent — all actions happen in-browser.
- If the session expires, simply re-run this skill to log in again.

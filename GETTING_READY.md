# 🚀 GETTING READY for the Workshop

Welcome! We’re excited to have you join us. This page will help you get set up before the workshop. If you run into any trouble, don’t worry—support will be provided at the workshop! But if you get things ready in advance, we’ll have more time for cool projects and hands-on fun. 😎

## 📚 Table of Contents

1. [💻 Laptop](#-laptop)
2. [🐙 Git](#-git)
3. [🐍 Python + UV](#-python--uv)
4. [🐳 Docker](#-docker)
5. [🦞 OpenClaw](#-openclaw)
6. [📝 IDE (VS Code Recommended)](#-ide-vs-code-recommended)
7. [💬 Telegram (Optional)](#-telegram-optional)

---

## 💻 Laptop

- **📦 What is it?**  
	Your personal computer! This is your main tool for coding, running commands, and participating in the workshop.

- **🛠️ How do I install it?**  
	Just bring your laptop, fully charged. Any OS (Windows, macOS, Linux) works.

- **🔎 How do I check it worked?**  
	If you’re reading this, you’re good to go!

- **🚀 How do I use it?**  
	You’ll use your laptop for everything: coding, running commands, and accessing workshop materials.

---

## 🐙 Git

- **📦 What is it?**  
	Git is a tool to manage and share code (version control). It lets you download, update, and collaborate on code with others.

- **🛠️ How do I install it?**  
	- **Windows:** [Download Git](https://git-scm.com/download/win) and run the installer.
	- **macOS:** Run `brew install git` (if you have Homebrew) or [download here](https://git-scm.com/download/mac).
	- **Linux:** Run `sudo apt install git` or `sudo dnf install git`.

- **🔎 How do I check it worked?**  
	Open a terminal and run:  
	`git --version`  
	You should see a version number.

- **🚀 How do I use it?**  
	You’ll use Git to clone the workshop repo:  
	`git clone https://github.com/SousaDiconium/ddsP-Sinfo_2026-Workshop`  
	After this, you’ll have all the code on your laptop.

---

## 🐍 Python + UV

- **📦 What is it?**  
	Python is a popular programming language used for scripting, automation, and building cool projects. UV is a super-fast Python package manager that also includes its own Python runtime—so you don’t need to install Python separately!

- **🛠️ How do I install it?**  
	- Go to the [UV Standalone Installer](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer) and follow the instructions for your OS.
	- This will install both UV and Python in one go.

- **🔎 How do I check it worked?**  
	- Open a terminal and run: `uv --version`
	- You should see a version number.

- **🚀 How do I use it?**  
	- In the root of the workshop folder, run:  
		`uv sync --all-packages`
	- This will create a `.venv` with all the dependencies for the entire workshop.
	- After this, you’re ready to run Python scripts and everything should “just work.”

---

## 🐳 Docker

- **📦 What is it?**  
	Docker lets you run apps in containers, so everything works the same for everyone. It’s like a magic box that makes sure “it works on my machine” is true for all!

- **🛠️ How do I install it?**  
	- [Download Docker Desktop](https://www.docker.com/products/docker-desktop/) for your OS and follow the instructions.

- **🔎 How do I check it worked?**  
	- Run: `docker --version` and `docker-compose --version`
	- You should see version numbers.
	- Open the Docker Desktop app—you should see it running and ready.

- **🚀 How do I use it?**  
	- In the project root, run:  
		`docker-compose up -d`  
		(the `-d` means it runs in the background)
	- To see which services are running, use:  
		`docker-compose ps`
	- You should also see the running containers in Docker Desktop.
	- After this, all services should start up automatically and be ready for you to use.

---

## 🦞 OpenClaw

- **📦 What is it?**  
	OpenClaw is an open-source platform for building and running AI-powered agents and automations. In this workshop, we’ll use it to connect your code to cool automations and external services—think of it as your “robot assistant” toolkit!


- **🛠️ How do I install it?**  
	- Go to the [OpenClaw Install Guide](https://docs.openclaw.ai/install) and follow the instructions for your operating system.
	- This will guide you through downloading and installing OpenClaw step-by-step.

- **🔎 How do I check it worked?**  
	- Try running: `openclaw --version` in your terminal.
	- You should see a version number or help message.

- **🚀 How do I use it?**  
	- We’ll finish the setup together during the workshop.
	- You’ll use OpenClaw to run agents and connect to other tools—no need to worry about details yet!

---

## 📝 IDE (VS Code Recommended)

- **📦 What is it?**  
	An IDE (Integrated Development Environment) is where you’ll write and edit code. We recommend [Visual Studio Code (VS Code)](https://code.visualstudio.com/) because it makes it easier for everyone to follow along, and we’ve prepared some tasks that work out-of-the-box for debugging and running code. Other editors (PyCharm, Sublime, etc.) are possible, but VS Code is preferred for this workshop.

- **🛠️ How do I install it?**  
	- [Download VS Code](https://code.visualstudio.com/)
	- Install the Python and Docker extensions (search for them in the Extensions sidebar).


- **🔎 How do I check it worked?**  
	- Open VS Code, open a folder, and make sure you can edit files.


- **🚀 How do I use it?**  
	- Open the workshop folder in VS Code.
	- You’ll see pre-made tasks available in the “Run & Debug” panel or via the Command Palette (⇧⌘P / Ctrl+Shift+P, then type “Tasks: Run Task”).
	- **Don’t run the tasks yet!** Just check that you can see them listed—this means everything is set up. We’ll use them together during the workshop.
	- Having VS Code set up this way will make following along and getting help much easier!

---

## 💬 Telegram (Optional)

- **📦 What is it?**  
	A messaging app. We might use it for bonus interactions with your agent.

- **🛠️ How do I install it?**  
	- [Download Telegram](https://telegram.org/) for your device.

- **🔎 How do I check it worked?**  
	- Open Telegram and log in.

- **🚀 How do I use it?**  
	- If you want, you’ll be able to interact with your agent via Telegram. This is just for fun!

---

# 🎉 You’re Ready!

If you have all this set up, you’re good to go! If you get stuck, don’t worry—we’ll help you out at the start of the workshop. The more you have ready, the more time we’ll have for awesome projects and experiments!

This page is still getting ready, please come back in the very near future! 👋 
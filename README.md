
![cli-password-manager1](images/2025-07-27-010250_hyprshot.png)
# 🔐 CLI Password Manager

Cli-password-manager is a utility to encrypt, store and manage passwords from anywhere in your terminal. It allows you to have full control of your
services' usernames and passwords by storing them locally and encrypted using a passkey of your choice.

## Degooglify your life and take control of your data.

> "The closest thing to burying your passwords in an undisclosed location without having to go outside"  
> —Some arch user, probably

---

## 🚀 Features

- Store, retrieve, and manage passwords securely
- Easy-to-use CLI interface
- Encryption for stored passwords
- Generate secure passwords on demand
- Cross-platform support
- Open-source and customizable

---

## 🧑‍💻 How does it work

 ### When you save a password it gets encrypted using the "Cryptography" library

- The four word passkey acts as the encryption and decryption key
- A secure 32-byte hash is derived from the passkey and used as the salt in the encryption and decryption process
- Data is stored locally in a .json file

### Why 4 words?

- Inspired by xkcd's take on password strength

![xkcd](images/password_strength.png)

---
## 📦 Installation

### Using `git`

```bash
git clone https://github.com/ManoloEsS/cli-password-manager.git
cd cli-password-manager
# Install dependencies (example: Python)
pip install -r requirements.txt
```

### Using Python Package (if available)

```bash
pip install cli-password-manager
```

---

## 🛠 Usage

```bash
# Add a new password
cli-password-manager add <service> <username> <password>

# Retrieve a password
cli-password-manager get <service>

# List all stored services
cli-password-manager list

# Delete a password
cli-password-manager delete <service>
```

---

## 🖼️ Screenshots

Add your screenshots here!

![image1](image1)
<!-- You can rename image1 to your actual file name or add more images as needed -->

---

## 🎉 Cool Emojis

- 🔒 Secure storage
- ⚡ Fast access
- 🌈 Customizable
- 🧑‍💻 Developer-friendly

---


## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Project made for the Boot.dev 2025 Hachathon.

Contributors:
-ManoloEsS
-Soullessgent


# AWS Utils CLI

A Python tool to facilitate interactions with some services on AWS.

## 📦 Features
- 🔐 Login to AWS SSO via CLI (`aws sso login`)
- 🌐 Listing configured profiles in the AWS CLI and active SSO profiles
- 🛠️ Connections to some AWS services

---

## 🧰 Prerequisites
- Profile preconfigured in AWS CLI
- Python >= 3.9
- AWS CLI installed and configured ([Guia oficial](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html))
- Credentials configured via SSO or `aws configure`
- Python dependencies installed (see below)

---

## 🔧 Installation
### Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

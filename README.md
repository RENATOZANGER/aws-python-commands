# AWS Utils CLI

A Python tool to facilitate interactions with AWS services.

## 📦 Features
- 🔐 Login to AWS SSO via CLI (`aws sso login`)
- 🌐 List configured profiles in the AWS CLI and active SSO profiles
- 🛠️ Connect to various AWS services

---

## 🧰 Prerequisites
- **Python >= 3.9**
- **AWS CLI v2** installed ([Official Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html))
- **AWS Profile Configured:**
  - **SSO (Primary approach used in this guide):** Configured via `aws configure sso`
  - **Static Keys (Alternative):** Configured via `aws configure` (Access Key ID & Secret Access Key)
- Python dependencies installed (see Installation section)

---

## ⚙️ Initial Setup (First-Time Only)

Before logging in for the first time, set up your SSO profile using the AWS CLI:

```bash
aws configure sso
```

Provide your SSO details when prompted:
- **SSO session name:** `<your-session-name>` *(e.g., `company-sso`)*
- **SSO start URL:** `https://<your-subdomain>.awsapps.com/start`
- **SSO region:** `us-east-1` *(The AWS region where your IAM Identity Center/SSO is hosted)*
- Select your **AWS Account** and **Role** *(e.g., `AdministratorAccess`)*
- **Profile name:** `<your-profile-name>` *(e.g., `renato_admin`)*

---

## 🔑 Authentication
### Once configured, authenticate daily or whenever your session expires:
```bash
aws sso login --profile renato_admin
```

Verify your active identity:
```bash
aws sts get-caller-identity --profile renato_admin
```

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

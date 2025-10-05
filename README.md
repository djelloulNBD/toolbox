# 🔗 Instance Links Provider

A secure Streamlit web application that generates quick-access links for cloud instances across AWS, Azure, and GCP providers. The application creates authenticated remote desktop (RDP), terminal, and Wireshark links based on instance names.

## Features

- 🔐 **Secure Authentication**: User login system with bcrypt password hashing
- ☁️ **Multi-Cloud Support**: Generate links for AWS, Azure, and GCP instances
- 🚀 **Quick Access Links**: Automatically generates RDP, Terminal, and Wireshark URLs
- 🔑 **Secure Credentials**: MD5-hashed usernames and passwords for RDP access
- 🎯 **Easy-to-Use Interface**: Simple input form with cloud provider selection

## Screenshots

The application provides a clean, centered interface where users can:
- Select their cloud provider (AWS/Azure/GCP)
- Enter an instance name
- Generate secure access links and credentials

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd toolbox
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run main.py
   ```

## Configuration

### Authentication
The application supports both single-user and multi-user authentication:

- **Single User**: Set `login_username` and `login_password` in secrets
- **Multiple Users**: Use the `auth.users` array for multiple user accounts

### Domain Configuration
Configure domains for your cloud providers:
- `domain`: Base domain used for all providers
- `aws`, `azure`, `gcp`: Provider-specific domains (optional)

### Security
- Passwords are automatically hashed using bcrypt if provided in plaintext
- Cookies are secured with configurable expiration
- Remote IDs are generated using MD5 hashing with your secret suffix

## Usage

1. **Login**: Enter your username and password
2. **Select Provider**: Choose AWS, Azure, or GCP from the sidebar
3. **Enter Instance Name**: Input your instance identifier (e.g., `LBLI-5GEB-1745411368365-10`)
4. **Generate Links**: Click the "Generate Links" button
5. **Access Services**: Use the generated links to access:
   - **RDP Console**: Remote desktop access with auto-generated credentials
   - **Terminal**: SSH/terminal access
   - **Wireshark**: Network analysis interface

## Requirements

- Python 3.7+
- Streamlit
- streamlit-authenticator
- hashlib (built-in)

## Security Considerations

- Store your `secrets.toml` file securely and never commit it to version control
- Use strong, unique passwords for authentication
- Regularly rotate your secret suffix for remote ID generation
- Consider using environment variables for sensitive configuration in production

## Troubleshooting

### Common Issues

1. **Missing Secret Error**: Ensure `secret` is configured in your `secrets.toml`
2. **Missing Domain Error**: Verify `domain` is set in your configuration
3. **Authentication Failed**: Check your username/password in the secrets file

### Logs
Check the Streamlit logs for detailed error messages when issues occur.

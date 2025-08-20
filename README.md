# SSL Certificate Expiry Monitoring with Zabbix

This project provides a solution for monitoring SSL certificate expiration dates using Zabbix monitoring system.

# Overview
The solution consists of:

A Python script that checks SSL certificate expiration dates

A Zabbix template for automatic discovery and monitoring

A configuration file for Zabbix agent

# Installation
1. Install the Python Script
2. Copy the Python script to your Zabbix server/agent:

```bash
sudo mkdir -p /var/opt/script/zabbix/
sudo cp checkSSL.py /var/opt/script/zabbix/
sudo chmod +x /var/opt/script/zabbix/checkSSL.py
```
# Install Required Dependencies
   
Ensure Python 3 and required libraries are installed:

```bash
# For Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-ssl
```

# For CentOS/RHEL
sudo yum install python3 python3-pyOpenSSL

# Configure Zabbix Agent
Create the agent configuration file:

```bash
sudo tee /etc/zabbix/zabbix_agentd.d/check_ssl.conf << 'EOF'
UserParameter=check.SSL[*],/var/opt/script/zabbix/checkSSL.py --urls "$1"
EOF
Restart Zabbix agent:
```

```bash
sudo systemctl restart zabbix-agent
```

Import Zabbix Template
   
In Zabbix web interface, go to Configuration → Templates

Click Import and select the provided XML template file

Assign the template to your host

Configuration
Template Macros
The template uses the following macro:

{$URLS} - List of URLs to monitor (space-separated)

Example value:

```text
example.com google.com:443 github.com:8443
URL Format
URLs can be specified in different formats:

example.com (defaults to port 443)

example.com:443 (explicit port)

https://example.com (URL with scheme)
```

How It Works
Discovery: Zabbix runs the script with the list of URLs from {$URLS} macro

Data Collection: The script connects to each URL and retrieves SSL certificate information

Low-Level Discovery: Zabbix discovers each URL as a separate item

Monitoring: Zabbix creates items and triggers for each discovered URL

Alerting: Triggers fire when certificates are nearing expiration

Trigger Thresholds
The template includes three levels of triggers:

Disaster (Red): Certificate expires in 5 days or less

Average (Yellow): Certificate expires between 5-30 days

Info (Green): Certificate expires between 30-60 days

Troubleshooting
Common Issues
"Cannot resolve hostname":

Check DNS configuration

Verify hostname is correct

"Connection timeout":

Check network connectivity

Verify the service is running on the specified port

"SSL verification error":

Certificate might be self-signed or invalid

Consider adjusting SSL context settings in the script

"embedded null byte":

Check for special characters in URL

Ensure URL formatting is correct

Debugging
To test the script manually:

```bash
cd /var/opt/script/zabbix/
python3 checkSSL.py example.com google.com:443
```

Logs

Check Zabbix agent logs for errors:

```bash
tail -f /var/log/zabbix/zabbix_agentd.log
```

Security Considerations
The script runs with the same privileges as the Zabbix agent

SSL verification is enabled by default

Only TLS 1.2 and higher are supported

The script validates hostnames before connecting

# Customization
Adjusting Timeouts
Edit the script to change connection timeouts:

python
conn.settimeout(10.0)  # Change this value
Adding Custom Ports
Modify the port parsing logic in the script if needed.

# Changing Trigger Thresholds
Edit the trigger expressions in the Zabbix template to adjust warning thresholds.

# Support
For issues with this solution:

Check the troubleshooting section above

Verify Zabbix agent has network access to monitored hosts

Ensure Python 3.6+ is installed

Confirm SSL certificates are valid and trusted

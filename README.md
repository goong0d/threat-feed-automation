# Threat Feed Automation

A Python-based cybersecurity automation project for ingesting, cleaning, validating, storing, and synchronizing threat intelligence indicators (IOCs).

The system works with **IP addresses, domains, and file hashes**. Valid indicators are stored in MySQL and pushed to a **local mock firewall API** using HTTP requests. A cleanup process removes indicators older than **90 days** from the database and synchronizes the deletion with the mock firewall.

> **Important:** This repository uses a Flask-based mock firewall for development/testing. It is not connected to a production firewall.

## Features

- Tkinter GUI for IOC input
- Extraction of IPs, domains, and hashes using regular expressions
- Basic IOC normalization, including common defanged formats such as `[.]` and `(dot)`
- MySQL storage with timestamps
- REST API integration using Python `requests`
- Flask-based mock firewall for local testing
- Push operations for IPs, domains, and hashes
- Automatic cleanup of indicators older than 90 days
- Firewall/database synchronization during cleanup
- Separate modules for interface, database, API pushing, mock firewall, and cleanup

## Architecture

```text
Raw Threat Intelligence
          |
          v
   Tkinter GUI
          |
          v
 IOC Cleaning / Regex Extraction
          |
          v
       MySQL
     /    |    \\
    IP  Domain  Hash
          |
          v
     API Pusher
          |
          v
   Flask Mock Firewall
          |
          v
  90-Day Retention Cleanup
          |
          +----> MySQL
          |
          +----> Mock Firewall

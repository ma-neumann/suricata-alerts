## Suricata Email Alert Notifier (Docker)

This project is a lightweight, containerized Python service that monitors a Suricata `eve.json` log file and sends email notifications whenever new alerts are detected.
It is designed for easy deployment in a Docker environment and can be customized entirely through environment variables.

### Features

* **Real-time monitoring** of Suricata alerts from `eve.json`
* **Email notifications** for new alerts, sent to one or more recipients
* **Customizable SMTP settings** with authentication support
* **Configurable polling interval**
* Runs as a **persistent background service** in Docker

### How it works

1. The container continuously watches `/logs/eve.json` for new Suricata alerts.
2. When new alerts are found, it formats them with relevant details:

   * Alert signature
   * Source and destination IPs/ports
   * Protocol
   * Timestamp
3. Sends a formatted email notification to the specified recipients.

### Environment Variables

| Variable       | Description                                   | Example Value                       |
| -------------- | --------------------------------------------- | ----------------------------------- |
| `MAILER`       | Mailer type (e.g. SMTP)                       | `SMTP`                              |
| `USERNAME`     | SMTP username                                 | `apikey`                            |
| `PASSWORD`     | SMTP password or API key                      | `mypassword`                        |
| `FROM`         | Sender email address                          | `alerts@example.com`                |
| `TO`           | Comma-separated list of recipient emails      | `admin@example.com,ops@example.com` |
| `SMTP_SERVER`  | SMTP server address                           | `smtp.mailserver.com`               |
| `PORT`         | SMTP server port                              | `587`                               |
| `POLLING_TIME` | Time in seconds between checks for new alerts | `10`                                |
| `POLL_LIMIT`   | Maximum number of new alerts to send          | `20`                                |
| `HOST`         | Name to identify your log source              | `myserver1`                         |

### Docker Usage

1. Clone the repository using `git clone https://github.com/AdarWa/suricata-alerts`
2. Add the alert-emailer to your docker

```yaml
  alert-emailer:
    build: ./suricata-alerts
    container_name: alert-emailer
    volumes:
      - suricata_logs:/logs:ro
    depends_on:
      - suricata
    environment:
      - MAILER=SMTP
      - USERNAME=emailapikey
      - PASSWORD=VERY_SECRET_PASSWORD
      - FROM=suricata-alert@example.com
      - TO=subject1@example.com,subject2@example.com
      - SMTP_SERVER=smtp.zeptomail.com
      - PORT=587
      - POLLING_TIME=60
      - POLL_LIMIT=20
      - HOST=myserver1
```

### Example Alert Email

```
Subject: [Suricata Alert] 2 New Alert(s)

New Suricata alert(s) detected:

- ET SCAN Nmap Scripting Engine User-Agent
  Source: 192.168.1.5:42312
  Destination: 10.0.0.2:80
  Protocol: TCP
  Time: 2025-08-09T17:35:12Z

- ET POLICY External IP Lookup
  Source: 192.168.1.5:42314
  Destination: 10.0.0.5:53
  Protocol: UDP
  Time: 2025-08-09T17:36:05Z
```

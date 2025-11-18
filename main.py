from dotenv import load_dotenv
import os
import logging
from mailer import Mailer
from suricata import SuricataAlertReader
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("Starting...")

    load_dotenv()

    logging.info("Loaded enviroment variables!")

    host = os.getenv("HOST")

    mailer_type = os.getenv("MAILER")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    from_email = os.getenv("FROM")
    to_emails = os.getenv("TO").split(",")
    smtp_server = os.getenv("SMTP_SERVER")
    port = int(os.getenv("PORT"))
    polling_time = int(os.getenv("POLLING_TIME"))
    poll_limit = int(os.getenv("POLL_LIMIT"))
    details_url = os.getenv("DETAILS_URL")

    logging.info("Setting up mailer...")

    mailer = Mailer(mailer_type,port,smtp_server, username, password)

    logging.info("Setup mailer successfuly!")

    reader = SuricataAlertReader("/logs/eve.json")

    try:
        while True:
            alerts = reader.get_new_alerts()
            if len(alerts) == 0:
                time.sleep(polling_time)
                continue
            subject = f"[Suricata Alert - {host}] {len(alerts)} New Alert(s)"
            body = ["New Suricata alert(s) detected:\n"]
            poll_count = 0
            for alert in alerts:
                if poll_count >= poll_limit:
                    poll_suppressed = len(alerts) - poll_count
                    body.append(
                        f"Note: additional {poll_suppressed} alerts suppressed\n"
                    )
                    break
                poll_count += 1
                a = alert["alert"]
                body.append(
                    f"- {a['signature']}"
                )
                if "src_port" in alert and "dest_port" in alert:
                    body.append(
                        f"  Source: {alert['src_ip']}:{alert['src_port']}\n"
                        f"  Destination: {alert['dest_ip']}:{alert['dest_port']}"
                    )
                elif "src_ip" in alert and "dest_ip" in alert:
                    body.append(
                        f"  Source: {alert['src_ip']}\n"
                        f"  Destination: {alert['dest_ip']}"
                    )
                body.append(
                    f"  Protocol: {alert['proto']}\n"
                    f"  Time: {alert['timestamp']}\n"
                )
                logging.info(f"ALERT: {alert['alert']['signature']}")
            body.append(
                f"For details please see: {details_url}"
            )
            for to_email in to_emails:
                mailer.send_message(from_email, to_email, subject, "\n".join(body))
            time.sleep(polling_time)
    finally:
        reader.close()

main()

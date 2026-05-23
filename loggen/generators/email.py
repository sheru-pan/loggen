"""Email server log generator."""

import random
from typing import List

from loggen.models.log_event import LogEvent, LogLevel
from .base import BaseGenerator


class EmailGenerator(BaseGenerator):
    """Generate email server logs (phishing, BEC, spoofing)."""

    SCENARIOS = {
        "phishing": "Phishing emails with suspicious links",
        "malware_attachment": "Emails with malicious attachments",
        "bec": "Business Email Compromise attempts",
        "spoofing": "Email spoofing/header manipulation",
        "spam": "Spam emails (low-grade unsolicited)",
        "normal": "Normal business email traffic",
    }

    # Phishing subject lines (training only)
    PHISHING_SUBJECTS = [
        "URGENT: Your account will be suspended",
        "Action Required: Verify your password now",
        "Invoice #INV-{} requires immediate payment",
        "Your package delivery failed - reschedule now",
        "Microsoft Security Alert: Unusual sign-in activity",
        "Your refund of $349 is ready",
        "DocuSign: You have a document to review",
        "[IT Support] Mailbox quota exceeded",
    ]

    # Phishing domains (lookalike)
    PHISHING_DOMAINS = [
        "micros0ft-support.com",
        "amaz0n-billing.com",
        "paypa1-secure.com",
        "g00gle-account.com",
        "app1e-id.com",
        "bank-of-america-verify.tk",
        "office365-update.ml",
    ]

    # Malicious attachment names
    MALICIOUS_ATTACHMENTS = [
        "Invoice_{}.docm",
        "Report_Q4.xlsm",
        "Receipt-{}.exe",
        "Resume.docx.scr",
        "ScannedDocument.pdf.exe",
        "Order_Confirmation.html",
        "Statement.zip",
    ]

    # BEC indicators
    BEC_SUBJECTS = [
        "Urgent wire transfer needed",
        "Change of vendor banking details",
        "CEO request - need this done quickly",
        "Updated invoice - please pay ASAP",
        "Confidential request",
    ]

    def generate(self, count: int = 10, scenario: str = "phishing", **kwargs) -> List[LogEvent]:
        """Generate email logs based on scenario."""
        if scenario == "phishing":
            return self._generate_phishing(count)
        elif scenario == "malware_attachment":
            return self._generate_malware_attachment(count)
        elif scenario == "bec":
            return self._generate_bec(count)
        elif scenario == "spoofing":
            return self._generate_spoofing(count)
        elif scenario == "spam":
            return self._generate_spam(count)
        elif scenario == "normal":
            return self._generate_normal(count)
        else:
            return self._generate_phishing(count)

    def _generate_phishing(self, count: int) -> List[LogEvent]:
        """Generate phishing email logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=30, max_seconds=600)

            sender_domain = random.choice(self.PHISHING_DOMAINS)
            sender = f"noreply@{sender_domain}"
            recipient = self.faker.email()
            subject = random.choice(self.PHISHING_SUBJECTS).format(random.randint(1000, 9999))

            message = f"Phishing email blocked: From {sender} to {recipient} - Subject: {subject}"

            event = LogEvent(
                timestamp=timestamp,
                source="email",
                event_type="phishing_detected",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "sender": sender,
                    "sender_domain": sender_domain,
                    "recipient": recipient,
                    "subject": subject,
                    "action": random.choice(["quarantined", "blocked"]),
                    "phishing_score": round(random.uniform(0.7, 0.99), 2),
                    "links_found": random.randint(1, 5),
                    "spf_result": random.choice(["fail", "softfail"]),
                    "dkim_result": random.choice(["fail", "none"]),
                    "dmarc_result": "fail",
                },
            )
            events.append(event)

        return events

    def _generate_malware_attachment(self, count: int) -> List[LogEvent]:
        """Generate malicious attachment logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=60, max_seconds=900)

            sender = self.faker.email()
            recipient = self.faker.email()
            attachment = random.choice(self.MALICIOUS_ATTACHMENTS).format(
                random.randint(10000, 99999)
            )
            malware_family = random.choice(
                ["Emotet", "Trickbot", "Qakbot", "IcedID", "Dridex", "Ursnif"]
            )

            message = f"Malware attachment detected: {attachment} ({malware_family}) from {sender}"

            event = LogEvent(
                timestamp=timestamp,
                source="email",
                event_type="malware_attachment",
                level=LogLevel.CRITICAL,
                message=message,
                fields={
                    "sender": sender,
                    "recipient": recipient,
                    "attachment_name": attachment,
                    "attachment_size": random.randint(50000, 5000000),
                    "malware_family": malware_family,
                    "file_hash": self._generate_hash(),
                    "action": "quarantined",
                    "av_engine": random.choice(["ClamAV", "Sophos", "Symantec", "Trend Micro"]),
                },
            )
            events.append(event)

        return events

    def _generate_bec(self, count: int) -> List[LogEvent]:
        """Generate Business Email Compromise logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=300, max_seconds=3600)

            ceo_name = self.faker.fake.name()
            ceo_domain = self.faker.domain_name()
            spoofed_sender = f"ceo@{ceo_domain.replace('.com', '-corp.com')}"
            legitimate_sender = f"ceo@{ceo_domain}"
            recipient = f"finance@{ceo_domain}"
            subject = random.choice(self.BEC_SUBJECTS)
            amount = random.randint(10000, 500000)

            message = f"BEC attempt: Spoofed {legitimate_sender} as {spoofed_sender} - Subject: {subject} (${amount:,})"

            event = LogEvent(
                timestamp=timestamp,
                source="email",
                event_type="bec_detected",
                level=LogLevel.CRITICAL,
                message=message,
                fields={
                    "sender_displayed": legitimate_sender,
                    "sender_actual": spoofed_sender,
                    "recipient": recipient,
                    "subject": subject,
                    "amount_requested": amount,
                    "impersonated_person": ceo_name,
                    "action": "flagged",
                    "confidence": round(random.uniform(0.85, 0.99), 2),
                    "indicators": ["display_name_spoofing", "urgent_language", "wire_transfer"],
                },
            )
            events.append(event)

        return events

    def _generate_spoofing(self, count: int) -> List[LogEvent]:
        """Generate email spoofing logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=60, max_seconds=600)

            real_domain = self.faker.domain_name()
            spoofed_sender = f"admin@{real_domain}"
            actual_ip = self.faker.ipv4()
            recipient = self.faker.email()

            message = f"Email spoofing detected: Claimed sender {spoofed_sender} from unauthorized IP {actual_ip}"

            event = LogEvent(
                timestamp=timestamp,
                source="email",
                event_type="spoofing_detected",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "claimed_sender": spoofed_sender,
                    "claimed_domain": real_domain,
                    "actual_ip": actual_ip,
                    "recipient": recipient,
                    "spf_result": "fail",
                    "dkim_result": "fail",
                    "dmarc_policy": "reject",
                    "action": "rejected",
                },
            )
            events.append(event)

        return events

    def _generate_spam(self, count: int) -> List[LogEvent]:
        """Generate spam email logs."""
        events = []

        spam_categories = ["pharmaceutical", "casino", "loan", "weight_loss", "crypto", "marketing"]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=30, max_seconds=300)

            sender = self.faker.email()
            recipient = self.faker.email()
            category = random.choice(spam_categories)

            message = f"Spam email blocked: From {sender} to {recipient} (category: {category})"

            event = LogEvent(
                timestamp=timestamp,
                source="email",
                event_type="spam_detected",
                level=LogLevel.INFO,
                message=message,
                fields={
                    "sender": sender,
                    "recipient": recipient,
                    "category": category,
                    "spam_score": round(random.uniform(5.0, 10.0), 1),
                    "action": "rejected",
                    "rule_id": f"SPAM-{random.randint(100, 999)}",
                },
            )
            events.append(event)

        return events

    def _generate_normal(self, count: int) -> List[LogEvent]:
        """Generate normal email traffic logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=10, max_seconds=300)

            sender = self.faker.email()
            recipient = self.faker.email()
            subject = self.faker.fake.sentence(nb_words=6)

            message = f"Email delivered: From {sender} to {recipient} - Subject: {subject}"

            event = LogEvent(
                timestamp=timestamp,
                source="email",
                event_type="email_delivered",
                level=LogLevel.INFO,
                message=message,
                fields={
                    "sender": sender,
                    "recipient": recipient,
                    "subject": subject,
                    "message_size": random.randint(1000, 100000),
                    "spf_result": "pass",
                    "dkim_result": "pass",
                    "dmarc_result": "pass",
                    "delivery_time_ms": random.randint(50, 500),
                },
            )
            events.append(event)

        return events

    @staticmethod
    def _generate_hash() -> str:
        """Generate a random hash."""
        return "".join(random.choices("0123456789abcdef", k=64))

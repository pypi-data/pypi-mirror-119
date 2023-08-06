# SMTP Mail

# Usage
```py
    import smtpmail
    import os

    sender = os.getenv('smpt_sender')
    pswd = os.getenv('smtp_pass')
    host = os.getenv('smtp_host', 'smtp.gmail.com')
    port = os.getenv('smtp_port', 587)
    read_only_settings: smtpmail.Settings = smatpmail.Mail.init(sender, pswd, host, port)
    ###
    smtpmail.Mail.send_mail(to, subject, content, content_type='plain')
```
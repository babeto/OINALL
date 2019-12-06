
from ntlm3 import ntlm
import base64
from smtplib import SMTPException, SMTPAuthenticationError

SMTP_EHLO_OKAY = 250
SMTP_AUTH_CHALLENGE = 334
SMTP_AUTH_OKAY = 235

def ntlm_authenticate(smtp, username, password):
    # Send the NTLM Type 1 message -- Authentication Request
    msg = ntlm.create_NTLM_NEGOTIATE_MESSAGE(username)
    print(msg)
    code, response = smtp.docmd("AUTH", "NTLM " + ntlm.create_NTLM_NEGOTIATE_MESSAGE(username).decode())
    if code != SMTP_AUTH_CHALLENGE:
        raise SMTPException("Server did not respond as expected to NTLM negotiate message")
    challenge, flags = ntlm.parse_NTLM_CHALLENGE_MESSAGE(response)
    user_parts = username.split("\\", 1)
    DomainName = user_parts[0].upper()
    UserName = user_parts[1]
    msg = ntlm.create_NTLM_AUTHENTICATE_MESSAGE(challenge, UserName, DomainName, password, flags)
    print(msg)
    code, response = smtp.docmd(
        "", ntlm.create_NTLM_AUTHENTICATE_MESSAGE(challenge, UserName, DomainName, password, flags).decode())
    print(code)
    if code != SMTP_AUTH_OKAY:
        raise SMTPAuthenticationError(code, response)

from email.mime.text import MIMEText
import smtplib
import traceback


class Email(object):
    """description of class"""
    host = 'smtphost.gtm.corp.microsoft.com'
    sender = 'cmseauto@microsoft.com'
    password = 'User@123@ShanghaiNovaElvis6'
    domain = 'fareast'
    body = 'Report.html'
    subject = 'Shanghai and Redmond Hosts/VMs Monthly Patch Report'

    @classmethod
    def send(Email, to, subject, body):
        with open(body, 'rb') as fp:
            msg = MIMEText(fp.read(), 'html', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = Email.sender
        msg['To'] = to
        try:
            server = smtplib.SMTP(Email.host, '25')
            server.set_debuglevel(0)
            #server.connect()
            server.ehlo()
            loginname = '\\'.join([Email.domain, Email.sender.split('@')[0]])
            ntlm_authenticate(server, loginname, Email.password)
            server.sendmail(msg['From'], msg['To'].split(","), msg.as_string())
            server.quit()
            print('sent mail succeed!')
        except Exception as e:
            print('send mail failed!')
            traceback.print_exc()

if __name__ == '__main__':
    Email.send('v-alhuan@microsoft.com', Email.subject, Email.body)

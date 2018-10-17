from email.mime.text import MIMEText
import smtplib




def create_message(from_addr, to_addrs, subject, text):
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    return msg


def send(host, user, password, message):
    s = smtplib.SMTP_SSL(host)
    s.login(user, password)
    s.send_message(message)
    s.quit()


def email_main(message_text):
    msg=create_message('kaili17@mails.jlu.edu.cn',['2630582744@qq.com'],'Test Title',message_text)
    send('mails.jlu.edu.cn','kaili17@mails.jlu.edu.cn','lk15131416',msg)

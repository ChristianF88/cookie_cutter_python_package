import smtplib
from email.message import EmailMessage


class EmailEawag:
    """
    A lightweight interface to use the Eawag SMTP server.
    !You must be in the intranet to use this smtp server!
    """
    __host = "smtp.eawag.ch"
    __port = 25

    def __init__(self, sender):
        """
        Parameter
        ---------

        sender : str
            specifying where the email is from -> eg: service@eawag.ch or another_name@eawag.ch
        recipient : str, list
            specifying wo to send the mail to -> eg: "christian.foerster@eawag.ch" or "christian.foerster@eawag.ch, simon.dicht@eawag.ch"
            You can also pass single mail addresses in a list!
        subject : str
            subject of email
        message : str
            the email's message/content

        Examples
        --------

        ## create email instance
        email=MailEawag("my_service@eawag.ch")

        ## multiple recipiants with list
        email.send(
            [
                "christian.foerster@eawag.ch",
                "other_people@eawag.ch"
            ],
            "IMPORTANT",
            "This is a very important notification!!!"
        )

        ## multiple recipiants with list
        email.send(
            "christian.foerster@eawag.ch, other_people@eawag.ch"
            "IMPORTANT2",
            "This is also a very important notification!!!"
        )

        ## single recipiant
        email.send(
            "christian.foerster@eawag.ch"
            "IMPORTANT3",
            "This is still a very important notification!!!"
        )

        """
        self._msg = EmailMessage()
        self._msg['From'] = sender

    def send(self, recipient, subject, message):
        """
        This method sets the recipiant(s), subject, email text and sends the email.

        Parameter
        ---------

        recipient : str, list
            specifying wo to send the mail to -> eg: "christian.foerster@eawag.ch" or "christian.foerster@eawag.ch, simon.dicht@eawag.ch"
            You can also pass single mail addresses in a list!
        subject : str
            subject of email
        message : str
            the email's message/content
        """

        self._msg.set_content(message)

        del self._msg['Subject']
        self._msg['Subject'] = subject

        del self._msg['To']
        self._msg['To'] = recipient if not isinstance(recipient, list) else ", ".join(recipient)

        s = smtplib.SMTP(host=self.__host, port=self.__port)
        s.send_message(self._msg)
        s.quit()

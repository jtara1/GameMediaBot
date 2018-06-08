from yagmail import SMTP


class Emailer:
    def __init__(self,
                 email='',
                 gmail_oauth2_file='',
                 email_csv=''):
        """Sends emails

        :param email: <str> sender's email
        :param gmail_oauth2_file: file path to a json file that contains \n
            google_client_id, \n
            google_client_secret, google_refresh_token as specified by \n
            yagmail
        :param email_csv: <str> csv with columns of email and opt-in \n
            with opt-in values being 0 or 1
        """
        self.email = email
        self.email_csv = email_csv
        self.server = None
        if email and gmail_oauth2_file:
            self.server = SMTP(email, oauth2_file=gmail_oauth2_file)

    def send_to_all(self, subject, contents):
        if self.server:
            with open(self.email_csv, 'r') as file:
                file.readline()
                for line in file:
                    to, opt_in, *_ = line.split(',')
                    if to and int(opt_in):
                        self.server.send(to, subject, contents)
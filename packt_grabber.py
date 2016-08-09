import requests
from bs4 import BeautifulSoup
import cred
from twilio.rest import TwilioRestClient

email    = 'diwahar.sivaraman@gmail.com'
password = 'GQeb4dFEu76yJtxLhCJj0Q=='

#Enter your Twilio account SID and Auth Token
accountSid = ""
authToken = ""

myTwilioNumber = "+1xxxx" #Twilio Sender number.  This must be a number that can send outgoing messages
destCellPhone = "xxxx" # Verified Number by Twilio.com

form_url = 'https://www.packtpub.com/packt/offers/free-learning'

def claim_book(form_url, email, password):
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    s = requests.Session()
    r = requests.get(form_url, headers=hdr)
    soup = BeautifulSoup(r.text)
    h2 = soup.find('div', {'class': 'dotd-title'}).find('h2').next_element.replace('\t', '').replace('\n', '').strip(' ')
    print h2

    form = soup.find(attrs={"name": "form_build_id"})
    if not form:
       # print 'Cannot find login form'
        return
    twilioClient = TwilioRestClient(accountSid, authToken)
    payload = {
        'email': email,
        'password': cred.getpasswd(password),
        'op': 'Login',
        'form_build_id': form.id,
        'form_id': 'packt_user_login_form'
    }
    r = s.post(form_url, headers=hdr, data=payload)
    soup = BeautifulSoup(r.text)

    if soup.find('div', class_='error'):
       # print 'Login failed'
        return

    url = soup.find(attrs={'class':'twelve-days-claim'})['href']

    if not url:
        print 'Failed to find claim url'

    r = s.get('https://www.packtpub.com'+url, headers=hdr)

    if r.status_code == 200:
        print 'Success'
        # sends a text from fromnumber to to number consisting of body_text
        twilioClient.messages.create(to="+919901035150", from_="+12019928417",body="Book Fetched:" + h2)
    else:
        print 'Error claiming book'

    # messages error


if __name__ == "__main__":
    claim_book( form_url, email, password)

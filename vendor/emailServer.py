import requests
from django.conf import settings

API_KEY= settings.EMAIL_SERVER_API_KEY

      
def VendorRegistrationEmail(
            email,
            vendor,
            brand,
      ):
      # (ref, date, fullname, email, vendor, university,description,vehicle_number,seats,dept_time,terminal,amount)
      return requests.post(
      "https://api.mailgun.net/v3/hallmarts.com/messages",
      auth=("api", API_KEY),
      data={"from": "Jasmine from Hallmarts <admin@hallmarts.com>",
            "subject": "Hallmarts Vendor Waitlist",
            "to": [email],
            "html": "<div style='font-family: Helvetica,Arial,sans-serif;background: #f6f6f6; height: 100%; line-height: 1.3em;'><div style='background: #ffff;padding: 2%;'><div style='margin: 0.6rem 0'><p style=' box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 5px 0;'>Hi {0},</p><p style=' box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 5px 0;'>I am Jasmine from Hallmarts.</p><p style=' box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 5px 0; font-weight:bold'>Thank you for joining the Hallmarts waitlist!</p><p style=' box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 5px 0;'>Hallmarts is a digital marketing platform for supporting and promoting student entreprenuership activities, models, brands and university business models. </p><p style=' box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 5px 0;'>We will send you an invite to get your university business running online soon!</p></div><div><p>Store name: <span style='font-weight:bold'>{1}</span></p><p>Hallmarts team</p><p>&copy;  Hallmarts. 2022</p></div></div></div>".format(vendor, brand)})

from django import template
from hashlib import md5

register = template.Library()

# Calculate an md5 hash as checksum for payment service
@register.simple_tag(name='getChecksum')
def getChecksum(amount, pid):
    sid = "" # Not shown in a public git repository
    secret_key = "" # Not shown in a public git repository
    check = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
    m = md5(check.encode(encoding='ascii', errors='strict'))
    checksum = m.hexdigest()
    return checksum

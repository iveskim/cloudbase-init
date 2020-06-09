import urllib


def set_password(username, password):
    from win32com import adsi
    ads_obj = adsi.ADsGetObject("WinNT://localhost/%s,user" % username)
    ads_obj.Getinfo()
    ads_obj.SetPassword(password)


def verify_success(username, password):
    from win32security import LogonUser
    from win32con import LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT
    try:
        LogonUser(username, None, password, LOGON32_LOGON_INTERACTIVE, LOGON32_PROVIDER_DEFAULT)
    except:
        return False
    return True


response = urllib.urlopen('http://169.254.169.254/2009-04-04/meta-data/initial-password')

if response.getcode() == 200:

    u = "Administrator"
    p = response.read()

    if p == "":
        print "Error: Empty Password!"
        exit(1)

    set_password(u, p)

    if verify_success(u, p):
        print "Password Changed"
        exit(0)
    else:
        print "Password Change Failed"
        exit(1)
else:
    print "Failed to get password"
    print response.getcode()
    exit(1)
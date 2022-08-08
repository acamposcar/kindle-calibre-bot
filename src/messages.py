

def help():
    return('''
Hello Human! 🤖 You can use me to send eBooks or documents to your Kindle or to convert and download them to your device. 

The maximum file size is <b>20MB</b>.

*************

If you want to receive the eBooks in your Kindle you need to follow these steps:

<b>1.-</b> Send me your @kindle email address.

    For example: johndoe@kindle.com

    To find your @kindle e-mail address, visit the <a href='https://www.amazon.com/myk#manageDevices'>Manage your Devices</a> page.

<b>2.-</b> Add kindlesendbot@gmail.com in your <a href='https://www.amazon.com/gp/help/customer/display.html?nodeId=GX9XLEVV8G4DB28H'>Approved Personal Document E-mail List</a>.

If you need more help, you can use this <a href='https://mytbr.co/how-to-email-books-to-kindle/'>step-by-step guide</a>.

*************

I can work with the following file types:
AZW, AZW3, AZW4, CBZ, CBR, CBC, CHM, DJVU, DOCX, EPUB, FB2, FBZ, HTML, HTMLZ, LIT, LRF, MOBI, ODT, PDF, PRC, PDB, PML, RB, RTF, SNB, TCR, TXT, TXTZ

Keep in mind that PDF documents are one of the worst formats to convert from. Best source formats in order of decreasing preference are: MOBI, AZW, EPUB, LIT, AZW3, FB2, FBZ, DOCX.

*************

Commands available:
 /help - Shows this message
 /email - Shows your kindle email stored in the database
 /delete - Deletes your user and kindle email from the database
 
*************
 
To get started, send me a eBook that you want to send to your Kindle or that you want to convert to another format.''')


def save_email(email):
    return (f'''
✅ Email saved: {email}

To receive eBooks in your Kindle, you will need to add botkindlesend@gmail.com in your <a href='https://www.amazon.com/gp/help/customer/display.html/?nodeId=200767340#approvefrom'>Approved Personal Document E-mail List</a>

If you don't know how to do it, you can use this <a href='https://mytbr.co/how-to-email-books-to-kindle/'>step-by-step guide</a>.''')


def get_email(email):
    return(f'''
ℹ️ Your email is {email}

If you want to update your email, just send me your new @kindle email address.

If you want to delete your email from the database, send me /delete command''')


def update_email():
    return(f'''
ℹ️ If you want to receive the eBook in your Kindle you need to send me your @kindle email address.

    For example: johndoe@kindle.com

To find your @kindle e-mail address, visit the <a href='https://www.amazon.com/myk#manageDevices'>Manage your Devices</a> page.

If you don't know how to do it, you can use this <a href='https://mytbr.co/how-to-email-books-to-kindle/'>step-by-step guide</a>.''')


def file_extension_not_valid():
    return(f'''
❌ The file extension is not valid. I can work with the following file types:

AZW, AZW3, AZW4, CBZ, CBR, CBC, CHM, DJVU, DOCX, EPUB, FB2, FBZ, HTML, HTMLZ, LIT, LRF, MOBI, ODT, PDF, PRC, PDB, PML, RB, RTF, SNB, TCR, TXT, TXTZ''')



def conversion(file_name, extension_input, extension_output):
    return(f'''
🛠️ Converting "{file_name}" 

{extension_input} ➡️ {extension_output}

Please wait...''')
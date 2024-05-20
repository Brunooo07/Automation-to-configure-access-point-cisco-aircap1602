Here is the script to configure the ap's for a flexconnect controller.
The user must have a console cable and have Python 3.12 installed on their PC.
Open your terminal and type:
pip install pyserial
pip installation time
So, press the mode button, plug the cable console into the port console, and then plug in an Ethernet cable connecting a Poe switch. Keep pressing the button until a red light appears, then you can release the button.
"#####################################"
The next step is to install the Google API libs:
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

#To remember#
You must the files in this case token.json and credentials.json. These files are essential for you to manipulate the spreadsheets.
Remember to run the serial_connection script as soon as you connect the console cable. After executing, enter the serial port.
After configuring the Ap, a Macs.txt file will be created, from this file the googlesheets script will take the mac's and add them to a spreadsheet.
Good job!

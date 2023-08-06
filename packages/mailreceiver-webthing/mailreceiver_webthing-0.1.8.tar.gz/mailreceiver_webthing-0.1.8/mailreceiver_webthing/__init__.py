from mailreceiver_webthing.mail_receiver_webthing import run_server
from mailreceiver_webthing.app import App
from string import Template
from typing import Dict
import os


PACKAGENAME = 'mailreceiver_webthing'
ENTRY_POINT = "mailreceiver"
DESCRIPTION = "A web connected mail receiver"


UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --port $port --mailserver_port $mailserver_port --to_pattern $to_pattern $passwordfile_entry
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
''')



def parse_credentials(credentials) -> Dict[str, str]:
    user_pwd_list = {}
    for part in credentials.split(" "):
        idx = part.index(":")
        if idx > 0:
            user = part[:idx]
            pwd = part[idx+1:]
            part[user] = pwd
            print("user '" + user + "'")
            print("pwd '" + pwd + "'")
            user_pwd_list[user] = pwd
    return user_pwd_list



class InternetApp(App):

    def do_add_argument(self, parser):
        parser.add_argument('--mailserver_port', metavar='mailserver_port', required=False, type=int, default=25, help='the port number of the mail server')
        parser.add_argument('--to_pattern', metavar='to_pattern', required=False, type=str, default=".*@.*", help='the regex pattern of the receiver address to be matched')
        parser.add_argument('--passwordfile', metavar='passwordfile', required=False, type=str, help='the password file (username and password pair (separated by colon) per line)')

    def do_additional_listen_example_params(self):
        return "--mailserver_port 25 --to_pattern system.231.233@example.org"

    def do_process_command(self, command:str, port: int, verbose: bool, args) -> bool:
        if command == 'listen' and (args.mailserver_port > 0):
            run_server(port, args.mailserver_port, args.to_pattern, self.description, args.passwordfile)
            return True
        elif args.command == 'register' and (args.mailserver_port > 0):
            print("register " + self.packagename + " on port " + str(args.port))
            passwordfile_entry = "" if args.passwordfile is None else "--passwordfile " + args.passwordfile
            unit = UNIT_TEMPLATE.substitute(packagename=self.packagename, entrypoint=self.entrypoint, port=port, mailserver_port=args.mailserver_port, to_pattern=args.to_pattern, passwordfile_entry=passwordfile_entry, verbose=verbose)
            self.unit.register(port, unit)
            return True
        else:
            return False

def main():
    InternetApp(PACKAGENAME, ENTRY_POINT, DESCRIPTION).handle_command()


if __name__ == '__main__':
    main()



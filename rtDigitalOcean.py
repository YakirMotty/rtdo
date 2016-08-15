import logging
from configparser import ConfigParser
from digitalocean import Droplet, Manager, SSHKey
from pexpect import pxssh
import commands
import time


def read_config(title: str = None, key: str = None) -> str or dict:
    config = ConfigParser()
    config.read('config.ini')
    if not title or not key:
        result = dict()
        for k in config.sections():
            result[k] = dict(config[k])
        return result
    return config[title][key]


class Cli:
    def __init__(self, ip_address):
        logging.basicConfig(filename='myapp.log', level=logging.INFO, filemode='w', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.ip_address = ip_address
        logging.info('ip address: {}'.format(self.ip_address))
        self.connect = self.login_server()

    def read(self, cmd):
        self.connect.sendline(cmd)
        self.connect.prompt()
        result = bytes(self.connect.before).decode()
        print(result)
        return result

    def login_server(self):
        connect = pxssh.pxssh()
        connect.SSH_OPTS += " -o StrictHostKeyChecking=no"
        connect.login(server=self.ip_address, username='root')
        return connect

    def first_steps(self, image):
        for ins in commands.first_steps[image]:
            print(ins)
            logging.info(self.read(ins))

    def go_server2(self):
        logging.info(self.read('ls -a'))

    def install_lamp(self, image):
        for ins in commands.lamp_cmd[image]:
            logging.info(self.read(ins))


class MyDigitalocean:
    def __init__(self):
        self.my_token = read_config('tokens', 'yakir')
        self.manager = Manager(token=self.my_token)

    def names(self):
        return [i.name for i in self.manager.get_all_droplets()]

    def create_droplet(self, name, **kwargs):
        keys = self.manager.get_all_sshkeys()

        details = dict(token=self.my_token,
                       name=name,
                       region='fra1',
                       image='18574245',  # CentOS 6.8 x64
                       size_slug='512mb',
                       ssh_keys=keys,
                       backups=True)
        details.update(**kwargs)
        if details['name'] in self.names():
            raise ValueError('Droplet name "{}" exists'.format(details['name']))
        droplet = Droplet(**details)
        droplet.create()
        return droplet

    def create_ssh(self, path_ssh, name):
        user_ssh_key = open(path_ssh).read()
        key = SSHKey(token=self.my_token,
                     name=name,
                     public_key=user_ssh_key)
        key.create()

    def get_droplet(self, name) -> Droplet:
        for droplet in self.manager.get_all_droplets():
            if droplet.name == name:
                return droplet
        raise ValueError('No droplet named ' + name)

    def get_id_by_name(self, name):
        return self.get_droplet(name).id

    def get_ip_by_name(self, name: str) -> str:
        return self.get_droplet(name).ip_address

    def destroy_droplet(self, name: str) -> dict:
        return self.get_droplet(name).destroy()


        return self.get_droplet(name).shutdown()

    def rename_droplet(self, name, new_name):
        return self.get_droplet(name).rename(new_name)

    def take_snapshot(self, name, snapshot_name):
        return self.get_droplet(name).take_snapshot(snapshot_name=snapshot_name)


def main():
    dig = MyDigitalocean()
    dig.create_droplet(name='firstVm', image='18830380')
    time.sleep(10)
    # cli = Cli(dig.get_ip_by_name(name='firstVm' ))
    # cli.first_steps(image='CentOS_6')
    # cli.install_lamp(image='CentOS_6')
    #
    # dig.create_ssh(os.path.expanduser('~') + '/.ssh/id_rsa.pub', 'moty')
    # dig.create_droplet(name='firstVm' )
    # print(dig.get_id_by_name(name='firstVm'))
    print(dig.get_ip_by_name(name='firstVm'))
    # dig.destroy_droplet(name='firstVm')
    # dig.shutdown_droplet(name='firstVm')
    # dig.rename_droplet(name='firstVm1', new_name="firstVm")
    # dig.take_snapshot(name='firstVm', snapshot_name='Take Snapshot test')
    # for i in dig.manager.get_all_images():
    #     if i.distribution == 'Ubuntu':
    #         print(i)

if __name__ == '__main__':
    main()

import logging
import logging.handlers
import configparser
import paramiko
import select
import getpass
import requests
import pathlib
import time
import sys
import os


def get_config_dir():

    return os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../conf"))


def read_config(config_name):

    config = configparser.ConfigParser()
    config_file = os.path.join(get_config_dir(), config_name)
    try:
        config.read(config_file)
    except ConfigParser.Error as e:
        print(f"Couldn't parse file: {config_file}- {e}")
        sys.exit(1)

    return config


def get_auth():
    
    username = getpass.getuser()
    password = getpass.getpass(prompt=f"Enter password for {username}: ")
    
    return username,password


def configure_logger(log_name):
    
    if not os.path.exists("/opt/hq/logs"):
        pathlib.Path("/opt/hq/logs").mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(f"{log_name}")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    fh = logging.FileHandler(f"/opt/hq/logs/{log_name}")
    sh = logging.StreamHandler(sys.stdout)
    lh = logging.handlers.SysLogHandler()
    fmtstr = "[%(asctime)s] %(levelname)s [%(name)s] %(message)s"
    formatter = logging.Formatter(fmtstr, datefmt="%a, %d %b %Y %H:%M:%S")
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    lh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.addHandler(lh)


def remote_exec(ssh, host, cmd, timeout=0.0):
    
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host)

    stdin, stdout, stderr = ssh.exec_command(cmd) 
    channel = stdout.channel

    stdin.close()                 
    channel.shutdown_write()      

    stdout_chunks = []
    stdout_chunks.append(stdout.channel.recv(len(stdout.channel.in_buffer)).decode('UTF-8'))
    while not channel.closed or channel.recv_ready() or channel.recv_stderr_ready(): 
        got_chunk = False
        readq, _, _ = select.select([stdout.channel], [], [], timeout)
        for c in readq:
            if c.recv_ready(): 
                stdout_chunks.append(stdout.channel.recv(len(c.in_buffer)).decode('UTF-8'))
                got_chunk = True
            if c.recv_stderr_ready(): 
                stderr.channel.recv_stderr(len(c.in_stderr_buffer))  
                got_chunk = True  
        
        if not got_chunk \
            and stdout.channel.exit_status_ready() \
            and not stderr.channel.recv_stderr_ready() \
            and not stdout.channel.recv_ready(): 
            stdout.channel.shutdown_read()  
            stdout.channel.close()
            # exit as remote side is finished and our bufferes are empty
            break

    stdout.close()
    stderr.close()

        return ''.join(stdout_chunks)


def progressbar(it, prefix="", size=60, fi=sys.stdout):
    """Display a simple progress bar in the terminal.

    Args:
        it: Any iterable

    Usage:
        for i in progrssbar(range(15)), "Computing: ", 40):
            do_stuff()
    """
    
    count = len(it)
    def show(j):
        x = int(size*j/count)
        fi.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        fi.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    fi.write("\n")
    fi.flush()

def ping(ip):
    """ping a host to test connectivity.

    Args:
        ip (str): IP address of the host to ping

    Returns:
        return code of the ping command
    """
    command = ["ping", "-c", "1", ip]

    return run(command).returncode == 0
'''
    def fetcher(self, url, query):

        offset = 0
        limit = self.getlimit
        result = defaultdict(list)
        try:
            query = urlencode(json.loads(query))
        except ValueError as e:
            pass

        while True:
            qurl = url + "/?offset=" + str(offset) + "&limit=" + str(limit) + "&" + query
            r = requests.get(qurl, auth=(self.username, self.password), verify=False)
            newresult = r.json()
            # empty results
            if "total_count" not in newresult:
                return newresult
            # merge results except for paging control results
            for key, value in newresult.items():
                if key == "limit" or key == "total_count" or key == "offset":
                    result[key] = newresult[key]
                    continue
                else:
                    result[key].extend(value)
            offset += result["limit"]
            if offset >= result["total_count"]:
                return result

    def apiquery(self, path, query):

        url = self.base_url + "/api/1.0/" + path
        return self.fetcher(url, query)

    def uploader(self, url, data, method="post", headers={"Content-Type": "application/x-www-form-urlencoded"}):

        if self.username == self.ro_user:
            self.get_auth()

        params = data
        if method == "put":
            r = requests.put(url, data=params, auth=(self.username, self.password), verify=False, headers=headers)
        elif method == "post":
            r = requests.post(url, data=params, auth=(self.username, self.password), verify=False, headers=headers)
        else:
            print(f"Invalid upload method: {method}")

        try:
            return r.json()
        except Exception as e:

            print("\n[*] Exception: %s" % str(e))
            pass

    def apipost(self, path, data):

        url = self.base_url + "/api/1.0/" + path + "/"
        return self.uploader(url, data)

    def apiput(self, path, data):

        url = self.base_url + "/api/1.0/" + path + "/"
        return self.uploader(url, data, method="put")

    def deleter(self, url, item):

        if self.username == self.ro_user:
            self.get_auth()

        qurl = url + "/" + item + "/" + "?id=" + item

        r = requests.delete(qurl, auth=(self.username, self.password), verify=False)
        try:
            return r.json()
        except Exception as e:

            print("\n[*] Exception: %s" % str(e))
            pass

    def apidelete(self, path, item):

        # url = self.base_url + "/api/1.0/" + path + "/" + str(item) + "/"
        url = self.base_url + "/api/1.0/" + path
        return self.deleter(url, item)


    def read_json(self, datafile):

        with open(datafile) as json_file:
            try:
                return json.load(json_file)
            except JSONDecodeError:
                return {}
    
'''
    

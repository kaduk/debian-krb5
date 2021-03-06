# Copyright (C) 2010 by the Massachusetts Institute of Technology.
# All rights reserved.

# Export of this software from the United States of America may
#   require a specific license from the United States Government.
#   It is the responsibility of any person or organization contemplating
#   export to obtain such a license before exporting.
#
# WITHIN THAT CONSTRAINT, permission to use, copy, modify, and
# distribute this software and its documentation for any purpose and
# without fee is hereby granted, provided that the above copyright
# notice appear in all copies and that both that copyright notice and
# this permission notice appear in supporting documentation, and that
# the name of M.I.T. not be used in advertising or publicity pertaining
# to distribution of the software without specific, written prior
# permission.  Furthermore if you modify this software you must label
# your software as modified software and not distribute it in such a
# fashion that it might be confused with the original M.I.T. software.
# M.I.T. makes no representations about the suitability of
# this software for any purpose.  It is provided "as is" without express
# or implied warranty.

"""A module for krb5 test scripts

To run test scripts during "make check" (if Python 2.4 or later is
available), add rules like the following to Makeflie.in:

    check-pytests::
	$(RUNPYTEST) $(srcdir)/t_testname.py $(PYTESTFLAGS)

A sample test script:

    from k5test import *

    # Run a test program under a variety of configurations:
    for realm in multipass_realms():
        realm.run_as_client(['./testprog', 'arg'])

    # Run a test server and client under just the default configuration:
    realm = K5Realm()
    realm.start_server(['./serverprog'], 'starting...')
    realm.run_as_client(['./clientprog', realm.host_princ])

    # Inform framework that tests completed successfully.
    success('World peace and cure for cancer.')

By default, the realm will have:

* The name KRBTEST.COM
* Listener ports starting at 61000
* Four different krb5.conf files for the client, server, master KDC,
  and slave KDC, specifying only the variables necessary for
  self-contained test operation
* Two different kdc.conf files for the master and slave KDCs
* A fresh DB2 KDB
* Running krb5kdc and kadmind processes
* Principals named realm.user_princ and realm.admin_princ; call
  password('user') and password('admin') to get the password
* Credentials for realm.user_princ in realm.ccache
* Admin rights for realm.admin_princ in the kadmind acl file
* A host principal named realm.host_princ with a random key
* A keytab for the host principal in realm.keytab

The realm's behaviour can be modified with the following constructor
keyword arguments:

* realm='realmname': Override the realm name

* portbase=NNN: Override the listener port base; currently three ports are
  used

* testdir='dirname': Override the storage area for the realm's files
  (path may be specified relative to the current working dir)

* krb5_conf={ ... }: krb5.conf options, expressed as a nested
  dictionary, to be merged with the default krb5.conf settings.  The
  top level keys of the dictionary should be 'all' to apply to all
  four krb5.conf files, and/or 'client'/'server'/'master'/'slave' to
  apply to a particular one.  A key may be mapped to None to delete a
  setting from the defaults.  A key may be maped to a list in order to
  create multpile settings for the same variable name.  Keys and
  values undergo the following template substitutions:

    - $type:     The configuration type (client/server/master/slave)
    - $realm:    The realm name
    - $testdir:  The realm storage directory (absolute path)
    - $buildtop: The root of the build directory
    - $srctop:   The root of the source directory
    - $plugins:  The plugin directory under $buildtop/util/fakedest
    - $hostname: The FQDN of the host
    - $port0:    The first listener port (portbase)
    - ...
    - $port9:    The tenth listener port (portbase + 9)

  When choosing ports, note the following:

    - port0 is used in the default krb5.conf for the KDC
    - port1 is used in the default krb5.conf for kadmind
    - port2 is used in the default krb5.conf for kpasswd
    - port3 is the return value of realm.server_port()

* kdc_conf={...}: kdc.conf options, expressed as a nested dictionary,
  to be merged with the default kdc.conf settings.  The top level keys
  should be 'all' or 'master'/'slave'.  The same conventions and
  substitutions for krb5_conf apply.

* create_kdb=False: Don't create a KDB.  Implicitly disables all of
  the other options since they all require a KDB.

* krbtgt_keysalt='enctype:salttype': After creating the KDB,
  regenerate the krbtgt key using the specified key/salt combination,
  using a kadmin.local cpw query.

* create_user=False: Don't create the user principal.  Implies
  get_creds=False.

* create_host=False: Don't create the host principal or the associated
  keytab.

* start_kdc=False: Don't start the KDC.  Implies get_creds=False.

* start_kadmind=False: Don't start kadmind.

* get_creds=False: Don't get user credentials.

Scripts may use the following functions and variables:

* fail(message): Display message (plus leading marker and trailing
  newline) and explanatory messages about debugging.

* success(message): Indicate that the test script has completed
  successfully.  Suppresses the display of explanatory debugging
  messages in the on-exit handler.  message should briefly summarize
  the operations tested; it will only be displayed (with leading
  marker and trailing newline) if the script is running verbosely.

* output(message, force_verbose=False): Place message (without any
  added newline) in testlog, and write it to stdout if running
  verbosely.

* password(name): Return a weakly random password based on name.  The
  password will be consistent across calls with the same name.

* stop_daemon(proc): Stop a daemon process started with
  realm.start_server() or realm.start_in_inetd().  Only necessary if
  the port needs to be reused; daemon processes will be stopped
  automatically when the script exits.

* multipass_realms(**keywords): This is an iterator function.  Yields
  a realm for each of the standard test passes, each of which alters
  the default configuration in some way to exercise different parts of
  the krb5 code base.  keywords may contain any K5Realm initializer
  keyword with the exception of krbtgt_keysalt, which will not be
  honored.  If keywords contains krb5_conf and/or kdc_conf fragments,
  they will be merged with the default and per-pass specifications.

* buildtop: The top of the build directory (absolute path).

* srctop: The top of the source directory (absolute path).

* plugins: The plugin directory under <buildtop>/util/fakedest.

* hostname: This machine's fully-qualified domain name.

* null_input: A file opened to read /dev/null.

* args: Positional arguments left over after flags are processed.

* verbose: Whether the script is running verbosely.

* testpass: The command-line test pass argument.  The script does not
  need to examine this argument in most cases; it will be honored in
  multipass_realms().

* Pathname variables for programs within the build directory:
  - krb5kdc
  - kadmind
  - kadmin
  - kadmin_local
  - kdb5_util
  - ktutil
  - kinit
  - klist
  - kswitch
  - kvno
  - kdestroy
  - kpasswd
  - t_inetd
  - kproplog
  - kpropd
  - kprop

Scripts may use the following realm methods and attributes:

* realm.run_as_client(args, **keywords): Run a command with an
  environment pointing at the client krb5.conf, obeying the
  command-line debugging options.  Fail if the command does not return
  0.  Log the command output appropriately, and return it as a single
  multi-line string.  Keyword arguments can contain input='string' to
  send an input string to the command, and expected_code=N to expect a
  return code other than 0.

* Similar methods for the server, master KDC, and slave KDC
  environments:
  - realm.run_as_server
  - realm.run_as_master
  - realm.run_as_slave

* realm.server_port(): Returns a port number based on realm.portbase
  intended for use by server processes.

* realm.start_server(args, sentinel): Start a process in the server
  environment.  Wait until sentinel appears as a substring of a line
  in the server process's stdout or stderr (which are folded
  together).  Returns a subprocess.Popen object which can be passed to
  stop_daemon() to stop the server, or used to read from the server's
  output.

* realm.start_in_inetd(args, port=None): Begin a t_inetd process which
  will spawn a server process within the server environment after
  accepting a client connection.  If port is not specified,
  realm.server_port() will be used.  Returns a process object which
  can be passed to stop_daemon() to stop the server.

* realm.create_kdb(): Create a new master KDB.

* realm.start_kdc(args=[]): Start a krb5kdc with the realm's master
  KDC environment.  Errors if a KDC is already running.  If args is
  given, it contains a list of additional krb5kdc arguments.

* realm.stop_kdc(): Stop the krb5kdc process.  Errors if no KDC is
  running.

* realm.start_kadmind(): Start a kadmind with the realm's master KDC
  environment.  Errors if a kadmind is already running.

* realm.stop_kadmind(): Stop the kadmind process.  Errors if no
  kadmind is running.

* realm.stop(): Stop any KDC and kadmind processes running on behalf
  of the realm.

* realm.addprinc(princname, password=None): Using kadmin.local, create
  a principle in the KDB named princname, with either a random or
  specified key.

* realm.extract_keytab(princname, keytab): Using kadmin.local, create
  a keytab for princname in the filename keytab.  Uses the -norandkey
  option to avoid re-randomizing princname's key.

* realm.kinit(princname, password=None, flags=[]): Acquire credentials
  for princname using kinit, with additional flags [].  If password is
  specified, it will be used as input to the kinit process; otherwise
  flags must cause kinit not to need a password (e.g. by specifying a
  keytab).

* realm.klist(client_princ, service_princ=None, ccache=None): Using
  klist, list the credentials cache ccache (must be a filename;
  self.ccache if not specified) and verify that the output shows
  credentials for client_princ and service_princ (self.krbtgt_princ if
  not specified).

* realm.klist_keytab(princ, keytab=None): Using klist, list keytab
  (must be a filename; self.keytab if not specified) and verify that
  the output shows the keytab name and principal name.

* realm.run_kadminl(query): Run the specified query in kadmin.local.

* realm.realm: The realm's name.

* realm.testdir: The realm's storage directory (absolute path).

* realm.portbase: The realm's first listener port.

* realm.user_princ: The principal name user@<realmname>.

* realm.admin_princ: The principal name user/admin@<realmname>.

* realm.host_princ: The name of the host principal for this machine,
  with realm.

* realm.nfs_princ: The name of the nfs principal for this machine,
  with realm.

* realm.krbtgt_princ: The name of the krbtgt principal for the realm.

* realm.keytab: A keytab file in realm.testdir.  Initially contains a
  host keytab unless disabled by the realm construction options.

* realm.ccache: A ccache file in realm.testdir.  Initially contains
  credentials for user unless disabled by the realm construction
  options.

* Attributes for the client, server, master, and slave environments.
  These environments are extensions of os.environ.
  - realm.env_client
  - realm.env_server
  - realm.env_master
  - realm.env_slave

When the test script is run, its behavior can be modified with
command-line flags.  These are documented in the --help output.

"""

import atexit
import optparse
import os
import shlex
import shutil
import signal
import socket
import string
import subprocess
import sys
import imp

# Used when most things go wrong (other than programming errors) so
# that the user sees an error message rather than a Python traceback,
# without help from the test script.  The on-exit handler will display
# additional explanatory text.
def fail(msg):
    """Print a message and exit with failure."""
    global _current_pass
    print "*** Failure:", msg
    if _current_pass:
        print "*** Failed in test pass:", _current_pass
    sys.exit(1)


def success(msg):
    global _success
    output('*** Success: %s\n' % msg)
    _success = True


def output(msg, force_verbose=False):
    """Output a message to testlog, and to stdout if running verbosely."""
    _outfile.write(msg)
    if verbose or force_verbose:
        sys.stdout.write(msg)


def password(name):
    """Choose a weakly random password from name, consistent across calls."""
    return name + str(os.getpid())


# Exit handler which ensures processes are cleaned up and, on failure,
# prints messages to help developers debug the problem.
def _onexit():
    global _daemons, _success, verbose
    global _debug, _stop_before, _stop_after, _shell_before, _shell_after
    if _daemons is None:
        # In Python 2.5, if we exit as a side-effect of importing
        # k5test, _onexit will execute in an empty global namespace.
        # This can happen if argument processing fails or the build
        # root isn't valid.  In this case we can safely assume that no
        # daemons have been launched and that we don't really need to
        # amend the error message.  The bug is fixed in Python 2.6.
        return
    if _debug or _stop_before or _stop_after or _shell_before or _shell_after:
        # Wait before killing daemons in case one is being debugged.
        sys.stdout.write('*** Press return to kill daemons and exit script: ')
        sys.stdin.readline()
    for proc in _daemons:
        os.kill(proc.pid, signal.SIGTERM)
    if not _success:
        print
        if not verbose:
            print 'See testlog for details, or re-run with -v flag.'
            print
        print 'Use --debug=NUM to run a command (other than a daemon) under a'
        print 'debugger.  Use --stop-after=NUM to stop after a daemon is'
        print 'started in order to attach to it with a debugger.  Use --help'
        print 'to see other options.'

# Find the parent of dir which is at the root of a build or source directory.
def _find_root(dir):
    while True:
        if os.path.exists(os.path.join(dir, 'lib', 'krb5', 'krb')):
            break
        parent = os.path.dirname(dir)
        if (parent == dir):
            return None
        dir = parent
    return dir


def _find_buildtop():
    root = _find_root(os.getcwd())
    if root is None:
        fail('Cannot find root of krb5 build directory.')
    if not os.path.exists(os.path.join(root, 'config.status')):
        # Looks like an unbuilt source directory.
        fail('This script must be run inside a krb5 build directory.')
    return root


def _find_srctop():
    scriptdir = os.path.abspath(os.path.dirname(sys.argv[0]))
    if not scriptdir:
        scriptdir = os.getcwd()
    root = _find_root(scriptdir)
    if root is None:
        fail('Cannot find root of krb5 source directory.')
    return os.path.abspath(root)


def _find_plugins():
    global buildtop
    fakeroot = os.path.join(buildtop, 'util', 'fakedest')
    if not os.path.exists(fakeroot):
        fail('You must run "make fake-install" in %s first.' % buildtop)
    for dir, subdirs, files in os.walk(fakeroot):
        if os.path.basename(dir) == 'plugins' and 'kdb' in subdirs:
            return dir
    fail('Cannot locate plugins; run "make fake-install" at %s.' % buildtop)

# Return the local hostname as it will be canonicalized by
# krb5_sname_to_principal.  We can't simply use socket.getfqdn()
# because it explicitly prefers results containing periods and
# krb5_sname_to_principal doesn't care.
def _get_hostname():
    hostname = socket.gethostname()
    try:
        ai = socket.getaddrinfo(hostname, None, 0, 0, 0,
                                socket.AI_CANONNAME | socket.AI_ADDRCONFIG)
    except socket.gaierror, (error, errstr):
        fail('Local hostname "%s" does not resolve: %s.' % (hostname, errstr))
    (family, socktype, proto, canonname, sockaddr) = ai[0]
    try:
        name = socket.getnameinfo(sockaddr, socket.NI_NAMEREQD)
    except socket.gaierror:
        return canonname.lower()
    return name[0].lower()

# Parse command line arguments, setting global option variables.  Also
# sets the global variable args to the positional arguments, which may
# be used by the test script.
def _parse_args():
    global args, verbose, testpass, _debug, _debugger_command
    global _stop_before, _stop_after, _shell_before, _shell_after
    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                      default=False, help='Display verbose output')
    parser.add_option('-p', '--pass', dest='testpass', metavar='PASS',
                      help='If a multi-pass test, run only PASS')
    parser.add_option('--debug', dest='debug', metavar='NUM',
                      help='Debug numbered command (or "all")')
    parser.add_option('--debugger', dest='debugger', metavar='COMMAND',
                      help='Debugger command (default is gdb --args)',
                      default='gdb --args')
    parser.add_option('--stop-before', dest='stopb', metavar='NUM',
                      help='Stop before numbered command (or "all")')
    parser.add_option('--stop-after', dest='stopa', metavar='NUM',
                      help='Stop after numbered command (or "all")')
    parser.add_option('--shell-before', dest='shellb', metavar='NUM',
                      help='Spawn shell before numbered command (or "all")')
    parser.add_option('--shell-after', dest='shella', metavar='NUM',
                      help='Spawn shell after numbered command (or "all")')
    (options, args) = parser.parse_args()
    verbose = options.verbose
    testpass = options.testpass
    _debug = _parse_cmdnum('--debug', options.debug)
    _debugger_command = shlex.split(options.debugger)
    _stop_before = _parse_cmdnum('--stop-before', options.stopb)
    _stop_after = _parse_cmdnum('--stop-after', options.stopa)
    _shell_before = _parse_cmdnum('--shell-before', options.shellb)
    _shell_after = _parse_cmdnum('--shell-after', options.shella)


# Translate a command number spec.  -1 means all, None means none.
def _parse_cmdnum(optname, str):
    if not str:
        return None
    if str == 'all':
        return -1
    try:
        return int(str)
    except ValueError:
        fail('%s value must be "all" or a number' % optname)


# Test if a command index matches a translated command number spec.
def _match_cmdnum(cmdnum, ind):
    if cmdnum is None:
        return False
    elif cmdnum == -1:
        return True
    else:
        return cmdnum == ind


# Return an environment suitable for running programs in the build
# tree.  It is safe to modify the result.
def _build_env():
    global buildtop, _runenv
    env = os.environ.copy()
    for (k, v) in _runenv.iteritems():
        if v.find('./') == 0:
            env[k] = os.path.join(buildtop, v)
        else:
            env[k] = v
    # Make sure we don't get confused by translated messages.
    env['LC_MESSAGES'] = 'C'
    return env


def _import_runenv():
    global buildtop
    runenv_py = os.path.join(buildtop, 'runenv.py')
    if not os.path.exists(runenv_py):
        fail('You must run "make fake-install" in %s first.' % buildtop)
    module = imp.load_source('runenv', runenv_py)
    return module.env


# Merge the nested dictionaries cfg1 and cfg2 into a new dictionary.
# cfg1 or cfg2 may be None, in which case the other is returned.  If
# cfg2 contains keys mapped to None, the corresponding keys will be
# mapped to None in the result.  The result may contain references to
# parts of cfg1 or cfg2, so is not safe to modify.
def _cfg_merge(cfg1, cfg2):
    if not cfg2:
        return cfg1
    if not cfg1:
        return cfg2
    result = cfg1.copy()
    for key, value2 in cfg2.items():
        if value2 is None or key not in result:
            result[key] = value2
        else:
            value1 = result[key]
            if isinstance(value1, dict):
                if not isinstance(value2, dict):
                    raise TypeError()
                result[key] = _cfg_merge(value1, value2)
            else:
                result[key] = value2
    return result


# Python gives us shlex.split() to turn a shell command into a list of
# arguments, but oddly enough, not the easier reverse operation.  For
# now, do a bad job of faking it.
def _shell_equiv(args):
    return " ".join(args)


# Add a valgrind prefix to the front of args if specified in the
# environment.  Under normal circumstances this just returns args.
def _valgrind(args):
    valgrind = os.getenv('VALGRIND')
    if valgrind:
        args = shlex.split(valgrind) + args
    return args


def _stop_or_shell(stop, shell, env, ind):
    if (_match_cmdnum(stop, ind)):
        sys.stdout.write('*** [%d] Waiting for return: ' % ind)
        sys.stdin.readline()
    if (_match_cmdnum(shell, ind)):
        output('*** [%d] Spawning shell\n' % ind, True)
        subprocess.call(os.getenv('SHELL'), env=env)


def _run_cmd(args, env, input=None, expected_code=0):
    global null_input, _cmd_index, _debug
    global _stop_before, _stop_after, _shell_before, _shell_after

    if (_match_cmdnum(_debug, _cmd_index)):
        return _debug_cmd(args, env, input)

    args = _valgrind(args)

    output('*** [%d] Executing: %s\n' % (_cmd_index, _shell_equiv(args)))
    _stop_or_shell(_stop_before, _shell_before, env, _cmd_index)

    if input:
        infile = subprocess.PIPE
    else:
        infile = null_input

    # Run the command and log the result, folding stderr into stdout.
    proc = subprocess.Popen(args, stdin=infile, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env=env)
    (outdata, dummy_errdata) = proc.communicate(input)
    code = proc.returncode
    output(outdata)
    output('*** [%d] Completed with return code %d\n' % (_cmd_index, code))
    _stop_or_shell(_stop_after, _shell_after, env, _cmd_index)
    _cmd_index += 1

    # Check the return code and return the output.
    if code != expected_code:
        fail('%s failed with code %d.' % (args[0], code))
    return outdata


def _debug_cmd(args, env, input):
    global _cmd_index, _debugger_command

    args = _debugger_command + list(args)
    output('*** [%d] Executing in debugger: %s\n' %
           (_cmd_index, _shell_equiv(args)), True)
    if input:
        print
        print '*** Enter the following input when appropriate:'
        print 
        print input
        print
    code = subprocess.call(args, env=env)
    output('*** [%d] Completed in debugger with return code %d\n' %
           (_cmd_index, code))
    _cmd_index += 1


# Start a daemon process with the specified args and env.  Wait until
# we see sentinel as a substring of a line on either stdout or stderr.
# Clean up the daemon process on exit.
def _start_daemon(args, env, sentinel):
    global null_input, _cmd_index, _debug
    global _stop_before, _stop_after, _shell_before, _shell_after

    # Make this non-fatal so that --debug=all works.
    if (_match_cmdnum(_debug, _cmd_index)):
        output('*** [%d] Cannot run daemon in debugger\n' % _cmd_index, True)

    args = _valgrind(args)
    output('*** [%d] Starting: %s\n' %
           (_cmd_index, _shell_equiv(args)))
    _stop_or_shell(_stop_before, _shell_before, env, _cmd_index)

    # Start the daemon and look for the sentinel in stdout or stderr.
    proc = subprocess.Popen(args, stdin=null_input, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env=env)
    while True:
        line = proc.stdout.readline()
        if line == "":
            code = proc.wait()
            fail('%s failed to start with code %d.' % (args[0], code))
        output(line)
        if sentinel in line:
            break
    output('*** [%d] Started with pid %d\n' % (_cmd_index, proc.pid))
    _stop_or_shell(_stop_after, _shell_after, env, _cmd_index)
    _cmd_index += 1

    # Save the daemon in a list for cleanup.  Note that we won't read
    # any more of the daemon's output after the sentinel, which will
    # cause the daemon to block if it generates enough.  For now we
    # assume all daemon processes are quiet enough to avoid this
    # problem.  If it causes an issue, some alternatives are:
    #   - Output to a file and poll the file for the sentinel
    #     (undesirable because it slows down the test suite by the
    #     polling interval times the number of daemons started)
    #   - Create an intermediate subprocess which discards output
    #     after the sentinel.
    _daemons.append(proc)

    # Return the process; the caller can stop it with stop_daemon.
    return proc


def stop_daemon(proc):
    output('*** Terminating process %d\n' % proc.pid)
    os.kill(proc.pid, signal.SIGTERM)
    proc.wait()
    _daemons.remove(proc)


class K5Realm(object):
    """An object representing a functional krb5 test realm."""

    def __init__(self, realm='KRBTEST.COM', portbase=61000, testdir='testdir',
                 krb5_conf=None, kdc_conf=None, create_kdb=True,
                 krbtgt_keysalt=None, create_user=True, get_creds=True,
                 create_host=True, start_kdc=True, start_kadmind=True):
        global hostname, _default_krb5_conf, _default_kdc_conf

        self.realm = realm
        self.testdir = os.path.join(os.getcwd(), testdir)
        self.portbase = portbase
        self.user_princ = 'user@' + self.realm
        self.admin_princ = 'user/admin@' + self.realm
        self.host_princ = 'host/%s@%s' % (hostname, self.realm)
        self.nfs_princ = 'nfs/%s@%s' % (hostname, self.realm)
        self.krbtgt_princ = 'krbtgt/%s@%s' % (self.realm, self.realm)
        self.keytab = os.path.join(self.testdir, 'keytab')
        self.ccache = os.path.join(self.testdir, 'ccache')
        self._krb5_conf = _cfg_merge(_default_krb5_conf, krb5_conf)
        self._kdc_conf = _cfg_merge(_default_kdc_conf, kdc_conf)
        self._kdc_proc = None
        self._kadmind_proc = None

        self._create_empty_dir()
        self._create_krb5_conf('client')
        self._create_krb5_conf('server')
        self._create_krb5_conf('master')
        self._create_krb5_conf('slave')
        self._create_kdc_conf('master')
        self._create_kdc_conf('slave')
        self._create_acl()
        self._create_dictfile()

        self.env_client = self._make_env('client', False)
        self.env_server = self._make_env('server', False)
        self.env_master = self._make_env('master', True)
        self.env_slave = self._make_env('slave', True)

        if create_kdb:
            self.create_kdb()
        if krbtgt_keysalt and create_kdb:
            self.run_kadminl('cpw -randkey -e %s %s' %
                             (krbtgt_keysalt, self.krbtgt_princ))
        if create_user and create_kdb:
            self.addprinc(self.user_princ, password('user'))
            self.addprinc(self.admin_princ, password('admin'))
        if create_host and create_kdb:
            self.addprinc(self.host_princ)
            self.extract_keytab(self.host_princ, self.keytab)
        if start_kdc and create_kdb:
            self.start_kdc()
        if start_kadmind and create_kdb:
            self.start_kadmind()
        if get_creds and create_kdb and create_user and start_kdc:
            self.kinit(self.user_princ, password('user'))
            self.klist(self.user_princ)

    def _create_empty_dir(self):
        dir = self.testdir
        shutil.rmtree(dir, True)
        if (os.path.exists(dir)):
            fail('Cannot remove %s to create test realm.' % dir)
        os.mkdir(dir)

    def _create_krb5_conf(self, type):
        filename = os.path.join(self.testdir, 'krb5.%s.conf' % type)
        file = open(filename, 'w')
        profile = _cfg_merge(self._krb5_conf['all'], self._krb5_conf.get(type))
        for section, contents in profile.items():
            file.write('[%s]\n' % section)
            self._write_cfg_section(file, type, contents, 1)
        file.close()

    def _create_kdc_conf(self, type):
        filename = os.path.join(self.testdir, 'kdc.%s.conf' % type)
        file = open(filename, 'w')
        profile = _cfg_merge(self._kdc_conf['all'], self._kdc_conf.get(type))
        for section, contents in profile.items():
            file.write('[%s]\n' % section)
            self._write_cfg_section(file, type, contents, 1)
        file.close()

    def _write_cfg_section(self, file, type, contents, indent_level):
        indent = '\t' * indent_level
        for name, value in contents.items():
            name = self._subst_cfg_value(name, type)
            if isinstance(value, dict):
                # A dictionary value yields a list subsection.
                file.write('%s%s = {\n' % (indent, name))
                self._write_cfg_section(file, type, value, indent_level + 1)
                file.write('%s}\n' % indent)
            elif isinstance(value, list):
                # A list value yields multiple values for the same name.
                for item in value:
                    item = self._subst_cfg_value(item, type)
                    file.write('%s%s = %s\n' % (indent, name, item))
            elif isinstance(value, str):
                # A string value yields a straightforward variable setting.
                value = self._subst_cfg_value(value, type)
                file.write('%s%s = %s\n' % (indent, name, value))
            elif value is not None:
                raise TypeError()

    def _subst_cfg_value(self, value, type):
        global buildtop, srctop, hostname
        template = string.Template(value)
        return template.substitute(type=type,
                                   realm=self.realm,
                                   testdir=self.testdir,
                                   buildtop=buildtop,
                                   srctop=srctop,
                                   plugins=plugins,
                                   hostname=hostname,
                                   port0=self.portbase,
                                   port1=self.portbase + 1,
                                   port2=self.portbase + 2,
                                   port3=self.portbase + 3,
                                   port4=self.portbase + 4,
                                   port5=self.portbase + 5,
                                   port6=self.portbase + 6,
                                   port7=self.portbase + 7,
                                   port8=self.portbase + 8,
                                   port9=self.portbase + 9)

    def _create_acl(self):
        global hostname
        filename = os.path.join(self.testdir, 'acl')
        file = open(filename, 'w')
        file.write('%s *\n' % self.admin_princ)
        file.write('kiprop/%s@%s p\n' % (hostname, self.realm))
        file.close()

    def _create_dictfile(self):
        filename = os.path.join(self.testdir, 'dictfile')
        file = open(filename, 'w')
        file.write('weak_password\n')
        file.close()

    def _make_env(self, type, has_kdc_conf):
        env = _build_env()
        env['KRB5_CONFIG'] = os.path.join(self.testdir, 'krb5.%s.conf' % type)
        if has_kdc_conf:
            filename = os.path.join(self.testdir, 'kdc.%s.conf' % type)
            env['KRB5_KDC_PROFILE'] = filename
        env['KRB5CCNAME'] = self.ccache
        env['KRB5_KTNAME'] = self.keytab
        env['KRB5RCACHEDIR'] = self.testdir
        return env

    def run_as_client(self, args, **keywords):
        return _run_cmd(args, self.env_client, **keywords)

    def run_as_server(self, args, **keywords):
        return _run_cmd(args, self.env_server, **keywords)

    def run_as_master(self, args, **keywords):
        return _run_cmd(args, self.env_master, **keywords)

    def run_as_slave(self, args, **keywords):
        return _run_cmd(args, self.env_slave, **keywords)

    def server_port(self):
        return self.portbase + 3

    def start_server(self, args, sentinel):
        return _start_daemon(args, self.env_server, sentinel)

    def start_in_inetd(self, args, port=None):
        if not port:
            port = self.server_port()
        inetd_args = [t_inetd, str(port)] + args
        return _start_daemon(inetd_args, self.env_server, 'Ready!')

    def create_kdb(self):
        global kdb5_util
        self.run_as_master([kdb5_util, 'create', '-W', '-s', '-P', 'master'])

    def start_kdc(self, args=[]):
        global krb5kdc
        assert(self._kdc_proc is None)
        self._kdc_proc = _start_daemon([krb5kdc, '-n'] + args, self.env_master,
                                        'starting...')

    def stop_kdc(self):
        assert(self._kdc_proc is not None)
        stop_daemon(self._kdc_proc)
        self._kdc_proc = None

    def start_kadmind(self):
        global krb5kdc
        assert(self._kadmind_proc is None)
        self._kadmind_proc = _start_daemon([kadmind, '-nofork', '-W'],
                                            self.env_master, 'starting...')

    def stop_kadmind(self):
        assert(self._kadmind_proc is not None)
        stop_daemon(self._kadmind_proc)
        self._kadmind_proc = None

    def stop(self):
        if self._kdc_proc:
            self.stop_kdc()
        if self._kadmind_proc:
            self.stop_kadmind()

    def addprinc(self, princname, password=None):
        if password:
            self.run_kadminl('addprinc -pw %s %s' % (password, princname))
        else:
            self.run_kadminl('addprinc -randkey %s' % princname)

    def extract_keytab(self, princname, keytab):
        self.run_kadminl('ktadd -k %s -norandkey %s' % (keytab, princname))

    def kinit(self, princname, password=None, flags=[], **keywords):
        if password:
            input = password + "\n"
        else:
            input = None
        self.run_as_client([kinit] + flags + [princname], input=input,
                           **keywords)

    def klist(self, client_princ, service_princ=None, ccache=None, **keywords):
        if service_princ is None:
            service_princ = self.krbtgt_princ
        if ccache is None:
            ccache = self.ccache
        output = self.run_as_client([klist, ccache], **keywords)
        if (('Ticket cache: FILE:%s\n' % ccache) not in output or
            ('Default principal: %s\n' % client_princ) not in output or
            service_princ not in output):
            fail('Unexpected klist output.')

    def klist_keytab(self, princ, keytab=None, **keywords):
        if keytab is None:
            keytab = self.keytab
        output = self.run_as_client([klist, '-k', keytab], **keywords)
        if (('Keytab name: FILE:%s\n' % keytab) not in output or
            'KVNO Principal\n----' not in output or
            princ not in output):
            fail('Unexpected klist output.')

    def run_kadminl(self, query):
        global kadmin_local
        return self.run_as_master([kadmin_local, '-q', query])


def multipass_realms(**keywords):
    global _current_pass, _passes, testpass
    caller_krb5_conf = keywords.get('krb5_conf')
    caller_kdc_conf = keywords.get('kdc_conf')
    for p in _passes:
        (name, krbtgt_keysalt, krb5_conf, kdc_conf) = p
        if testpass and name != testpass:
            continue
        output('*** Beginning pass %s\n' % name)
        keywords['krb5_conf'] = _cfg_merge(krb5_conf, caller_krb5_conf)
        keywords['kdc_conf'] = _cfg_merge(kdc_conf, caller_kdc_conf)
        keywords['krbtgt_keysalt'] = krbtgt_keysalt
        _current_pass = name
        realm = K5Realm(**keywords)
        yield realm
        realm.stop()
        _current_pass = None


_default_krb5_conf = {
    'all' : {
        'libdefaults' : {
            'default_realm' : '$realm',
            'dns_lookup_kdc' : 'false',
            'plugin_base_dir' : '$plugins'
        },
        'realms' : {
            '$realm' : {
                'kdc' : '$hostname:$port0',
                'admin_server' : '$hostname:$port1',
                'kpasswd_server' : '$hostname:$port2'
            }
        }
    }
}


_default_kdc_conf = {
    'all' : {
        'realms' : {
            '$realm' : {
                'database_module' : 'foo_db2'
            }
        },
        'dbmodules' : {
            'db_module_dir' : '$plugins/kdb',
            'foo_db2' : {
                'db_library' : 'db2',
                'database_name' : '$testdir/$type-db'
            }
        },
        'logging' : {
            'admin_server' : 'FILE:$testdir/kadmind5.log',
            'kdc' : 'FILE:$testdir/kdc.log',
            'default' : 'FILE:$testdir/others.log'
        }
    },
    'master' : {
        'realms' : {
            '$realm' : {
                'key_stash_file' : '$testdir/stash',
                'acl_file' : '$testdir/acl',
                'dictfile' : '$testdir/dictfile',
                'kadmind_port' : '$port1',
                'kpasswd_port' : '$port2',
                'kdc_ports' : '$port0',
                'kdc_tcp_ports' : '$port0'
            }
        }
    },
    'slave' : {
        'realms' : {
            '$realm' : {
                'key_stash_file' : '$testdir/slave-stash',
            }
        }
    }
}


# A pass is a tuple of: name, krbtgt_keysalt, krb5_conf, kdc_conf.
_passes = [
    # No special settings; exercises AES256.
    ('default', None, None, None),

    # Exercise a DES enctype and the v4 salt type.
    ('desv4', None,
     {'all' : {'libdefaults' : {
                    'default_tgs_enctypes' : 'des-cbc-crc',
                    'default_tkt_enctypes' : 'des-cbc-crc',
                    'permitted_enctypes' : 'des-cbc-crc',
                    'allow_weak_crypto' : 'true'}}},
     {'master' : {'realms' : {'$realm' : {
                        'supported_enctypes' : 'des-cbc-crc:v4',
                        'master_key_type' : 'des-cbc-crc'}}}}),

    # Exercise the DES3 enctype.
    ('des3', None,
     {'all' : {'libdefaults' : {
                    'default_tgs_enctypes' : 'des3',
                    'default_tkt_enctypes' : 'des3',
                    'permitted_enctypes' : 'des3'}}},
     {'master' : {'realms' : {'$realm' : {
                        'supported_enctypes' : 'des3-cbc-sha1:normal',
                        'master_key_type' : 'des3-cbc-sha1'}}}}),

    # Exercise the arcfour enctype.
    ('arcfour', None,
     {'all' : {'libdefaults' : {
                    'default_tgs_enctypes' : 'rc4',
                    'default_tkt_enctypes' : 'rc4',
                    'permitted_enctypes' : 'rc4'}}},
     {'master' : {'realms' : {'$realm' : {
                        'supported_enctypes' : 'arcfour-hmac:normal',
                        'master_key_type' : 'arcfour-hmac'}}}}),

    # Exercise the AES128 enctype.
    ('aes128', None,
      {'all' : {'libdefaults' : {
                    'default_tgs_enctypes' : 'aes128-cts',
                    'default_tkt_enctypes' : 'aes128-cts',
                    'permitted_enctypes' : 'aes128-cts'}}},
      {'master' : {'realms' : {'$realm' : {
                        'supported_enctypes' : 'aes128-cts:normal',
                        'master_key_type' : 'aes128-cts'}}}}),

    # Exercise the camellia256-cts enctype.
# Enable when Camellia support becomes unconditional.
#    ('camellia256', None,
#      {'all' : {'libdefaults' : {
#                    'default_tgs_enctypes' : 'camellia256-cts',
#                    'default_tkt_enctypes' : 'camellia256-cts',
#                    'permitted_enctypes' : 'camellia256-cts'}}},
#      {'master' : {'realms' : {'$realm' : {
#                        'supported_enctypes' : 'camellia256-cts:normal',
#                        'master_key_type' : 'camellia256-cts'}}}}),

    # Test a setup with modern principal keys but an old TGT key.
    ('aes256.destgt', 'des-cbc-crc:normal',
     {'all' : {'libdefaults' : {'allow_weak_crypto' : 'true'}}},
     None)
]

_success = False
_current_pass = None
_daemons = []
_parse_args()
atexit.register(_onexit)
_outfile = open('testlog', 'w')
_cmd_index = 1
buildtop = _find_buildtop()
srctop = _find_srctop()
plugins = _find_plugins()
_runenv = _import_runenv()
hostname = _get_hostname()
null_input = open(os.devnull, 'r')

krb5kdc = os.path.join(buildtop, 'kdc', 'krb5kdc')
kadmind = os.path.join(buildtop, 'kadmin', 'server', 'kadmind')
kadmin = os.path.join(buildtop, 'kadmin', 'cli', 'kadmin')
kadmin_local = os.path.join(buildtop, 'kadmin', 'cli', 'kadmin.local')
kdb5_util = os.path.join(buildtop, 'kadmin', 'dbutil', 'kdb5_util')
ktutil = os.path.join(buildtop, 'kadmin', 'ktutil', 'ktutil')
kinit = os.path.join(buildtop, 'clients', 'kinit', 'kinit')
klist = os.path.join(buildtop, 'clients', 'klist', 'klist')
kswitch = os.path.join(buildtop, 'clients', 'kswitch', 'kswitch')
kvno = os.path.join(buildtop, 'clients', 'kvno', 'kvno')
kdestroy = os.path.join(buildtop, 'clients', 'kdestroy', 'kdestroy')
kpasswd = os.path.join(buildtop, 'clients', 'kpasswd', 'kpasswd')
t_inetd = os.path.join(buildtop, 'tests', 'dejagnu', 't_inetd')
kproplog = os.path.join(buildtop, 'slave', 'kproplog')
kpropd = os.path.join(buildtop, 'slave', 'kpropd')
kprop = os.path.join(buildtop, 'slave', 'kprop')

# Currently there are no helpers for doing cross-realm testing, but
# the necessary flexibility is present in K5Realm to create them.  A
# cross-realm test setup would need to:
#
# * Select distinct realm names, port bases, and directories for each
#   realm.
# 
# * Create a krb5_conf fragment with a comprehensive [realms] section
#   so that each realm knows how to reach the others, since there
#   won't be DNS SRV records.  The fragment should probably None out
#   'realms' -> '$realm' to avoid a duplicate section for the home
#   realm.  capaths configuration may also be desired for some test
#   cases.
#
# * Create cross-TGS principals for some or all of the pairs of
#   realms.

.TH KDB5_LDAP_UTIL 8
.SH NAME
kdb5_ldap_util \- Kerberos Configuration Utility
.SH SYNOPSIS
.B kdb5_ldap_util
[\fB\-D\fP\ \fIuser_dn\fP [\fB\-w\fP\ \fIpasswd\fP]]
[\fB\-H\fP\ \fIldapuri\fP]
.I command
.I [command_options]
.SH DESCRIPTION
.B kdb5_ldap_util
allows an administrator to manage realms, Kerberos services and ticket policies.
.SH COMMAND-LINE OPTIONS
.TP
\fB\-D\fP\ \fIuser_dn\fP
Specifies the Distinguished name (DN) of the user who has sufficient rights to 
perform the operation on the LDAP server.
.TP
\fB\-w\fP\ \fIpasswd\fP
Specifies the password of 
.IR user_dn .
This option is not recommended.
.TP
\fB\-H\fP\ \fIldapuri\fP
Specifies the URI of the LDAP server.
.SH COMMANDS
.TP
\fBcreate\fP [\fB\-subtrees\fP\ \fIsubtree_dn_list\fP] [\fB\-sscope\fP\ \fIsearch_scope\fP] [\fB\-containerref\fP\ \fIcontainer_reference_dn\fP] [\fB\-k\fP\ \fImkeytype\fP] [\fB\-kv\fP\ \fImkeyVNO\fP] [\fB\-m\fP|\fB\-P\fP\ \fIpassword\fP|\fB\-sf\fP\ \fIstashfilename\fP] [\fB\-s\fP] [\fB\-r\fP\ \fIrealm\fP] [\fB\-kdcdn\fP\ \fIkdc_service_list\fP] [\fB\-admindn\fP\ \fIadmin_service_list\fP] [\fB\-maxtktlife\fP\ \fImax_ticket_life\fP] [\fB\-maxrenewlife\fP\ \fImax_renewable_ticket_life\fP] [\fIticket_flags\fP]
Creates realm in directory. Options:
.RS
.TP
\fB\-subtrees\fP\ \fIsubtree_dn_list\fP
Specifies the list of subtrees containing the principals of a realm. The list contains the DNs of the subtree
objects separated by colon(:).
.TP
\fB\-sscope\fP\ \fIsearch_scope\fP
Specifies the scope for searching the principals under the 
.IR subtree .
The possible values are 1 or one (one level), 2 or sub (subtrees).
.TP
\fB\-containerref\fP\ \fIcontainer_reference_dn\fP 
Specifies the DN of the container object in which the principals of a realm will be created.
If the container reference is not configured for a realm, the principals will be created in the realm container. 
.TP
\fB\-k\fP\ \fImkeytype\fP
Specifies the key type of the master key in the database; the default is
that given in
.IR kdc.conf .
.TP
\fB\-kv\fP\ \fImkeyVNO\fP
Specifies the version number of the master key in the database; the default is
1. Note that 0 is not allowed.
.TP
\fB\-m\fP
Specifies that the master database password should be read from the TTY
rather than fetched from a file on the disk.
.TP
\fB\-P\fP\ \fIpassword\fP
Specifies the master database password. This option is not recommended.
.TP
\fB\-sf\fP\ \fIstashfilename\fP
Specifies the stash file of the master database password.
.TP
\fB\-s\fP
Specifies that the stash file is to be created.
.TP
\fB\-maxtktlife\fP\ \fImax_ticket_life\fP
Specifies maximum ticket life for principals in this realm.
.TP
\fB\-maxrenewlife\fP\ \fImax_renewable_ticket_life\fP
Specifies maximum renewable life of tickets for principals in this realm.
.TP
\fIticket_flags\fP
Specifies the ticket flags. If this option is not specified, by default, none of the flags are
set. This means all the ticket options will be allowed and no restriction will be set.

The various flags are:
.TP
{\fB\-\fP|\fB+\fP}\fBallow_postdated\fP
.B \-allow_postdated
prohibits principals from obtaining postdated tickets.  (Sets the
.SM KRB5_KDB_DISALLOW_POSTDATED
flag.)
.B +allow_postdated
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_forwardable\fP
.B \-allow_forwardable
prohibits principals from obtaining forwardable tickets.  (Sets the
.SM KRB5_KDB_DISALLOW_FORWARDABLE
flag.)
.B +allow_forwardable
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_renewable\fP
.B \-allow_renewable
prohibits principals from obtaining renewable tickets. (Sets the
.SM KRB5_KDB_DISALLOW_RENEWABLE
flag.)
.B +allow_renewable
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_proxiable\fP
.B \-allow_proxiable
prohibits principals from obtaining proxiable tickets.  (Sets the
.SM KRB5_KDB_DISALLOW_PROXIABLE
flag.)
.B +allow_proxiable
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_dup_skey\fP
.B \-allow_dup_skey
Disables user-to-user authentication for principals by prohibiting
principals from obtaining a session key for another user. (Sets the
.SM KRB5_KDB_DISALLOW_DUP_SKEY
flag.)
.B +allow_dup_skey
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBrequires_preauth\fP
.B +requires_preauth
requires principals to preauthenticate before being allowed to
kinit.  (Sets the
.SM KRB5_KDB_REQUIRES_PRE_AUTH
flag.)
.B \-requires_preauth
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBrequires_hwauth\fP
.B +requires_hwauth
requires principals to preauthenticate using a hardware device
before being allowed to kinit.  (Sets the
.SM KRB5_KDB_REQUIRES_HW_AUTH
flag.)
.B \-requires_hwauth
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_svr\fP
.B \-allow_svr
prohibits the issuance of service tickets for principals.  (Sets the
.SM KRB5_KDB_DISALLOW_SVR
flag.)
.B +allow_svr
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_tgs_req\fP
.B \-allow_tgs_req
specifies that a Ticket-Granting Service (TGS) request for a service
ticket for principals is not permitted.  This option is useless for
most things.
.B +allow_tgs_req
clears this flag.  The default is
.BR +allow_tgs_req .
In effect,
.B \-allow_tgs_req
sets the
.SM KRB5_KDB_DISALLOW_TGT_BASED
flag on principals in the database.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_tix\fP
.B \-allow_tix
forbids the issuance of any tickets for principals.
.B +allow_tix
clears this flag.  The default is
.BR +allow_tix .
In effect,
.B \-allow_tix
sets the
.SM KRB5_KDB_DISALLOW_ALL_TIX
flag on principals in the database.
.TP
{\fB\-\fP|\fB+\fP}\fBneedchange\fP
.B +needchange
sets a flag in attributes field to force a password change;
.B \-needchange
clears it. The default is
.BR \-needchange .
In effect,
.B +needchange
sets the
.SM KRB5_KDB_REQUIRES_PWCHANGE
flag on principals in the database.
.TP
{\fB\-\fP|\fB+\fP}\fBpassword_changing_service\fP
.B +password_changing_service
sets a flag in the attributes field marking principal as a password change
service principal (useless for most things).
.B \-password_changing_service
clears the flag. This flag intentionally has a long name. The default
is
.BR \-password_changing_service .
In effect,
.B +password_changing_service
sets the
.SM KRB5_KDB_PWCHANGE_SERVICE
flag on principals in the database.
.TP
\fB\-r\fP\ \fIrealm\fP
Specifies the Kerberos realm of the database; by default the realm
returned by
.IR krb5_default_local_realm (3)
is used.
.TP
.B Command Options Specific to eDirectory 
.TP
\fB\-kdcdn\fP\ \fIkdc_service_list\fP
Specifies the list of KDC service objects serving the realm. The list contains the DNs of the KDC
service objects separated by colon(:).
.TP
\fB\-admindn\fP\ \fIadmin_service_list\fP
Specifies the list of Administration service objects serving the realm. The list contains the DNs
of the Administration service objects separated by colon(:).
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu
create \-subtrees o=org \-sscope SUB
\-r ATHENA.MIT.EDU\fP
.nf
Password for "cn=admin,o=org":
Initializing database for realm 'ATHENA.MIT.EDU'
You will be prompted for the database Master Password.
It is important that you NOT FORGET this password.
Enter KDC database master key:
Re-enter KDC database master key to verify:
.fi
.RE

.TP
\fBmodify\fP [\fB\-subtrees\fP\ \fIsubtree_dn_list\fP] [\fB\-sscope\fP\ \fIsearch_scope\fP] [\fB\-containerref\fP\ \fIcontainer_reference_dn\fP] [\fB\-r\fP\ \fIrealm\fP] [\fB\-kdcdn\fP\ \fIkdc_service_list\fP | [\fB\-clearkdcdn\fP\ \fIkdc_service_list\fP] [\fB\-addkdcdn\fP\ \fIkdc_service_list\fP]] [\fB\-admindn\fP\ \fIadmin_service_list\fP | [\fB\-clearadmindn\fP\ \fIadmin_service_list\fP] [\fB\-addadmindn\fP\ \fIadmin_service_list\fP]] [\fB\-maxtktlife\fP\ \fImax_ticket_life\fP] [\fB\-maxrenewlife\fP\ \fImax_renewable_ticket_life\fP] [\fIticket_flags\fP]

Modifies the attributes of a realm. Options:
.RS
.TP
\fB\-subtrees\fP\ \fIsubtree_dn_list\fP
Specifies the list of subtrees containing the principals of a realm.
The list contains the DNs of the subtree objects separated by 
colon(:). This list replaces the existing list.
.TP
\fB\-sscope\fP\ \fIsearch_scope\fP
Specifies the scope for searching the principals under the 
.IR subtrees .
The possible values are 1 or one (one level), 2 or sub (subtrees).
.TP
\fB\-containerref\fP\ \fIcontainer_reference_dn\fP 
Specifies the DN of the container object in which the principals of a realm 
will be created. 
.TP
\fB\-maxtktlife\fP\ \fImax_ticket_life\fP
Specifies maximum ticket life for principals in this realm.
.TP
\fB\-maxrenewlife\fP\ \fImax_renewable_ticket_life\fP
Specifies maximum renewable life of tickets for principals in this realm.
.TP
\fIticket_flags\fP
Specifies the ticket flags. If this option is not specified, by default, 
none of the flags are set. This means all the ticket options will be allowed 
and no restriction will be set.

The various flags are:
.TP
{\fB\-\fP|\fB+\fP}\fBallow_postdated\fP
.B \-allow_postdated
prohibits principals from obtaining postdated tickets.  (Sets the
.SM KRB5_KDB_DISALLOW_POSTDATED
flag.)
.B +allow_postdated
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_forwardable\fP
.B \-allow_forwardable
prohibits principals from obtaining forwardable tickets.  (Sets the
.SM KRB5_KDB_DISALLOW_FORWARDABLE
flag.)
.B +allow_forwardable
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_renewable\fP
.B \-allow_renewable
prohibits principals from obtaining renewable tickets. (Sets the
.SM KRB5_KDB_DISALLOW_RENEWABLE
flag.)
.B +allow_renewable
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_proxiable\fP
.B \-allow_proxiable
prohibits principals from obtaining proxiable tickets.  (Sets the
.SM KRB5_KDB_DISALLOW_PROXIABLE
flag.)
.B +allow_proxiable
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_dup_skey\fP
.B \-allow_dup_skey
Disables user-to-user authentication for principals by prohibiting
principals from obtaining a session key for another user. (Sets the
.SM KRB5_KDB_DISALLOW_DUP_SKEY
flag.)
.B +allow_dup_skey
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBrequires_preauth\fP
.B +requires_preauth
requires principals to preauthenticate before being allowed to
kinit.  (Sets the
.SM KRB5_KDB_REQUIRES_PRE_AUTH
flag.)
.B \-requires_preauth
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBrequires_hwauth\fP
.B +requires_hwauth
requires principals to preauthenticate using a hardware device
before being allowed to kinit.  (Sets the
.SM KRB5_KDB_REQUIRES_HW_AUTH
flag.)
.B \-requires_hwauth
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_svr\fP
.B \-allow_svr
prohibits the issuance of service tickets for principals.  (Sets the
.SM KRB5_KDB_DISALLOW_SVR
flag.)
.B +allow_svr
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_tgs_req\fP
.B \-allow_tgs_req
specifies that a Ticket-Granting Service (TGS) request for a service
ticket for principals is not permitted.  This option is useless for
most things.
.B +allow_tgs_req
clears this flag.  The default is
.BR +allow_tgs_req .
In effect,
.B \-allow_tgs_req
sets the
.SM KRB5_KDB_DISALLOW_TGT_BASED
flag on principals in the database.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_tix\fP
.B \-allow_tix
forbids the issuance of any tickets for principals.
.B +allow_tix
clears this flag.  The default is
.BR +allow_tix .
In effect,
.B \-allow_tix
sets the
.SM KRB5_KDB_DISALLOW_ALL_TIX
flag on principals in the database.
.TP
{\fB\-\fP|\fB+\fP}\fBneedchange\fP
.B +needchange
sets a flag in attributes field to force a password change;
.B \-needchange
clears it. The default is
.BR \-needchange .
In effect,
.B +needchange
sets the
.SM KRB5_KDB_REQUIRES_PWCHANGE
flag on principals in the database.
.TP
{\fB\-\fP|\fB+\fP}\fBpassword_changing_service\fP
.B +password_changing_service
sets a flag in the attributes field marking principal as a password change
service principal (useless for most things).
.B \-password_changing_service
clears the flag. This flag intentionally has a long name. The default
is
.BR \-password_changing_service .
In effect,
.B +password_changing_service
sets the
.SM KRB5_KDB_PWCHANGE_SERVICE
flag on principals in the database.
.TP
\fB\-r\fP\ \fIrealm\fP
Specifies the Kerberos realm of the database; by default the realm
returned by
.IR krb5_default_local_realm (3)
is used.
.TP
.B Command Options Specific to eDirectory
.TP
\fB\-kdcdn\fP\ \fIkdc_service_list\fP
Specifies the list of KDC service objects serving the realm. The list contains the DNs of the KDC
service objects separated by a colon (:). This list replaces the existing list.
.TP
\fB\-clearkdcdn\fP\ \fIkdc_service_list\fP
Specifies the list of KDC service objects that need to be removed from the existing list. The list contains
the DNs of the KDC service objects separated by a colon (:).
.TP
\fB\-addkdcdn\fP\ \fIkdc_service_list\fP
Specifies the list of KDC service objects that need to be added to the existing list. The list contains the
DNs of the KDC service objects separated by a colon (:).
.TP
\fB\-admindn\fP\ \fIadmin_service_list\fP
Specifies the list of Administration service objects serving the realm. The list contains the DNs
of the Administration service objects separated by a colon (:). This list replaces the existing list.
.TP
\fB\-clearadmindn\fP\ \fIadmin_service_list\fP
Specifies the list of Administration service objects that need to be removed from the existing list. The list
contains the DNs of the Administration service objects separated by a colon (:).
.TP
\fB\-addadmindn\fP\ \fIadmin_service_list\fP
Specifies the list of Administration service objects that need to be added to the existing list. The list
contains the DNs of the Administration service objects separated by a colon (:).
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu modify 
+requires_preauth \-r ATHENA.MIT.EDU \fP
.nf
Password for "cn=admin,o=org":
.fi
.RE
.TP
\fBview\fP [\fB\-r\fP\ \fIrealm\fP]
Displays the attributes of a realm.  Options:
.RS
.TP
\fB\-r\fP\ \fIrealm\fP
Specifies the Kerberos realm of the database; by default the realm returned by
.IR krb5_default_local_realm (3)
is used.
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu view 
\-r ATHENA.MIT.EDU\fP
.nf
Password for "cn=admin,o=org":
               Realm Name: ATHENA.MIT.EDU
                  Subtree: ou=users,o=org
                  Subtree: ou=servers,o=org
              SearchScope: ONE
      Maximum ticket life: 0 days 01:00:00
   Maximum renewable life: 0 days 10:00:00
             Ticket flags: DISALLOW_FORWARDABLE REQUIRES_PWCHANGE
.fi
.RE
.TP
\fBdestroy\fP [\fB-f\fP] [\fB\-r\fP\ \fIrealm\fP]
Destroys an existing realm. Options:
.RS
.TP
\fB\-f\fP
If specified, will not prompt the user for confirmation.  
.TP
\fB\-r\fP\ \fIrealm\fP
Specifies the Kerberos realm of the database; by default the realm returned by
.IR krb5_default_local_realm (3)
is used.
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu destroy 
\-r ATHENA.MIT.EDU\fP
.nf
Password for "cn=admin,o=org":
Deleting KDC database of 'ATHENA.MIT.EDU', are you sure?
(type 'yes' to confirm)? yes
OK, deleting database of 'ATHENA.MIT.EDU'...
.fi
.RE
.TP
\fBlist\fP

Lists the name of realms.
.RS
.nf
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu list\fP
Password for "cn=admin,o=org":
ATHENA.MIT.EDU
OPENLDAP.MIT.EDU
MEDIA-LAB.MIT.EDU
.fi
.RE
.TP
\fBstashsrvpw\fP [\fB\-f\fP\ \fIfilename\fP] \fIservicedn\fP
Allows an administrator to store the password for service object in a file so that KDC and Administration
server can use it to authenticate to the LDAP server. Options:
.RS
.TP
\fB\-f\fP\ \fIfilename\fP
Specifies the complete path of the service password file. By default, /usr/local/var/service_passwd is used.
.TP
\fIservicedn\fP
Specifies Distinguished name (DN) of the service object whose password is to be stored in file.
.TP
EXAMPLE:
\fBkdb5_ldap_util stashsrvpw \-f /home/andrew/conf_keyfile cn=service-kdc,o=org\fP
.nf
Password for "cn=service-kdc,o=org":
Re-enter password for "cn=service-kdc,o=org":
.fi
.RE
.TP
\fBcreate_policy\fP [\fB\-r\fP\ \fIrealm\fP] [\fB\-maxtktlife\fP\ \fImax_ticket_life\fP] [\fB\-maxrenewlife\fP\ \fImax_renewable_ticket_life\fP] [\fIticket_flags\fP] \fIpolicy_name\fP
Creates a ticket policy in directory. Options:
.RS
.TP
\fB\-r\fP\ \fIrealm\fP
Specifies the Kerberos realm of the database; by default the realm
returned by
.IR krb5_default_local_realm (3)
is used.
.TP
\fB\-maxtktlife\fP\ \fImax_ticket_life\fP
Specifies maximum ticket life for principals.
.TP
\fB\-maxrenewlife\fP\ \fImax_renewable_ticket_life\fP
Specifies maximum renewable life of tickets for principals.
.TP
\fIticket_flags\fP
Specifies the ticket flags. If this option is not specified, by default, none of the flags are
set. This means all the ticket options will be allowed and no restriction will be set.

The various flags are:
.TP
{\fB\-\fP|\fB+\fP}\fBallow_postdated\fP
.B \-allow_postdated
prohibits principals from obtaining postdated tickets.  (Sets the
.SM KRB5_KDB_DISALLOW_POSTDATED
flag.)
.B +allow_postdated
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_forwardable\fP
.B \-allow_forwardable
prohibits principals from obtaining forwardable tickets.  (Sets the
.SM KRB5_KDB_DISALLOW_FORWARDABLE
flag.)
.B +allow_forwardable
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_renewable\fP
.B \-allow_renewable
prohibits principals from obtaining renewable tickets. (Sets the
.SM KRB5_KDB_DISALLOW_RENEWABLE
flag.)
.B +allow_renewable
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_proxiable\fP
.B \-allow_proxiable
prohibits principals from obtaining proxiable tickets.  (Sets the
.SM KRB5_KDB_DISALLOW_PROXIABLE
flag.)
.B +allow_proxiable
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_dup_skey\fP
.B \-allow_dup_skey
Disables user-to-user authentication for principals by prohibiting
principals from obtaining a session key for another user. (Sets the
.SM KRB5_KDB_DISALLOW_DUP_SKEY
flag.)
.B +allow_dup_skey
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBrequires_preauth\fP
.B +requires_preauth
requires principals to preauthenticate before being allowed to
kinit.  (Sets the
.SM KRB5_KDB_REQUIRES_PRE_AUTH
flag.)
.B \-requires_preauth
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBrequires_hwauth\fP
.B +requires_hwauth
requires principals to preauthenticate using a hardware device
before being allowed to kinit.  (Sets the
.SM KRB5_KDB_REQUIRES_HW_AUTH
flag.)
.B \-requires_hwauth
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_svr\fP
.B \-allow_svr
prohibits the issuance of service tickets for principals.  (Sets the
.SM KRB5_KDB_DISALLOW_SVR
flag.)
.B +allow_svr
clears this flag.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_tgs_req\fP
.B \-allow_tgs_req
specifies that a Ticket-Granting Service (TGS) request for a service
ticket for principals is not permitted.  This option is useless for
most things.
.B +allow_tgs_req
clears this flag.  The default is
.BR +allow_tgs_req .
In effect,
.B \-allow_tgs_req
sets the
.SM KRB5_KDB_DISALLOW_TGT_BASED
flag on principals in the database.
.TP
{\fB\-\fP|\fB+\fP}\fBallow_tix\fP
.B \-allow_tix
forbids the issuance of any tickets for principals.
.B +allow_tix
clears this flag.  The default is
.BR +allow_tix .
In effect,
.B \-allow_tix
sets the
.SM KRB5_KDB_DISALLOW_ALL_TIX
flag on principals in the database.
.TP
{\fB\-\fP|\fB+\fP}\fBneedchange\fP
.B +needchange
sets a flag in attributes field to force a password change;
.B \-needchange
clears it. The default is
.BR \-needchange .
In effect,
.B +needchange
sets the
.SM KRB5_KDB_REQUIRES_PWCHANGE
flag on principals in the database.
.TP
{\fB\-\fP|\fB+\fP}\fBpassword_changing_service\fP
.B +password_changing_service
sets a flag in the attributes field marking principal as a password change
service principal (useless for most things).
.B \-password_changing_service
clears the flag. This flag intentionally has a long name. The default
is
.BR \-password_changing_service .
In effect,
.B +password_changing_service
sets the
.SM KRB5_KDB_PWCHANGE_SERVICE
flag on principals in the database.
.TP
\fIpolicy_name\fP
Specifies the name of the ticket policy.
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu create_policy \-r ATHENA.MIT.EDU \-maxtktlife "1 day" \-maxrenewlife "1 week" \-allow_postdated +needchange \-allow_forwardable tktpolicy\fP
.nf
Password for "cn=admin,o=org":
.fi
.RE
.TP
\fBmodify_policy\fP [\fB\-r\fP\ \fIrealm\fP] [\fB\-maxtktlife\fP\ \fImax_ticket_life\fP] [\fB\-maxrenewlife\fP\ \fImax_renewable_ticket_life\fP] [\fIticket_flags\fP] \fIpolicy_name\fP
Modifies the attributes of a ticket policy. Options are same as 
.B create_policy.
.RS
.TP
\fB\-r\fP\ \fIrealm\fP
Specifies the Kerberos realm of the database; by default the realm
returned by
.IR krb5_default_local_realm (3)
is used.
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu modify_policy \-r ATHENA.MIT.EDU \-maxtktlife "60 minutes" \-maxrenewlife "10 hours" +allow_postdated \-requires_preauth tktpolicy\fP
.nf
Password for "cn=admin,o=org":
.fi
.RE
.TP
\fBview_policy\fP [\fB\-r\fP\ \fIrealm\fP] \fIpolicy_name\fP
Displays the attributes of a ticket policy. Options:
.RS
.TP
\fIpolicy_name\fP
Specifies the name of the ticket policy.
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu view_policy \-r ATHENA.MIT.EDU tktpolicy\fP
.nf
Password for "cn=admin,o=org":
            Ticket policy: tktpolicy
      Maximum ticket life: 0 days 01:00:00
   Maximum renewable life: 0 days 10:00:00
             Ticket flags: DISALLOW_FORWARDABLE REQUIRES_PWCHANGE
.fi
.RE
.TP
\fBdestroy_policy\fP [\fB\-r\fP\ \fIrealm\fP] [\fB\-force\fP] \fIpolicy_name\fP
Destroys an existing ticket policy. Options:
.RS
.TP
\fB\-r\fP\ \fIrealm\fP
Specifies the Kerberos realm of the database; by default the realm
returned by
.IR krb5_default_local_realm (3)
is used.
.TP
\fB\-force\fP
Forces the deletion of the policy object. If not specified, will be prompted for confirmation while deleting the policy. Enter 
.B yes
to confirm the deletion.
.TP
\fIpolicy_name\fP
Specifies the name of the ticket policy.
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu destroy_policy \-r ATHENA.MIT.EDU tktpolicy\fP
.nf
Password for "cn=admin,o=org":
This will delete the policy object 'tktpolicy', are you sure?
(type 'yes' to confirm)? yes
** policy object 'tktpolicy' deleted.
.fi
.RE
.TP
\fBlist_policy\fP [\fB\-r\fP\ \fIrealm\fP]
Lists the ticket policies in \fIrealm\fP if specified or in the default realm.  Options:
.RS
.TP
\fB\-r\fP\ \fIrealm\fP
Specifies the Kerberos realm of the database; by default the realm
returned by
.IR krb5_default_local_realm (3)
is used.
.TP
EXAMPLE:
\fBkdb5_ldap_util \-D cn=admin,o=org \-H ldaps://ldap-server1.mit.edu list_policy \-r ATHENA.MIT.EDU\fP
.nf
Password for "cn=admin,o=org":
tktpolicy
tmppolicy
userpolicy
.fi
.RE

.SH SEE ALSO
kadmin(8)

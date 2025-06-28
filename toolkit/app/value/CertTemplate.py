_1CRTCER = """
RACDCERT +
     GENCERT + 
      {Owner} +
      WITHLABEL('{New Label}') +
      SIZE(2048) +
      KEYUSAGE(HANDSHAKE) +
   {Subject_Name}

RACDCERT {Owner} LIST

SETR RACLIST(DIGTCERT) REFRESH
"""

_2CRTCSR = """
RACDCERT {Owner} +
 GENREQ(
   LABEL('{New Label}') +
) +
DSN('{CSR}')
"""

_3REOLD = """
RACDCERT ALTER( +
LABEL('{Current Label}') +
 {Owner} +
NEWLABEL('{Expiring Label}') +
NOTRUST

RACDCERT {Owner} LIST

SETR RACLIST(DIGTCERT) REFRESH
"""

_4ADDCER = """
RACDCERT +
 {Owner} +
 ADD('{CER}') +
 WITHLABEL('{New Label}') +
TRUST

RACDCERT ALTER( +
 LABEL('{New Label}') +
 {Owner} +
 NEWLABEL('{Current Label}') +
TRUST

RACDCERT {Owner} LIST

SETR RACLIST(DIGTCERT) REFRESH
"""

_4CHGCER = """
RACDCERT ALTER( +
 LABEL('{New Label}') +
 {Owner} +
 NEWLABEL('{Current Label}') +
TRUST

RACDCERT {Owner} LIST

SETR RACLIST(DIGTCERT) REFRESH
"""

_5ADDKR1 = """
RACDCERT + 
{Owner} +
  CONNECT( +
  ID({Keyring Owner}) +
  LABEL('{Current Label}') +
RING({Keyring}) +
USAGE(PERSONAL) {Key Mode}

RACDCERT LISTRING({Keyring}) +
ID({Keyring Owner})
"""

_6RMVKR1 = """
RACDCERT + 
ID({Keyring Owner}) +
  REMOVE( +
  {Owner}
  LABEL('{Expiring Label}') +
RING({Keyring}) +
)

RACDCERT LISTRING({Keyring}) +
ID({Keyring Owner})

"""

REFRESH_KEYRING = """
SETR RACLIST(DIGTCERT) REFRESH
SETR RACLIST(DIGTRING) REFRESH
"""

JC_LOG = """
//{jc} JOB (XXXXXX),'RUN RACF CMDS',CLASS={class},MSGCLASS=X,
//     MSGLEVEL=(1,1),NOTIFY=&SYSUID
//CMDLIB SET CMDLIB={desfile}
//CMDLOG SET CMDLOG={desfile}.{type}LOG
//*************************************************************
//IMPL EXEC INCMDS,MBR={member}
"""

JC_NOLOG = """
//{jc} JOB (XXXXXX),'RUN RACF CMDS',CLASS={class},MSGCLASS=X,
//     MSGLEVEL=(1,1),NOTIFY=&SYSUID
//STEP1    EXEC PGM=IKJEFT01
//SYSTSPRT DD   SYSOUT=*
//SYSTSIN  DD   *
"""


/*
 * lib/krb5/os/init_ctx.c
 *
 * Copyright 1994 by the Massachusetts Institute of Technology.
 * All Rights Reserved.
 *
 * Export of this software from the United States of America may
 *   require a specific license from the United States Government.
 *   It is the responsibility of any person or organization contemplating
 *   export to obtain such a license before exporting.
 * 
 * WITHIN THAT CONSTRAINT, permission to use, copy, modify, and
 * distribute this software and its documentation for any purpose and
 * without fee is hereby granted, provided that the above copyright
 * notice appear in all copies and that both that copyright notice and
 * this permission notice appear in supporting documentation, and that
 * the name of M.I.T. not be used in advertising or publicity pertaining
 * to distribution of the software without specific, written prior
 * permission.  M.I.T. makes no representations about the suitability of
 * this software for any purpose.  It is provided "as is" without express
 * or implied warranty.
 *
 * krb5_init_contex()
 */

#define NEED_WINDOWS
#include "k5-int.h"

#ifdef macintosh
static CInfoPBRec	theCatInfo;
static	char		*FileBuffer;
static	int			indexCount;
static FSSpec		theWorkingFile;

static char*
GetDirName(short vrefnum, long dirid, char *dststr)
{
CInfoPBRec	theCatInfo;
FSSpec		theParDir;
char		str[37];
char		*curstr;
OSErr		err;
	// Get info on the directory itself, it's name and it's parent
	theCatInfo.dirInfo.ioCompletion		= NULL;
	theCatInfo.dirInfo.ioNamePtr		= (StringPtr) str;
	theCatInfo.dirInfo.ioVRefNum		= vrefnum;
	theCatInfo.dirInfo.ioFDirIndex		= -1;
	theCatInfo.dirInfo.ioDrDirID		= dirid;
	err = PBGetCatInfoSync(&theCatInfo);

	// If I'm looking at the root directory and I've tried going up once
	// start returning down the call chain
	if (err != noErr || (dirid == 2 && theCatInfo.hFileInfo.ioFlParID == 2))
		return dststr;

	// Construct a file spec for the parent
	curstr = GetDirName(theCatInfo.dirInfo.ioVRefNum, theCatInfo.hFileInfo.ioFlParID, dststr);

	// Copy the pascal string to the end of a C string
	BlockMoveData(&str[1], curstr, str[0]);
	curstr += str[0];
	*curstr++ = ':';
	
	// return a pointer to the end of the string (for someone below to append to)
	return curstr;
}

static void
GetPathname(FSSpec *theFile, char *dststr)
{
FSSpec		theParDir;
char		*curstr;
OSErr		err;

	// Start crawling up the directory path recursivly
	curstr = GetDirName(theFile->vRefNum, theFile->parID, dststr);
	BlockMoveData(&theFile->name[1], curstr, theFile->name[0]);
	curstr += theFile->name[0];
	*curstr = 0;
}

char*
GetMacProfilePathName(Str255 filename)
{
short	vRefnum;
long	parID;
OSErr	theErr;
FSSpec	krbSpec;
char	pathbuf[255];

	theErr = FindFolder(kOnSystemDisk, kPreferencesFolderType, kDontCreateFolder, &vRefnum, &parID);
	FSMakeFSSpec(vRefnum, parID, filename, &krbSpec);
	GetPathname(&krbSpec, &pathbuf);
	return strdup(pathbuf);
}
#endif /* macintosh */

#if defined(_MSDOS) || defined(_WIN32)

static krb5_error_code
get_from_windows_dir(
    char **pname
    )
{
    UINT size = GetWindowsDirectory(0, 0);
    *pname = malloc(size + 1 +
                    strlen(DEFAULT_PROFILE_FILENAME) + 1);
    if (*pname)
    {
        GetWindowsDirectory(*pname, size);
        strcat(*pname, "\\");
        strcat(*pname, DEFAULT_PROFILE_FILENAME);
        return 0;
    } else {
        return KRB5_CONFIG_CANTOPEN;
    }
}

static krb5_error_code
get_from_module_dir(
    char **pname
    )
{
    const DWORD size = 1024; /* fixed buffer */
    int found = 0;
    char *p;
    char *name;
    struct _stat s;

    *pname = 0;

    name = malloc(size);
    if (!name)
        return ENOMEM;

    if (!GetModuleFileName(GetModuleHandle("krb5_32"), name, size))
        goto cleanup;

    p = name + strlen(name);
    while ((p >= name) && (*p != '\\') && (*p != '/')) p--;
    if (p < name)
        goto cleanup;
    p++;
    strncpy(p, DEFAULT_PROFILE_FILENAME, size - (p - name));
    name[size - 1] = 0;
    found = !_stat(name, &s);

 cleanup:
    if (found)
        *pname = name;
    else
        if (name) free(name);
    return 0;
}

/*
 * get_from_registry
 *
 * This will find a profile in the registry.  *pbuffer != 0 if we
 * found something.  Make sure to free(*pbuffer) when done.  It will
 * return an error code if there is an error the user should know
 * about.  We maintain the invariant: return value != 0 => 
 * *pbuffer == 0.
 */
static krb5_error_code
get_from_registry(
    char** pbuffer,
    HKEY hBaseKey
    )
{
    HKEY hKey = 0;
    LONG rc = 0;
    DWORD size = 0;
    krb5_error_code retval = 0;
    const char *key_path = "Software\\MIT\\Kerberos5";
    const char *value_name = "config";

    /* a wannabe assertion */
    if (!pbuffer)
    {
        /*
         * We have a programming error!  For now, we segfault :)
         * There is no good mechanism to deal.
         */
    }
    *pbuffer = 0;

    if ((rc = RegOpenKeyEx(hBaseKey, key_path, 0, KEY_QUERY_VALUE, 
                           &hKey)) != ERROR_SUCCESS)
    {
        /* not a real error */
        goto cleanup;
    }
    rc = RegQueryValueEx(hKey, value_name, 0, 0, 0, &size);
    if ((rc != ERROR_SUCCESS) &&  (rc != ERROR_MORE_DATA))
    {
        /* not a real error */
        goto cleanup;
    }
    *pbuffer = malloc(size);
    if (!*pbuffer)
    {
        retval = ENOMEM;
        goto cleanup;
    }
    if ((rc = RegQueryValueEx(hKey, value_name, 0, 0, *pbuffer, &size)) != 
        ERROR_SUCCESS)
    {
        /*
         * Let's not call it a real error in case it disappears, but
         * we need to free so that we say we did not find anything.
         */
        free(*pbuffer);
        *pbuffer = 0;
        goto cleanup;
    }
 cleanup:
    if (hKey)
        RegCloseKey(hKey);
    if (retval && *pbuffer)
    {
        free(*pbuffer);
        /* Let's say we did not find anything: */
        *pbuffer = 0;
    }
    return retval;
}

#endif /* _MSDOS || _WIN32 */

static void
free_filenames(filenames)
	char **filenames;
{
    char **cp;

    if (filenames == 0)
        return;
    
    for (cp = filenames; *cp; cp++)
	free(*cp);
    free(filenames);
}

static krb5_error_code
os_get_default_config_files(pfilenames, secure)
	char ***pfilenames;
	krb5_boolean secure;
{
    char **filenames;
#ifdef macintosh
    filenames = malloc(3 * sizeof(char *));
    filenames[0] = GetMacProfilePathName("\pkrb Configuration");
    filenames[1] = GetMacProfilePathName("\pkrb5.ini");
    filenames[2] = 0;
#else /* !macintosh */
#if defined(_MSDOS) || defined(_WIN32)
    krb5_error_code retval = 0;
    char *name = 0;

    if (!secure)
    {
        char *env = getenv("KRB5_CONFIG");
        if (env)
        {
            name = malloc(strlen(env) + 1);
            if (!name) return ENOMEM;
            strcpy(name, env);
        }
    }
    if (!name && !secure)
    {
        /* HKCU */
        retval = get_from_registry(&name, HKEY_CURRENT_USER);
        if (retval) return retval;
    }
    if (!name)
    {
        /* HKLM */
        retval = get_from_registry(&name, HKEY_LOCAL_MACHINE);
        if (retval) return retval;
    }
    if (!name && !secure)
    {
        /* module dir */
        retval = get_from_module_dir(&name);
        if (retval) return retval;
    }
    if (!name)
    {
        /* windows dir */
        retval = get_from_windows_dir(&name);
    }
    if (retval)
        return retval;
    if (!name)
        return KRB5_CONFIG_CANTOPEN; /* should never happen */
    
    filenames = malloc(2 * sizeof(char *));
    filenames[0] = name;
    filenames[1] = 0;
#else /* !_MSDOS && !_WIN32 */
    char* filepath = 0;
    int n_entries, i;
    int ent_len;
    const char *s, *t;
    errcode_t retval;

    if (!secure) filepath = getenv("KRB5_CONFIG");
    if (!filepath) filepath = DEFAULT_PROFILE_PATH;

    /* count the distinct filename components */
    for(s = filepath, n_entries = 1; *s; s++) {
        if (*s == ':')
            n_entries++;
    }

    /* the array is NULL terminated */
    filenames = (char**) malloc((n_entries+1) * sizeof(char*));
    if (filenames == 0)
        return ENOMEM;

    /* measure, copy, and skip each one */
    for(s = filepath, i=0; (t = strchr(s, ':')) || (t=s+strlen(s)); s=t+1, i++)
    {
        ent_len = t-s;
        filenames[i] = (char*) malloc(ent_len + 1);
        if (filenames[i] == 0) {
            /* if malloc fails, free the ones that worked */
            while(--i >= 0) free(filenames[i]);
            free(filenames);
            return ENOMEM;
        }
        strncpy(filenames[i], s, ent_len);
        filenames[i][ent_len] = 0;
        if (*t == 0) {
            i++;
            break;
        }
    }
    /* cap the array */
    filenames[i] = 0;
#endif /* !_MSDOS && !_WIN32 */
#endif /* !macintosh */
    *pfilenames = filenames;
    return 0;
}


/* Set the profile paths in the context. If secure is set to TRUE then 
   do not include user paths (from environment variables, etc.)
*/
static krb5_error_code
os_init_paths(ctx, secure)
	krb5_context ctx;
	krb5_boolean secure;
{
    krb5_error_code	retval = 0;
    char **filenames = 0;

    ctx->profile_secure = secure;

    retval = os_get_default_config_files(&filenames, secure);

    if (!retval)
        retval = profile_init(filenames, &ctx->profile);

    if (filenames)
        free_filenames(filenames);

    if (retval)
        ctx->profile = 0;

    if (retval == ENOENT)
        return KRB5_CONFIG_CANTOPEN;

    if ((retval == PROF_SECTION_NOTOP) ||
        (retval == PROF_SECTION_SYNTAX) ||
        (retval == PROF_RELATION_SYNTAX) ||
        (retval == PROF_EXTRA_CBRACE) ||
        (retval == PROF_MISSING_OBRACE))
        return KRB5_CONFIG_BADFORMAT;

    return retval;
}

krb5_error_code
krb5_os_init_context(ctx)
	krb5_context ctx;
{
	krb5_os_context os_ctx;
	krb5_error_code	retval = 0;

	if (ctx->os_context)
		return 0;

	os_ctx = malloc(sizeof(struct _krb5_os_context));
	if (!os_ctx)
		return ENOMEM;
	memset(os_ctx, 0, sizeof(struct _krb5_os_context));
	os_ctx->magic = KV5M_OS_CONTEXT;

	ctx->os_context = (void *) os_ctx;

	os_ctx->time_offset = 0;
	os_ctx->usec_offset = 0;
	os_ctx->os_flags = 0;
	os_ctx->default_ccname = 0;

	krb5_cc_set_default_name(ctx, NULL);

	retval = os_init_paths(ctx, FALSE);

	/*
	 * If there's an error in the profile, return an error.  Just
	 * ignoring the error is a Bad Thing (tm).
	 */

	return retval;
}

krb5_error_code
krb5_set_config_files(ctx, filenames)
	krb5_context ctx;
	const char **filenames;
{
	krb5_error_code retval;
	profile_t	profile;
	
	retval = profile_init(filenames, &profile);
	if (retval)
		return retval;

	if (ctx->profile)
		profile_release(ctx->profile);
	ctx->profile = profile;

	return 0;
}

KRB5_DLLIMP krb5_error_code KRB5_CALLCONV
krb5_get_default_config_files(pfilenames)
	char ***pfilenames;
{
    if (!pfilenames)
        return EINVAL;
    return os_get_default_config_files(pfilenames, FALSE);
}

KRB5_DLLIMP void KRB5_CALLCONV
krb5_free_config_files(filenames)
	char **filenames;
{
    free_filenames(filenames);
}

krb5_error_code
krb5_secure_config_files(ctx)
	krb5_context ctx;
{
	krb5_error_code retval;
	
	if (ctx->profile) {
		profile_release(ctx->profile);
		ctx->profile = 0;
	}

	retval = os_init_paths(ctx, TRUE);

	return retval;
}

void
krb5_os_free_context(ctx)
	krb5_context	ctx;
{
	krb5_os_context os_ctx;

	os_ctx = ctx->os_context;
	
	if (!os_ctx)
		return;

	if (os_ctx->default_ccname)
		free(os_ctx->default_ccname);

	os_ctx->magic = 0;
	free(os_ctx);
	ctx->os_context = 0;

	if (ctx->profile)
	    profile_release(ctx->profile);
}

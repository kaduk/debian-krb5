/*
 * lib/gssapi/krb5/import_sec_context.c
 *
 * Copyright 1995 by the Massachusetts Institute of Technology.
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
 */

/*
 * import_sec_context.c	- Internalize the security context.
 */
#include "gssapiP_krb5.h"

OM_uint32
krb5_gss_import_sec_context(context,
			    minor_status, interprocess_token, context_handle)
    krb5_context	context;
    OM_uint32		*minor_status;
    gss_buffer_t	interprocess_token;
    gss_ctx_id_t	*context_handle;
{
    krb5_error_code	kret;
    OM_uint32		retval;
    krb5_context	ser_ctx;
    size_t		blen;
    krb5_gss_ctx_id_t	*ctx;
    krb5_octet		*ibp;

    /* Assume a tragic failure */
    ser_ctx = (krb5_context) NULL;
    ctx = (krb5_gss_ctx_id_t *) NULL;
    retval = GSS_S_FAILURE;
    *minor_status = 0;

    /* Get a fresh Kerberos context */
    if (!(kret = krb5_init_context(&ser_ctx))) {
	/* Initialize the serializers */
	if (!(kret = krb5_ser_context_init(ser_ctx)) &&
	    !(kret = krb5_ser_auth_context_init(ser_ctx)) &&
	    !(kret = krb5_ser_ccache_init(ser_ctx)) &&
	    !(kret = krb5_ser_rcache_init(ser_ctx)) &&
	    !(kret = krb5_ser_keytab_init(ser_ctx)) &&
	    !(kret = kg_ser_context_init(ser_ctx))) {

	    /* Internalize the context */
	    ibp = (krb5_octet *) interprocess_token->value;
	    blen = (size_t) interprocess_token->length;
	    if (!(kret = krb5_internalize_opaque(ser_ctx,
						 KG_CONTEXT,
						 (krb5_pointer *) &ctx,
						 &ibp,
						 &blen))) {

		/* Make sure that everything is cool. */
		if (kg_validate_ctx_id((gss_ctx_id_t) ctx)) {
		    interprocess_token->value = ibp;
		    interprocess_token->length = blen;
		    *context_handle = (gss_ctx_id_t) ctx;
		    retval = GSS_S_COMPLETE;
		}
	    }
	}
	krb5_free_context(ser_ctx);
    }
    if (retval != GSS_S_COMPLETE) {
	if (ctx) {
	    (void) kg_delete_ctx_id((gss_ctx_id_t) ctx);
	    if (ctx->enc.processed)
		krb5_finish_key(ctx->context, &ctx->enc.eblock);
	    krb5_free_keyblock(ctx->context, ctx->enc.key);
	    if (ctx->seq.processed)
		krb5_finish_key(ctx->context, &ctx->seq.eblock);
	    krb5_free_principal(ctx->context, ctx->here);
	    krb5_free_principal(ctx->context, ctx->there);
	    krb5_free_keyblock(ctx->context, ctx->subkey);
	    
	    /* Zero out context */
	    memset(ctx, 0, sizeof(*ctx));
	    xfree(ctx);
	}
	if (*minor_status == 0)
	    *minor_status = (OM_uint32) kret;
    }
    return(retval);
}

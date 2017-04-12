"""Only keep the data for the own national cert, if a specific
annotation was set for this organisation
"""

def determine_directives(context):
    context.logger.debug("============= 07national_cert_filter.py  ===========")
    context.logger.debug("Content of the Context BEFORE this script:")
    context.logger.debug("Organisations %r" % context.organisations)
    context.logger.debug("Matches %r" % context.matches)

    FILTER_CERT = "DE"
    FILTER_ANNOTATION = "Erhalte-DE"

    cc_field = context.section + ".geolocation.cc"

    # Only run this script, if source or destination .geolocation.cc are 
    # FILTER_CERT
    if context.get(cc_field) != FILTER_CERT:
       return 

    
    new_matches = []

    # iterate the matches.
    for match in context.matches:
        # Only take the datasets, which match on the field geolocation.cc
        if match.field == 'geolocation.cc':
            # This indicates a candidate where REMOVAL of the Organisation
            # from the match migth be required...
            orgs = get_orgs_for_match(context, match)
            kept_org_ids = set()

            # Iterate the orgs.
            for org in orgs:
                annos = org.annotations
                for a in annos:
                   if a.tag == FILTER_ANNOTATION: 
                       # only keep those organisations in this match, if the 
                       # organisations has the FILTER_ANNOTATION annotation.
                       kept_org_ids.add(org.orgid)
                       break

            # Overwrite the organisations of this match with those we decided to keep
            match.organisations = kept_org_ids

            # Decide if this Match shall be kept at all: If no Orgs exist, we don't need to.
            if match.organisations:
                new_matches.append(match)

        else:
          # this match is not relevant....
          new_matches.append(match)


    # Overwrite the contexts matches
    context.matches = new_matches
    
    context.logger.debug("Content of the Context AFTER this script:")
    context.logger.debug("Organisations %r" % context.organisations)
    context.logger.debug("Matches %r" % context.matches)
    
    # We'll return None, as other scripts shall still run....
    return None 

def get_orgs_for_match(context, match):
    # TODO Duplicated from 51avalanche.py, might be 
    # a candidate for a convenience function.
    # Return the Organisations which are listed within a match
    org_ids = match.organisations
    orgs = set()
    for o in org_ids:
        orgs.add(context.lookup_organisation(o))

    return orgs


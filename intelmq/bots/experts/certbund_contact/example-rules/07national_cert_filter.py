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

    # If the event is not related to the the country FILTER_CERT as
    # indicated by the cc_field, we don't need to do anything and exit
    # early.
    if context.get(cc_field) != FILTER_CERT:
        return

    # Now look at all matches for the geolocation.cc field and remove
    # all organisations referenced by such matches that do not have a
    # FILTER_ANNOTATION annotation. Keep the matches for other fields.
    #
    # Strategy: Build a new list of match objects by iterating over all
    # match objects and adding the match unchanged if it's not a match
    # for geolocation.cc or otherwise removing the organisations without
    # the relevant annotation from match before adding it (and only
    # adding it if any organsition remains)

    new_matches = []

    for match in context.matches:
        if match.field == 'geolocation.cc':
            # It's a geolocation match, so replace its list of
            # organisation IDs with a list of the IDs of all
            # organisations referenced by the match that have at least
            # one annotation tag equal to FILTER_ANNOTATION ...
            match.organisations = \
                [org.orgid
                 for org in context.organisations_for_match(match)
                 if any(a.tag == FILTER_ANNOTATION for a in org.annotations)]

            # .. and append it to the new list of matches if any
            # organisations remain
            if match.organisations:
                new_matches.append(match)

        else:
            # It's not a geolocation match, so append it to the new list
            # of matches unchanged.
            new_matches.append(match)


    # Overwrite the context's matches with the new list
    context.matches = new_matches

    context.logger.debug("Content of the Context AFTER this script:")
    context.logger.debug("Organisations %r" % context.organisations)
    context.logger.debug("Matches %r" % context.matches)

    # Return None, because other scripts still have to run
    return None

"""Only handle those organisations which are participating
in the test-run. Currently those are all Orgs that were added manually
and carry the tag "testbetrieb"
"""

TESTGROUP_TAG = "testbetrieb"

def determine_directives(context):
    context.logger.debug("============= 06testbetrieb.py ===========")
    context.logger.debug("Content of the Context BEFORE this script:")
    context.logger.debug("Organisations %r" % context.organisations)
    context.logger.debug("Matches %r" % context.matches)


    # Determine all manual matches, and the IDs of the Organisations
    # associated to this match.

    matching_orgs_manual = set()

    for match in context.matches:
        # Only take the manual datasets
        if match.managed == 'manual':
            # Write the ID of this matches organisation to the array.
            for org in match.organisations:
                matching_orgs_manual.add(org)


    new_orgs = []
    for m in matching_orgs_manual:
        org = context.lookup_organisation(m)
        # Iterate the tags of the Organisations and make sure the
        # Organisation is within the testgroup
        for anno in org.annotations:
            if anno.tag == TESTGROUP_TAG:
                new_orgs.append(org)

    # Overwrite the context 
    context.organisations = new_orgs
    
    context.logger.debug("Content of the Context AFTER this script:")
    context.logger.debug("Organisations %r" % context.organisations)
    context.logger.debug("Matches %r" % context.matches)
    
    # We'll return None, as other scripts shall still run....
    return None 

# coding=utf-8

def test_checkDiscovery(self, expextedAttribute, actualDiscovery):
    """
    Check discovery.

    :param expextedAttribute the resource attribute to filter
    :param actualDiscovery the reported Link Format
    :param actualDiscovery:
    :param expextedAttribute:
    :return True, if successful
    """

    # resource res = RemoteResource.newRoot(actualDiscovery)
    #
    # List < Option > query = new ArrayList < Option > ()
    # query.add(new Option(expextedAttribute, options.URI_QUERY))
    #
    # success = True
    #
    # for sub in res.getSubResources():
    #   success &= LinkFormat.matches(sub, query)
    #
    #       if not success:
    #           logging.info("FAIL: Expected %s, but was %s\n", expextedAttribute, LinkFormat.serialize(sub, null, false))
    #
    #            if success:
    #                logging.info("PASS: Correct Link Format filtering")


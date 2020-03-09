def get_domain_from_url(url: str) -> str:
    """
    :param url: the url whit the domain
    :type url: str
    :return: the domain of the give url
    :rtype: str
    """
    domain = ''
    if '.onion' in url:
        domain = url.split(".onion")[0]
    elif '.i2p' in url:
        domain = url.split(".i2p")[0]

    return domain

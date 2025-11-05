import connexion
import six

from swagger_server import util


def root_get():  # noqa: E501
    """Returns &#x27;&lt;h1&gt;Hello world&lt;/h1&gt;&#x27;

     # noqa: E501


    :rtype: str
    """
    return 'do some magic!'

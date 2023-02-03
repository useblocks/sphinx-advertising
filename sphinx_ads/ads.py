from typing import Any, Dict, List, Optional

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.errors import SphinxError

from sphinx_ads.directives.advertisement import AdsDirective
from sphinx_ads.logging import get_logger
from sphinx_ads.utils import get_json_data_from_path, get_json_data_from_url

VERSION = "0.0.1"


def setup(app: Sphinx) -> Dict[str, Any]:
    log = get_logger(__name__)
    log.debug("Starting setup of Sphinx-Ads")

    app.add_config_value("advertisement_path", None, "html", types=[str])
    app.add_config_value("advertisement_url", None, "html", types=[str])

    ########################################################################
    # DIRECTIVES
    ########################################################################

    # Define directives
    app.add_directive("sphinx-ads", AdsDirective)

    return {
        "version": VERSION,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }


def prepare_env(app: Sphinx, env: BuildEnvironment) -> None:
    """
    Prepares the sphinx environment to store sphinx-ads JSON data.
    """
    if not hasattr(env, "sphinx_ads_data"):
        # Used to store the Ads json data, so it can be easily accessible anywhere in the extension package.
        env.sphinx_ads_data = {}

    if app.config.advertisement_path is not None and len(app.config.advertisement_path) != 0:
        ads_json_data: Dict = get_json_data_from_path(app)
        env.sphinx_ads_data.update(ads_json_data)

    if app.config.advertisement_url is not None and len(app.config.advertisement_url) != 0:
        ads_json_data: Dict = get_json_data_from_url(app)
        env.sphinx_ads_data.update(ads_json_data)

    if (not app.config.advertisement_path and not app.config.advertisement_url) or (
        app.config.advertisement_path and app.config.advertisement_url
    ):
        raise AdsConfigException(
            "Please provide a path or url to retrieve the JSON data from "
            "using either the 'advertisement_path' or 'advertisement_url' variable."
        )

    if app.config.advertisement_path and app.config.advertisement_url:
        raise AdsConfigException(
            "Please provide only one of these variables: 'advertisement_path' or 'advertisement_url' variable."
        )


class AdsConfigException(SphinxError):
    pass

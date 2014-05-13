from ferris.core import routing, plugins
from ferris.controllers.download import Download

routing.route_controller(Download)

# Routes all App handlers
routing.auto_route()

# Default root route
# routing.default_root()

# Default root route
routing.redirect('/', to='/documents')


# Plugins
plugins.enable('settings')
plugins.enable('oauth_manager')

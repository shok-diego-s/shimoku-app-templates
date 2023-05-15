# Core python libraries
from os import getenv

# Third party
from shimoku_api_python import Client

# Local imports
from layout import plot_dashboard

# def setup_dashboard(shimoku: Client):
#     """
#     """
#     # Sets the business for the whole module
#     shimoku.dashboard.set_business(shimoku.app.business_id)
#
#     dashboard_name = 'Dashboard'
#
#     # Creates a dashboard and return it's dictionary representation
#     shimoku.dashboard.create_dashboard(dashboard_name=dashboard_name, order=0)
#
#     shimoku.dashboard.add_app_in_dashboard()


if __name__ == "__main__":

    # Create the client
    shimoku = Client(
        universe_id=getenv('UNIVERSE_ID'),
        access_token=getenv('API_TOKEN'),
        business_id=getenv('BUSINESS_ID'),
        verbosity='INFO',
        async_execution=True,
    )

    plot_dashboard(shimoku, menu_path="Vida media")

    # Execute all plots in asynchronous mode
    shimoku.activate_async_execution()
    shimoku.run()

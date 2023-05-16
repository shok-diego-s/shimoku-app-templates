# Core python libraries
from os import getenv

# Third party
from shimoku_api_python import Client

# Local imports
from layout import plot_dashboard

def setup_dashboard(shimoku: Client):
    """
    Does dashboard configuration
    """


    new_name = 'Dashboard'

    # Change the old dashboard name
    shimoku.dashboard.update_dashboard(
        dashboard_name='Default Name',
        name=new_name,
    )


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

    # setup_dashboard(shimoku)

    # Execute all plots in asynchronous mode
    shimoku.activate_async_execution()
    shimoku.run()

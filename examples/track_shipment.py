#!/usr/bin/env python
"""
This example shows how to track shipments.
"""
import logging
# adding sys to support running from command line
import sys
from example_config import CONFIG_OBJ
from fedex.services.track_service import FedexTrackRequest

"""
changed to a function
tracking_id is the value of the id. can be tracking number or another value, like invoice number
tracking_id_name is the name of the type of tracking id, e.g. INVOICE
process_type can be set to the string 'True' to include tracking details
ship_zip is required only if you are tracking by something other than tracking number
"""
def get_status(tracking_id, tracking_id_name=None, process_type=None, ship_zip=None):
    # Set this to the INFO level to see the response from Fedex printed in stdout.
    logging.basicConfig(level=logging.INFO)
    """
    added the below to capture more logs during debugging and to limit logs during production
    """
    logging.getLogger().setLevel(logging.ERROR)
    """
    added the below to get more data during debugging.
    uncomment these to log suds SOAP exchanges. Can set them to DEBUG or INFO, etc.
    via http://blogs.it.ox.ac.uk/inapickle/2011/05/15/using-logging-to-debug-what-suds-is-sending-across-the-wire/
    """
#    handler = logging.StreamHandler(sys.stderr)
#    logger = logging.getLogger('suds.transport.http')
#    logger.setLevel(logging.DEBUG), handler.setLevel(logging.DEBUG)
#    logger.addHandler(handler)
    
    # NOTE: TRACKING IS VERY ERRATIC ON THE TEST SERVERS. YOU MAY NEED TO USE
    # PRODUCTION KEYS/PASSWORDS/ACCOUNT #.
    # We're using the FedexConfig object from example_config.py in this dir.
    track = FedexTrackRequest(CONFIG_OBJ)
    """
    added very rough validation of input.
    """
    if not isinstance(tracking_id, str):

        tracking_id_str = tracking_id[0]

        if len(tracking_id) == 2:

            process_type = tracking_id[1]

        else:

            tracking_id_name = tracking_id[1]
            process_type = tracking_id[2]
    
    else:

        tracking_id_str = tracking_id

    track.TrackSelectionDetail.PackageIdentifier.Value = tracking_id_str

    """
    changed to set tracking id name only if one is provided.
    """
    if tracking_id_name:
        track.TrackSelectionDetail.PackageIdentifier.Type = tracking_id_name
    
    """
    added set processing option.
    """
    if process_type == 'True':
        track.ProcessingOptions = 'INCLUDE_DETAILED_SCANS'

    """
    added the ship zip if we have one.
    """
    if ship_zip:
        track.TrackSelectionDetail.Destination.PostalCode = ship_zip
        track.TrackSelectionDetail.Destination.CountryCode = 'US'

    # Fires off the request, sets the 'response' attribute on the object.
    track.send_request()
    

    # See the response printed out.
#    print track.response
    
    """
    added retrieve severity
    """
    severity = track.response.HighestSeverity

    """
    modified to collect result to return
    """
    match_list = list()
    # Look through the matches (there should only be one for a tracking number
    # query), and show a few details about each shipment.
    for match in track.response.CompletedTrackDetails:
        match_list.append(match)

    """
    Added for testing
    """
#    print match_list

    """
    added return result
    """
    return {'severity': severity, 'tracking': match_list}

"""
added to run from command line
only include the tracking number as an argument for testing from command line
"""
if __name__ == "__main__":
    get_status(sys.argv[1:])
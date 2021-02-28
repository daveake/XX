# XX

** OLD AND DEPRECATED **

This script is no longer required, since the SNUS now has the same ability to add X for the prediction, but for any number of payloads not just one.

** SO PLEASE DO NOT USE! **

Just set the payload document as described below and SNUS will do the rest.

----

Uploads "X marks the spot" position to habhub, using predicted landing position from a HAB

This script can be used where a balloon payload predicts its own landing position.
The spacenear.us map accepts a special "XX" payload ID, which tells it to display the payload as a big "X"
So the script extracts the landing position from a payload, and uploads that as a new payload "XX"

Since all such payloads need a payload document, an "XX" payload document has been created.  DO NOT CHANGE IT !!!

Your HAB payload needs to include the landing position, using these field names:

  pred_lat and pred_lon (for latitude and longitude)
  
  - or -
  
  predicted_latitude and predicted_longitude
  
To use:
  
  python3 xx.py <payload_ID>
    

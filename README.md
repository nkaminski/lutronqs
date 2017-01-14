# lutronqs - A Python library for interfacing with Lutron QS devices via the Telnet integration protocol.

# Tested Devices
 * Lutron Quantum lighting processor implementing revision H of the QS Telnet protocol

# Requirements
 * Python 3.x
 * Telnet access to QS processor

# Command Line Usage
      usage: lutronqs-cli [-h] --host HOST --user USER [--password PASSWORD]
                    --action ACTION --iid IID [--value VALUE]

      optional arguments:
       -h, --help           show this help message and exit
       --host HOST          IP/Hostname of the Lutron QS Processor
        --user USER          Username for QS processor login.
        --password PASSWORD  Password for QS processor login. Will be prompted 
                       if not provided.
        --action ACTION      Action to perform, one of:
                       getAreaScene|getAreaOccupancy|setAreaLevel|setAreaScene
        --iid IID            Integration ID of target area.
        --value VALUE        Value to set, required only for setXXX commands (default is 0)


# Library Functions
       LutronQS(hostname, username, password)
Attempts to establish a connection to the Lutron QS processor and returns an instance of the LutronQS class

       close()
Closes the connection to the Lutron QS processor and terminates the receiver thread.

       setAreaLevel(iid,level)
Sets the area with integration ID equal to 'iid' to the level specified by 'level'. Throws ConnectionError if the connection to the QS processor has been closed.

       setAreaScene(iid,scene)
Sets the area with integration ID equal to 'iid' to the scene specified by 'scene'. Throws ConnectionError if the connection to the QS processor has been closed.

       getAreaScene(iid,scene)
Gets the current scene being displayed in the area with integration ID equal to 'iid'. Throws ConnectionError if the connection to the QS processor has been closed and ProcessorError if the iid is invalid or unassigned.

       getAreaOccupancy(iid)
Gets the occupancy state (true/false) of the area specified by iid. Returns False if there is no occupancy sensing equipment in the area.

# Acknowledgements

Development of this library is sponsored by mHUB - http://www.mhubchicago.com/

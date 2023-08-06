Rohde & Schwarz ATS1800C Python instrument driver Version 1.0.0.2

Version history:

1.2.0.3 09/2021
- Added Feed Switcher control interface 'feed_switcher'
- Added new 'system' interface
- Added Trigger output control for Elevation
- Moved the following methods from general 'utilites' interface to a dedicated interface 'system': 
  - get_current_status()
  - preset()
  - wait_for_movements_finish()
  - Package require
- Package requirements for pyvisa now contain minimum version of 1.11.3


 1.0.0.2 02/2020
 - First version created

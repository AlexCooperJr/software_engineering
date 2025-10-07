#
# CloudLab Profile: Ubuntu 24.04 on Utah ARM nodes
#
# This profile requests one ARM-based node from the Utah cluster running Ubuntu 24.04.
#

import geni.portal as portal
import geni.rspec.pg as pg

# Create a portal context
pc = portal.Context()

# Define parameters
pc.defineParameter(
    "nodeType", 
    "Hardware Type", 
    portal.ParameterType.STRING, 
    "ampere",
    longDescription="Select ARM-based node type available at Utah (e.g., ampere or ampere-altra)."
)

# Bind parameters
params = pc.bindParameters()

# Create a request specification
request = pc.makeRequestRSpec()

# Create a node
node = request.RawPC("node1")
node.hardware_type = params.nodeType

# Use Ubuntu 24.04 (Noble Numbat)
node.disk_image = "urn:publicid:IDN+utah.cloudlab.us+image+ubuntu-24.04"

# Optional: Add public IP or network interface (default is public network)
iface = node.addInterface("eth0")
iface.addAddress(pg.IPv4Address("192.168.1.1", "255.255.255.0"))

# Print the RSpec
pc.printRequestRSpec(request)

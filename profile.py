#
# CloudLab Profile: Ubuntu 24.04 (ARM) on Utah nodes with Docker
#

import geni.portal as portal
import geni.rspec.pg as pg

pc = portal.Context()
pc.defineParameter(
    "nodeType",
    "Hardware Type",
    portal.ParameterType.STRING,
    "ampere",
    longDescription="Select ARM-based node type at Utah (e.g., ampere or ampere-altra)."
)
params = pc.bindParameters()

request = pc.makeRequestRSpec()

node = request.RawPC("node1")
node.hardware_type = params.nodeType

# ✅ Correct ARM Ubuntu 24.04 image URN
node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU24-64-ARM"

# Install Docker automatically
node.addService(pg.Execute(shell="bash", command="""sudo apt-get update -y &&
    sudo apt-get install -y ca-certificates curl gnupg &&
    sudo install -m 0755 -d /etc/apt/keyrings &&
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg &&
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
      https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null &&
    sudo apt-get update -y &&
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin &&
    sudo systemctl enable docker &&
    sudo systemctl start docker"""))

pc.printRequestRSpec(request)

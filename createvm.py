import boto.ec2
import os
import io
import keypair

region = 'eu-west-1'
imageId = "ami-0862aabda3fb488b5"
subnetId = "subnet-0d6a19e3fb731c836"
securityGroupId = "sg-bda895cc"

 # current script path
print("Current executing path %s" % os.path.realpath(__file__))

ec2 = boto.ec2.connect_to_region(region)

keypair = keypair.KeyPair(ec2,'ec2-keypairv2')

print("Connecting to region, %s!" % region)

currentworkingdir = os.path.abspath(os.path.dirname(__file__))
bootscriptpath = os.path.join(currentworkingdir, "automation/bootstrap.sh")

file = open(bootscriptpath, "r")
bootscript = file.read()

print("Creating key pair")
keypair.create_key_pair()

interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(subnet_id=subnetId,
                                                                    groups=[
                                                                        securityGroupId],
                                                                    associate_public_ip_address=True)
interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(interface)

instances = ec2.run_instances(
    image_id=imageId,
    min_count=1,
    max_count=1,
    instance_type='t2.micro',
    key_name='ec2-keypairv2.pem',
    user_data=bootscriptpath,
    network_interfaces=interfaces
)
print("ec2 instance started!")

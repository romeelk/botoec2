import boto.ec2
import os
import io

def create_key_pair():
   
    # if(os.path.exists('ec2-keypairv2.pem')):
    #     print("Key file already exists!")
    #     os.remove("ec2-keypairv2.pem")
    
    # create a file to store the key locally
    outfile = open('ec2-keypairv2.pem','w')

    if(check_key_pair_exists("ec2-keypairv2")):
          print("Key pair exists attached to ec2. deleting!")
          ec2.delete_key_pair("ec2-keypairv2")

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(key_name='ec2-keypairv2')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)


def check_key_pair_exists(name):
   key_pairs = ec2.get_all_key_pairs()
   for key in key_pairs:
       if(key.name == name):
           return True
   return False

region = 'eu-west-1'
imageId = "ami-0862aabda3fb488b5"
subnetId = "subnet-0e853e2305b84de2b"
securityGroupId = "sg-bda895cc"
ec2 = boto.ec2.connect_to_region(region)


print("Connection to region, %s!" % region)

currentworkingdir = os.path.abspath(os.path.dirname(__file__))
bootscriptpath = os.path.join(currentworkingdir, "automation/bootstrap.sh")

file = open(bootscriptpath,"r")
bootscript = file.read()

create_key_pair()

interface = boto.ec2.networkinterface.NetworkInterfaceSpecification(subnet_id=subnetId,
                                                                    groups=[securityGroupId],
                                                                    associate_public_ip_address=True)
interfaces = boto.ec2.networkinterface.NetworkInterfaceCollection(interface)

instances = ec2.run_instances(
     image_id=imageId,
     min_count=1,
     max_count=1,
     instance_type='t2.micro',
     key_name='ec2-keypairv2',
     user_data=bootscriptpath,
     network_interfaces=interfaces
    )


import boto.ec2
import os

class KeyPair:
    def __init__(self, ec2, name): 
        self.ec2 = ec2
        self.name = name

    def create_key_pair(self):
        pemfile = self.name + ".pem"
        if(os.path.exists(pemfile)):
            print("Key file already exists!")
            os.remove(pemfile)

        # create a file to store the key locally
        outfile = open(pemfile, 'w')

        if(self.__check_key_pair_exists(pemfile)):
            print("Key pair exists attached to ec2. deleting!")
            self.ec2.delete_key_pair(pemfile)
           
        key_pair = self.ec2.create_key_pair(key_name=pemfile)

        # call the boto ec2 function to create a key pair
      
        # capture the key and store it in a file
        key_pair_out = str(key_pair.material)
        outfile.write(key_pair_out)
        outfile.close()

    def __check_key_pair_exists(self,name):
        key_pairs = self.ec2.get_all_key_pairs()
        for key in key_pairs:
            if(key.name == name):
                return True
        return False
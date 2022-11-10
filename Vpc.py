import boto3
ec2=boto3.resource('ec2')
vpc=ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc.create_tags(Tags=[{
    "Key":"Name",
    "Value":"my_vpc"}])
vpc.wait_until_available()
ig=ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id)
route_table=vpc.create_route_table()
route=route_table.create_route(
DestinationCidrBlock='0.0.0.0/0',GatewayId=ig.id
)
subnet=ec2.create_subnet(CidrBlock='10.0.0.0/24',
VpcId=vpc.id)
route_table.associate_with_subnet(SubnetId=subnet.id)
securitygroup=ec2.create_security_group(GroupName='VPC-S',Description='only allow VPC traffic',VpcId=vpc.id)
securitygroup.authorize_ingress(CidrIp='0.0.0.0/0',IpProtocol='tcp',FromPort=22, ToPort=22)
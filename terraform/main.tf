resource "aws_instance" "devops_server" {
  ami           = "ami-03f4878755434977f" 
  instance_type = var.instance_type

  user_data = file("user_data.sh")

  tags = {
    Name = "DevOpsServer"
  }
}
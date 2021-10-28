provider "aws" {
  region = "eu-central-1"
  profile = "private"
}

resource "aws_instance" "klarna_api" {
  ami = "ami-0c960b947cbb2dd16" 
  instance_type = "t2.small"
  key_name = var.key_pair_name
  associate_public_ip_address = true
  vpc_security_group_ids = [aws_security_group.security_group.id]

 tags = {
    Name = "klarna-default-prediction-api"
  }

  connection {
    type = "ssh"
    user = "ubuntu"
    private_key = file("~/.ssh/${var.key_pair_name}.pem")
    host = aws_instance.klarna_api.public_ip
  }

  provisioner "file" {
    source = "docker-compose.yaml"
    destination = "/home/ubuntu/docker-compose.yaml"
  }

resource "aws_security_group" "security_group" {
  name = "klarna-security-group"

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = "80"
    to_port = "80"
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_role" "role" {
  name = "klarna-role"
  assume_role_policy = file("role-policy.json")
}

resource "aws_iam_policy" "policy" {
  name = "klarna-policy"
  policy = file("policy.json")
}

resource "aws_iam_role_policy_attachment" "attach" {
  role       = aws_iam_role.role.name
  policy_arn = aws_iam_policy.policy.arn
}
resource "aws_iam_instance_profile" "profile" {
  name = "klarna-profile"
  role = aws_iam_role.role.name
}
resource "aws_security_group" "web_sg" {
  name        = "web-sg"
  description = "Allow web and backend inbound traffic"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Backend API"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_server_1" {
  key_name                    = "arquitectura"
  ami                         = "ami-0c7217cdde317cfec"
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public[0].id
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name

  user_data = <<-EOF
              #!/bin/bash
              # Update packages
              yum update -y
              
              # Install Docker and docker-compose
              yum install -y docker aws-cli
              systemctl start docker
              systemctl enable docker
              
              # Install docker-compose
              curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
              
              # Create app directory
              mkdir -p /opt/app
              
              # Get the docker-compose file from S3
              aws s3 cp s3://${aws_s3_bucket.config_bucket.id}/docker-compose.yml /opt/app/docker-compose.yml
              
              # Create ECR login script
              echo '#!/bin/bash
              aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 086054568763.dkr.ecr.us-east-1.amazonaws.com
              ' > /opt/app/ecr-login.sh
              chmod +x /opt/app/ecr-login.sh
              
              # Create environment file with variables
              echo "BACKEND_ECR_URL=${aws_ecr_repository.backend_repo.repository_url}
              FRONTEND_ECR_URL=${aws_ecr_repository.frontend_repo.repository_url}
              DB_HOST=${aws_db_instance.postgres.address}
              DB_PASSWORD=${var.db_password}" > /opt/app/.env
              
              # Login to ECR and start containers
              /opt/app/ecr-login.sh
              cd /opt/app && docker-compose --env-file .env up -d
              EOF

  tags = {
    Name = "WebServer1"
  }
}

resource "aws_instance" "web_server_2" {
  key_name                    = "arquitectura"
  ami                         = "ami-0c7217cdde317cfec"
  instance_type               = "t2.micro"
  subnet_id                   = aws_subnet.public[1].id
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name

  user_data = <<-EOF
              #!/bin/bash
              # Update packages
              yum update -y
              
              # Install Docker and docker-compose
              yum install -y docker aws-cli
              systemctl start docker
              systemctl enable docker
              
              # Install docker-compose
              curl -L "https://github.com/docker/compose/releases/download/v2.24.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
              
              # Create app directory
              mkdir -p /opt/app
              
              # Get the docker-compose file from S3
              aws s3 cp s3://${aws_s3_bucket.config_bucket.id}/docker-compose.yml /opt/app/docker-compose.yml
              
              # Create ECR login script
              echo '#!/bin/bash
              aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 086054568763.dkr.ecr.us-east-1.amazonaws.com
              ' > /opt/app/ecr-login.sh
              chmod +x /opt/app/ecr-login.sh
              
              # Create environment file with variables
              echo "BACKEND_ECR_URL=${aws_ecr_repository.backend_repo.repository_url}
              FRONTEND_ECR_URL=${aws_ecr_repository.frontend_repo.repository_url}
              DB_HOST=${aws_db_instance.postgres.address}
              DB_PASSWORD=${var.db_password}" > /opt/app/.env
              
              # Login to ECR and start containers
              /opt/app/ecr-login.sh
              cd /opt/app && docker-compose --env-file .env up -d
              EOF

  tags = {
    Name = "WebServer2"
  }
}
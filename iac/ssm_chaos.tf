resource "aws_iam_role" "ssm_role" {
  name = "ec2-ssm-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_attach" {
  role       = aws_iam_role.ssm_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# resource "aws_ssm_document" "chaos_script" {
#   name          = "ChaosInjectionDocument"
#   document_type = "Command"

#   content = jsonencode({
#     schemaVersion = "2.2"
#     description   = "Chaos Engineering - Stress CPU"
#     mainSteps = [{
#       action = "aws:runShellScript"
#       name   = "stressCPU"
#       inputs = {
#         runCommand = [
#           "sudo yum install -y stress",
#           "stress --cpu 2 --timeout 60"
#         ]
#       }
#     }]
#   })
# }
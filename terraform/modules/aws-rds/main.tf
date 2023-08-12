locals {
  app_name = var.app_name
}

resource "aws_security_group" "rds_sg" {
  name        = "${local.app_name}-${var.rds_sg_name}"
  description = "RDS security group."
  vpc_id      = var.vpc_id

  ingress {
    protocol        = "tcp"
    from_port       = var.rds_port
    to_port         = var.rds_port
    security_groups = [var.ecs_sg_id]
  }
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name        = "${local.app_name}_rds_subnet_group"
  description = "Subnet group for RDS"
  subnet_ids  = [var.private_subnet_3_id, var.private_subnet_4_id]

  tags = {
    Name = "RDS subnet group"
  }
}

resource "aws_db_parameter_group" "app_db" {
  name   = "${local.app_name}-db"
  family = "postgres14"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

resource "aws_db_instance" "app_db" {
  identifier              = "${local.app_name}-db"
  instance_class          = "db.t3.micro"
  allocated_storage       = 5
  engine                  = "postgres"
  engine_version          = "14.3"
  username                = jsondecode(data.aws_secretsmanager_secret_version.db_creds.secret_string)["PROD_POSTGRES_USER"]
  password                = jsondecode(data.aws_secretsmanager_secret_version.db_creds.secret_string)["PROD_POSTGRES_PASS"]
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  parameter_group_name    = aws_db_parameter_group.app_db.name
  publicly_accessible     = false
  skip_final_snapshot     = true
  availability_zone       = var.rds_availability_zone
  backup_retention_period = 7
}

# resource "aws_db_instance" "app_db_replica" {
#   identifier             = "${local.app_name}-db-replica"
#   instance_class         = "db.t3.micro"
#   allocated_storage      = 5
#   engine                 = "postgres"
#   engine_version         = "14.3"
#   vpc_security_group_ids = [aws_security_group.rds_sg.id]
#   parameter_group_name   = aws_db_parameter_group.app_db.name
#   publicly_accessible    = false
#   skip_final_snapshot    = true
#   availability_zone      = "us-east-1b"
# 
#   # Specify the primary RDS instance as the source
#   replicate_source_db = aws_db_instance.app_db.id
# }
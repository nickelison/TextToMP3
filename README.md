# TextToMP3

A Django text-to-speech web application designed with a focus on scalable, secure cloud infrastructure using AWS. Originally built using Flask as a semester-length project for 50:198:441 (Distributed & Cloud Computing) at Rutgers–Camden in Spring 2023.

<p align="center">
  <img src="https://github.com/nickelison/TextToMP3/blob/main/texttomp3.gif?raw=true" />
</p>

Features include:

- Text-to-speech conversion using Amazon Polly, allowing users to convert text to MP3 files
- Functionality for management of generated MP3 files: listen, download, view text transcript, and delete
- User registration and account management capabilities
- A simple, intuitive user-friendly interface using Bootstrap
- AWS infrastructure automation achieved using Terraform
- Containerization using Docker

The purpose of the project was not to write an application, but to design and implement a highly scalable and secure cloud architecture on which an application could run. As such, most effort was expended on gaining familiarity with AWS — particularly with VPC and the networking aspects of cloud infrastructure — as well as with DevOps tools like Docker and Terraform. The application was containerized using Docker, and Terraform was used to automate the provisioning of almost all the requisite AWS resources. The AWS services used in this project include VPC, ECR, ECS, EC2, RDS, Lambda, S3, CloudFront, Route53, Certificate Manager, Secrets Manager, and CloudWatch.

For more information, you're encouraged to read the [original project write-up](https://github.com/nickelison/TextToMP3-Flask/blob/main/project.pdf) detailing how the application works, the design of the architecture, the networking and security aspects of the project, and how the project could be improved.

In summary, however:

- A standard three-tier architecture (presentation, application/logic, data) was used.
- A VPC was created with six subnets between two AZs. NACLs, security groups and route tables are used to control the traffic coming into and out of the network, as well as between subnets within the network. The purpose of resource segregation is for security, and the splitting of resources between AZs is for fault-tolerance.
- The Docker image is pushed to ECR, and the application is then deployed to an ECS service running on two EC2 instances located in different AZs. These EC2 instances are part of an ECS auto scaling group.
- An additional EC2 instance serves as a bastion host, allowing SSH forwarding into otherwise inaccessible EC2 instances.
- A PostgreSQL RDS database is used along with read-replica situated in a different AZ.
- A Lambda function is used for converting text to audio with Amazon Polly and storing the resulting audio file in an S3 bucket.
- Secrets Manager is used to securely store secrets, such as database credentials.
- CloudFront is used for serving user image files.

**AWS Architecture**

<p align="center">
  <img src="https://github.com/nickelison/TextToMP3/blob/main/architecture.jpg?raw=true" />
</p>
# A CI/CD pipeline for an AWS Lambda function

##### This project has the following requirements:
  - A function which takes 'h' as input and returns the post with the deepest comment thread on HackerNews, in the past *h* hours.
  - The CI/CD infrastructure to deploy to production.

##### Notes
  - The API endpoint ('hours' query string parameter required): [API](https://ot0rnmj6o7.execute-api.us-east-2.amazonaws.com/prod/prodLambdaFunction)
  - The deployed function does not perform the original task asked of the project, however the code for that is still included. The AWS API Gateway service has a hard timeout limit of 30 seconds. I realized this too late.
  - The Python function for parsing the HackerNews API is located in: `extras/standalone/main.py`.
  - The unit and integration tests are bare-bones and are just enough to demonstrate a functional pipeline.

##### Usage
  - Two sets of access credentials were provided:
    1. Sign into AWS using the AWS Login Info.
    2. Clone this repository using the AWS CodeCommit Login Info.

  - Deploy to the development environment on AWS:
    1. On the AWS Console, go to the AWS CodePipeline service home page.
    2. Go to where you cloned this repository and switch to this branch: **riiid-dev**
    3. Make the desired changes and push your code. I recommend changing line 11 in `python_function/main.py` from | `'body': "Hello Riiid Labs!   Hours: " + input_time` | to | `'body': "<sample_text_to_print>"` |.
    4. Watch the CodePipeline page and the **devPipeline** pipeline will trigger (might take a few seconds). This pipeline does the installation   of dependencies, unit testing, and the build. Note that only the **main** branch runs the upload stage where the artifact is uploaded to the   production s3 bucket.

  - Deploy to the production environment on AWS:
    1. Go to the AWS CodeCommit service home page. Click on the **brian-wijaya-riiid** repository.
    2. Create a pull request to merge the **riiid-dev** branch with the **main** branch.
    3. Go through the process and approve the pull request. The changes are now merged to main.
    4. Watch the CodePipeline page and the **prodPipeline** pipeline will trigger (might take a few seconds). This pipeline does the installation   of dependencies, unit testing, the build, and the upload.

  - Test locally:
    1. Clone the repository.
    2. Install Docker.
    3. Run | `docker build --target unittest test/unit/` | to run the unit tests.
    4. Run | `docker build --target integrationtest test/integration/` | to run the integration tests. (WIP. Requires a PostgreSQL server).
    5. Run | `./build.sh` | to package the Python application into a `.zip` file.

##### Implementation Details
  - The setup uses two accounts, one for development (dev) and another for production (prod). The pipelines are in the dev account. The Lambda function and the s3 bucket with its code are in the prod account.
  - The high-level flow is like this: CloudWatch signals CodePipeline anytime a change happens in the CodeCommit repository, which triggers the appropriate pipeline. Each pipeline is associated with its own CodeBuild project. Once a pull request is merged to the main branch, the production pipeline installs, tests, builds, and uploads the artifact (a zip file for the lambda function). There is a second lambda function in the prod account that is triggered when a zip file is uploaded to the s3 bucket. This secondary Lambda function updates the code used by the primary Lambda function and creates a CloudFormation stack with the primary function as a resource, thus creating a deployment in the production environment.

##### Thoughts
  - The HackerNews API is simple yet very inefficient. In order to obtain all the stories or posts in a time range, each story ID has to first be checked against a Unix time stamp. Then all of the matching story IDs are checked to see how many top level comments it has, and then how many child comments each top level comment has, and so on. This is achieved via recursion however for every new item ID, an API request has to be made to the [HackerNews API](https://github.com/HackerNews/API). This places a limit on how often these requests can be made before either a system timeout or a service denial comes into effect. Based on these observations I would not use this API in any production work.
  - The aforementioned hard time limit on the AWS API Gateway service was the curveball I didn't account for. A way around this is to put the python code as well as its own frontend API into one Docker container and deploy it via Kubernetes or AWS ECS. Thus providing a highly available, self-contained application to parse the HackerNews API. With this in mind I included a link to an online Python IDE with the code from `extras/standalone/main.py`, which I assume is hosted using a similar high availability approach: [repl Python IDE](https://repl.it/repls/SplendidFickleExams#main.py). Hit the green **Run** button and enter a value for *h* on the terminal to the right.
  - The unit and integration tests are not actual tests, they are simple functions where each performs a related task to the main code. They are solely for the purpose of implementing a working pipeline and have a lot of room for improvement. Same goes for the main code in `extras/standalone/main.py`, it's ugly but it works. The integration test is still in beta and thus is not part of either dev or prod pipelines. I'm able to run the integration test successfully on my local environment because I have a local PostgreSQL server. I'm working on automating Postgres installation in **devPipeline**.
  - The post-build trigger (the artifact upload), which updates the primary Lambda functions's code and creates the CloudFormation stack, can be implemented in a better way. Specifically, the secondary function can be deleted entirely. After artifact creation, the same logic can be accomplished via the AWS CLI during **prodPipeline** pipeline's execution, inside the build environment in the **Build** stage. This is the correct approach as it's the simplest and uses the least number of resources.
  - The ideal setup still uses a multi-account enviornment however all of the production pipelines and resources should exist only in the production account. Right now **prodPipeline** is in the dev account thus to accomplish the ideal setup it would need to reside in the prod account. This means granting cross-account privileges to the prod account's CodePipeline to access the CodeCommit repository in the dev account. I'm working on implementing this change. I have also granted some entities "fullAccess" permissions within AWS with the goal of accomplishing a minimal viable pipeline, as quickly as possible. The ideal approach grants only the required permissions per entitiy thus involves a deeper dive into all the actions involved in the AWS infrastructure.
  - This could have been accomplished via Jenkins, GitHub, Artifactory, and Docker/Kubernetes in a much shorter time. However, I wanted an AWS only solution first. I'm working on implementing a hybrid pipeline using EC2 instances, Terraform, and the aforementioned tools and technologies.


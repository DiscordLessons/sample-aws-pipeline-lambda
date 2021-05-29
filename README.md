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


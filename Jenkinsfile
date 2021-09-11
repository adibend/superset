pipeline {
   agent any


   stages {
       stage('Build Docker') {
           steps {
               script {
                   sh 'echo "JOB: $JOB_NAME" > ./version.txt'
                   sh 'echo "BUILD NUMBER: $BUILD_NUMBER" >> ./version.txt'
                   sh 'echo "GIT BRANCH:" $GIT_BRANCH >> ./version.txt'
                   sh 'echo "GIT LAST COMMIT:" $GIT_COMMIT >> ./version.txt'
                   sh 'echo "DOCKER NAME: $ENV_NAME/$IMAGE_NAME:$BRANCH_NAME-$BUILD_ID" >> ./version.txt'

                   sh '$(aws ecr get-login --no-include-email --region $REPOSITORY_REGION)'
                   def customImage = docker.build("$ENV_NAME/$IMAGE_NAME:$BRANCH_NAME-${env.BUILD_ID}")
                   docker.withRegistry("https://$REPOSITORY_URI") {
                        customImage.push()
                        customImage.push('$BRANCH_NAME-latest')
                   }
               }
           }
       }

       stage('Deploy to Kubernetes') {
           steps {
               script {

                    dir('helm/superset/') {

                    def deploymentTxt = readFile "values.yaml.template"
                    deploymentTxt = deploymentTxt.replaceAll("@@SECURITY_GROUP@@", "$SG_NAME")
                    deploymentTxt = deploymentTxt.replaceAll("@@AWS_CERT_ARN@@", "$AWS_CERT_ARN")
                    writeFile file: "values.yaml", text: deploymentTxt

                    sh 'pwd'
                    sh 'ls -la'
                    
                    sh 'helm upgrade --install --values values.yaml $IMAGE_NAME $IMAGE_NAME/$IMAGE_NAME --namespace=$KUBE_NAMESPACE'
                    // helm upgrade --install --values values.yaml superset superset/superset --namespace=qa
                    }

                //    def date = new Date()
                //    def ts = date.format("yyMMddHHmmsss", TimeZone.getTimeZone('UTC'))

                //    def deploymentTxt = readFile "kube/deployment.yaml.template"
                //    deploymentTxt = deploymentTxt.replaceAll("@@MICROSERVICE_NAME@@", "$IMAGE_NAME")
                //    deploymentTxt = deploymentTxt.replaceAll("@@MICROSERVICE_IMAGE@@", "$REPOSITORY_URI/$ENV_NAME/$IMAGE_NAME:$BRANCH_NAME-latest")
                //    deploymentTxt = deploymentTxt.replaceAll("@@MICROSERVICE_NAMESPACE@@", "$KUBE_NAMESPACE")
                //    deploymentTxt = deploymentTxt.replaceAll("@@UPDATE_DATE@@", "$ts")

                //    writeFile file: "kube/deployment.yaml", text: deploymentTxt
                //    catchError {
                //       sh 'kubectl delete configmap $IMAGE_NAME-configmap --namespace=$KUBE_NAMESPACE'
                //    }
                //    sh 'kubectl create configmap $IMAGE_NAME-configmap --from-env-file=kube/conf/$ENV_NAME.env --namespace=$KUBE_NAMESPACE'
                //    sh 'kubectl apply -f kube/deployment.yaml'
               }
           }
       }
    }
}
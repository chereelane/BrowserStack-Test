 pipeline {
   agent any
   stages {
       stage('setup') {
         steps {
             browserstack(credentialsId: 'c9198883-a803-4091-8021-0e7212fbeffc') {
                 sh 'python get-pip.py'
                 sh 'pip install -r requirements.txt'
                 sh 'python3 scripts/parallel.py'
             }
         }
       }
     }
   }


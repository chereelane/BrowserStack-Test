 pipeline {
   agent any
   stages {
       stage('setup') {
         steps {
             browserstack(credentialsId: 'c9198883-a803-4091-8021-0e7212fbeffc') {
                 sh 'npm install'
                 sh 'node scripts/parallel.py'
             }
         }
       }
     }
   }


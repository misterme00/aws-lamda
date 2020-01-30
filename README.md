# aws-lamda
 pipenv --python 3.7
 pipenv shell
 pipenv install requests
Note: If you are on macOS, you can install Pipenv using Homebrew:

 brew install pipenv
On Amazon Linux, or another environment, you can install using pip:

 pip3 install pipenv --user
Create the ZIP deployment package:

 PY_DIR='build/python/lib/python3.7/site-packages'
 # Create temporary build directory
 mkdir -p $PY_DIR
 # Generate requirements file
 pipenv lock -r > requirements.txt
 # Install packages into the target directory
 pip install -r requirements.txt --no-deps -t $PY_DIR
 cd build
 # Zip files
 zip -r ../requests_layer.zip .
 cd ..
 # Remove temporary directory
 rm -r build
Create the Lambda layer.

 aws lambda publish-layer-version \
 --layer-name requests \
 --compatible-runtimes python3.7 \
 --zip-file fileb://requests_layer.zip

# FUNCTION_NAME=$1
# FUNCTION_VERSION=$2
# ALIAS=$3

# # Check if the required arguments are provided
# if [ -z "$FUNCTION_NAME" ] || [ -z "$FUNCTION_VERSION" ] || [ -z "$ALIAS" ]; then
#     echo "Usage: $0 <function-name> <function-version> <alias>"
#     exit 1
# fi

# Create lambda dependencies package
if [ ! -d dependencies ]; then
    mkdir dependencies
    pip install rapidfuzz pydantic[email] --platform manylinux2014_x86_64 --only-binary=:all: --implementation cp --python-version 312 -t dependencies
    # pip install levenshtein -t dependencies
fi

# Creat temp dirs
mkdir temp_combined deployment
# Copy source code to temp dir
cp -r rule_engine/* temp_combined/
cp -r rule_engine_config/* temp_combined/
# Copy package dependencies to temp dir
cp -r dependencies/* temp_combined/
cd temp_combined
# Create zip file of temp_combined
zip -r ../deployment/deployment.zip *
cd ..

# Update lambda function
aws lambda update-function-code \
    --function-name cir-ds-rule-engine-fibe-basic \
    --zip-file fileb://deployment/deployment.zip


# # Step 1: Update the Lambda function code
# aws lambda update-function-code \
#     --function-name "$FUNCTION_NAME" \
#     --zip-file fileb://deployment/deployment.zip

# # Step 2: Publish a new version of the function
# aws lambda publish-version \
#     --function-name cir-ds-rule-engine-hdfc \
#     --description "Publishing new version"


# aws lambda create-alias \
#     --function-name cir-ds-rule-engine-hdfc \
#     --name uat-v1-0-0 \
#     --function-version 2 \
#     --description "UAT alias for version 1.0.0"


# # Step 3: Update or create an alias to point to the new version
# aws lambda update-alias \
#     --function-name cir-ds-rule-engine-hdfc \
#     --name "$ALIAS" \
#     --function-version "$FUNCTION_VERSION" \
#     --description ""


# # Delete temporary folders
rm -r temp_combined deployment
rm -r dependencies
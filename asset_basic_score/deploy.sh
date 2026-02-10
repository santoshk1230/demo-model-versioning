#!/bin/bash
set -e

# Usage: ./deploy.sh <function-name> [region]
# Example: ./deploy.sh cir-ds-rule-engine-pocketly us-east-1

if [ -z "$1" ]; then
    echo "Usage: $0 <function-name> [region]"
    echo "Example: $0 cir-ds-rule-engine-pocketly us-east-1"
    exit 1
fi

FUNCTION_NAME="$1"
REGION="${2:-us-east-1}"

echo "Deploying to Lambda function: $FUNCTION_NAME (region: $REGION)"

# Create lambda dependencies package from requirements-prod.txt
if [ ! -d dependencies ]; then
    echo "Installing production dependencies from requirements-prod.txt..."
    mkdir dependencies
    pip install -r ../requirements-prod.txt -t dependencies
fi

# Create temp dirs
mkdir -p temp_combined deployment

# Copy source code to temp dir
echo "Packaging source code..."
cp -r rule_engine/* temp_combined/
cp -r rule_engine_config/* temp_combined/

# Copy package dependencies to temp dir
cp -r dependencies/* temp_combined/

# Create zip file
echo "Creating deployment package..."
cd temp_combined
zip -r ../deployment/deployment.zip * -q
cd ..

# Update lambda function
echo "Updating Lambda function: $FUNCTION_NAME"
aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file fileb://deployment/deployment.zip \
    --region "$REGION"

echo "Lambda function updated successfully!"

# Cleanup
echo "Cleaning up temporary files..."
rm -rf temp_combined deployment dependencies
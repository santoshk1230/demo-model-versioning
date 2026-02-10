#!/bin/bash
set -e

# Usage: ./deploy_uat.sh <function-name> <alias-name> [version-description] [region]
# Example: ./deploy_uat.sh cir-ds-rule-engine-pocketly uat-v1-0-0 "UAT deployment v1.0.0" us-east-1

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <function-name> <alias-name> [version-description] [region]"
    echo "Example: $0 cir-ds-rule-engine-pocketly uat-v1-0-0 \"UAT deployment v1.0.0\" us-east-1"
    exit 1
fi

FUNCTION_NAME="$1"
ALIAS_NAME="$2"
VERSION_DESC="${3:-UAT deployment}"
REGION="${4:-us-east-1}"

echo "=== UAT Deployment ==="
echo "Function: $FUNCTION_NAME"
echo "Alias: $ALIAS_NAME"
echo "Region: $REGION"

# Create lambda dependencies package from requirements-prod.txt (Linux x86_64 compatible)
if [ ! -d dependencies ]; then
    echo "Installing production dependencies from requirements-prod.txt (Linux x86_64)..."
    mkdir dependencies
    pip install -r ../requirements-prod.txt \
        --platform manylinux2014_x86_64 \
        --only-binary=:all: \
        --implementation cp \
        --python-version 312 \
        -t dependencies
fi

# Create temp dirs
mkdir -p temp_combined deployment

# Copy source code
echo "Packaging source code..."
cp -r rule_engine/* temp_combined/
cp -r rule_engine_config/* temp_combined/

# Copy dependencies
cp -r dependencies/* temp_combined/

# Create zip file
echo "Creating deployment package..."
cd temp_combined
zip -r ../deployment/deployment.zip * -q
cd ..

# Step 1: Update the Lambda function code
echo "Uploading code to Lambda function: $FUNCTION_NAME"
aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file fileb://deployment/deployment.zip \
    --region "$REGION"

# Wait for update to complete
echo "Waiting for update to complete..."
sleep 5

# Step 2: Publish a new version
echo "Publishing new version..."
NEW_VERSION=$(aws lambda publish-version \
    --function-name "$FUNCTION_NAME" \
    --description "$VERSION_DESC" \
    --region "$REGION" \
    --query 'Version' \
    --output text)

echo "New version published: $NEW_VERSION"

# Step 3: Create or update alias
echo "Creating/updating alias: $ALIAS_NAME"
aws lambda update-alias \
    --function-name "$FUNCTION_NAME" \
    --name "$ALIAS_NAME" \
    --function-version "$NEW_VERSION" \
    --region "$REGION" \
    --description "$VERSION_DESC" 2>/dev/null || \
aws lambda create-alias \
    --function-name "$FUNCTION_NAME" \
    --name "$ALIAS_NAME" \
    --function-version "$NEW_VERSION" \
    --description "$VERSION_DESC" \
    --region "$REGION"

echo "=== UAT Deployment Complete ==="
echo "Alias $ALIAS_NAME now points to version $NEW_VERSION"

# Cleanup
echo "Cleaning up temporary files..."
rm -rf temp_combined deployment dependencies
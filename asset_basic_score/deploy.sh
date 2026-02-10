# Create lambda dependencies package
if [ ! -d dependencies ]; then
    mkdir dependencies
    pip install rapidfuzz -t dependencies
    pip install pydantic[email] -t dependencies
    pip install levenshtein -t dependencies
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

# Delete temporary folders
rm -r temp_combined deployment